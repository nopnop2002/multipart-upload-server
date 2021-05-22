# -*- coding: utf-8 -*-
import os
import sys
import werkzeug
from datetime import datetime
#from flask import Flask, request, render_template, send_file, Blueprint
from flask import *
from werkzeug.serving import WSGIRequestHandler
import logging
import json
import magic

# flask
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# create UPLOAD_DIR
UPLOAD_DIR = os.path.join(os.getcwd(), "uploaded")
logging.info("UPLOAD_DIR={}".format(UPLOAD_DIR))
if (os.path.exists(UPLOAD_DIR) == False):
	logging.warning("UPLOAD_DIR [{}] not found. Create this".format(UPLOAD_DIR))
	os.mkdir(UPLOAD_DIR)

# Added /uploaded to static_url_path
add_app = Blueprint("uploaded", __name__, static_url_path='/uploaded', static_folder='./uploaded')
app.register_blueprint(add_app)

@app.route("/")
def hello():
	files = []
	dirs = []
	meta = {
		"current_directory": UPLOAD_DIR
	}
	for (dirpath, dirnames, filenames) in os.walk(UPLOAD_DIR):
		logging.info("filenames={}".format(filenames))
		for name in filenames:
			nm = os.path.join(dirpath, name).replace(UPLOAD_DIR, "").strip("/").split("/")
			logging.info("nm={}".format(nm))
			# Skip if the file is in a subdirect
			# nm=['templates', 'index.html']
			if len(nm) != 1: continue

			fullpath = os.path.join(dirpath, name)
			logging.info("fullpath={}".format(fullpath))
			if os.path.isfile(fullpath) == False: continue
			size = os.stat(fullpath).st_size

			mime = magic.from_file(fullpath, mime=True)
			logging.info("mime={}".format(mime))
			visible = "image/" in mime
			if (visible == False):
				visible = "text/" in mime
			logging.info("visible={}".format(visible))

			files.append({
				"name": name,
				"size": str(size) + " B",
				"mime": mime,
				"fullname": fullpath,
				"visible": visible
			})

	return render_template("index.html", files=sorted(files, key=lambda k: k["name"].lower()), folders=dirs, meta=meta)


@app.route("/download")
def download():
	filename = request.args.get('filename', default=None, type=str)
	logging.info("{}:filename={}".format(sys._getframe().f_code.co_name, filename))

	if os.path.isfile(filename):
		if os.path.dirname(filename) == UPLOAD_DIR.rstrip("/"):
			return send_file(filename, as_attachment=True)
		else:
			return render_template("no_permission.html")
	else:
		return render_template("not_found.html")
	return None

@app.route("/imageview")
def imageview():
	filename = request.args.get('filename', default=None, type=str)
	logging.info("{}:filename={}".format(sys._getframe().f_code.co_name, filename))

	mime = magic.from_file(filename, mime=True)
	mime = mime.split("/")
	logging.info("mime={}".format(mime))

	if (mime[0] == "image"):
		logging.debug("filename={}".format(filename))
		filename = os.path.basename(filename)
		logging.debug("filename={}".format(filename))
		filename = os.path.join("/uploaded", filename)
		logging.debug("filename={}".format(filename))
		return render_template("view.html", user_image = filename)

	if (mime[0] == "text"):
		contents = ""
		f = open(filename, 'r')
		datalist = f.readlines()
		for data in datalist:
			print("[{}]".format(data.rstrip()))
			contents = contents + data.rstrip() + "<br>"
		return contents

@app.route('/upload_multipart', methods=['POST'])
def upload_multipart():
	print("upload_multipart")
	logging.info("request={}".format(request))
	logging.info("request.files={}".format(request.files))
	dict = request.files.to_dict(flat=False)
	logging.info("dict={}".format(dict))


	'''
	file is werkzeug.datastructures.FileStorage Object.
	This object have these member.
		filename：Uploaded File Name
		name：Field name of Form
		headers：HTTP request header information(header object of flask)
		content_length：content-length of HTTP request
		mimetype：mimetype

	'''

	FileStorage = dict['upfile'][0]
	logging.info("FileStorage={}".format(FileStorage))
	logging.info("FileStorage.filename={}".format(FileStorage.filename))
	logging.info("FileStorage.mimetype={}".format(FileStorage.mimetype))

	filename = FileStorage.filename
	filepath = os.path.join(UPLOAD_DIR, werkzeug.utils.secure_filename(filename))
	#FileStorage.save(filepath)

	try:
		FileStorage.save(filepath)
		responce = {'result':'upload OK'}
		logging.info("{} uploaded {}, saved as {}".format(request.remote_addr, filename, filepath))
	except IOError as e:
		logging.error("Failed to write file due to IOError %s", str(e))
		responce = {'result':'upload FAIL'}

	return json.dumps(responce)

# main
if __name__ == "__main__":
	WSGIRequestHandler.protocol_version = "HTTP/1.1"
	app.run(host='0.0.0.0', port=8080, debug=True)
	#app.run(host='0.0.0.0', port=8080)
