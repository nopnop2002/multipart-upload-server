# -*- coding: utf-8 -*-
import os
import werkzeug
from datetime import datetime
from flask import Flask, request, make_response, jsonify
from werkzeug.serving import WSGIRequestHandler
import logging
import json

# flask
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


# ex) set UPLOAD_DIR_PATH=C:/tmp/flaskUploadDir
UPLOAD_DIR = os.getenv("UPLOAD_DIR_PATH")
logging.info("UPLOAD_DIR={}".format(UPLOAD_DIR))
if (UPLOAD_DIR == None):
    UPLOAD_DIR = os.path.join(os.getcwd(), "UPLOADED")
    logging.info("UPLOAD_DIR={}".format(UPLOAD_DIR))

if (os.path.exists(UPLOAD_DIR) == False):
    logging.warning("UPLOAD_DIR [{}] not found. Create this".format(UPLOAD_DIR))
    os.mkdir(UPLOAD_DIR)

@app.route("/")
def hello():
	print("hello")
	return "Hello World!"

@app.route('/upload_multipart', methods=['POST'])
def upload_multipart():
	logging.info("request={}".format(request))
	logging.info("request.files={}".format(request.files))
	dict = request.files.to_dict(flat=False)
	logging.info("dict={}".format(dict))

	"""
	if 'uploadFile' not in request.files:
		return make_response(jsonify({'result':'uploadFile is required'}))

	file = request.files['uploadFile']
	"""

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
	#logging.info("app.url_map={}".format(app.url_map))
	app.run(host='0.0.0.0', port=8080, debug=True)
