# -*- coding: utf-8 -*-
import os
import sys
import werkzeug
from datetime import datetime
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
import json
import magic
import urllib

from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int)

UPLOAD_DIR = os.path.join(os.getcwd(), "uploaded")
logging.info("UPLOAD_DIR={}".format(UPLOAD_DIR))
if (os.path.exists(UPLOAD_DIR) == False):
	logging.warning("UPLOAD_DIR [{}] not found. Create this".format(UPLOAD_DIR))
	os.mkdir(UPLOAD_DIR)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		logging.info("IndexHandler:get")
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

		self.render("index.html", files=sorted(files, key=lambda k: k["name"].lower()), folders=dirs, meta=meta)
		#self.write("Hello World")

class DownloadHandler(tornado.web.RequestHandler):
	def get(self):
		filename = self.get_argument('filename', default=None)
		logging.info("{}:filename={}".format(sys._getframe().f_code.co_name, filename))
		if os.path.isfile(filename):
			if os.path.dirname(filename) == UPLOAD_DIR.rstrip("/"):
				self.set_header('Content-Type', 'application/octet-stream')
				self.set_header('Content-Disposition', 'attachment; filename=' + os.path.basename(filename))
				with open(filename, 'rb') as f:
					while True:
						data = f.read(4096)
						if not data: break
						self.write(data)
				self.finish()
			else:
				return render_template("no_permission.html")
		else:
			return render_template("not_found.html")

class ImageviewHandler(tornado.web.RequestHandler):
	def get(self):
		filename = self.get_argument('filename', default=None)
		logging.info("{}:filename={}".format(sys._getframe().f_code.co_name, filename))
		rotate = self.get_argument('rotate', default=0)
		logging.info("{}:rotate={}{}".format(sys._getframe().f_code.co_name, rotate, type(rotate)))
		if (type(rotate) is str): 
			rotate = int(rotate)
			logging.info("{}:rotate={}{}".format(sys._getframe().f_code.co_name, rotate, type(rotate)))

		mime = magic.from_file(filename, mime=True)
		mime = mime.split("/")
		logging.info("mime={}".format(mime))

		if (mime[0] == "image"):
			logging.info("filename={}".format(filename))
			filename = os.path.basename(filename)
			logging.info("filename={}".format(filename))
			filename = os.path.join("/uploaded", filename)
			logging.info("filename={}".format(filename))
			self.render("view.html", user_image = filename, rotate=rotate)

		if (mime[0] == "text"):
			contents = ""
			f = open(filename, 'r')
			datalist = f.readlines()
			for data in datalist:
				logging.debug("[{}]".format(data.rstrip()))
				contents = contents + data.rstrip() + "<br>"
			self.write(contents)

class UploadHandler(tornado.web.RequestHandler):
	def post(self):
		logging.info("UploadHandler:post")
		logging.info("self.request={}".format(self.request))

		fileinfo = self.request.files['upfile'][0]
		#logging.info("fileinfo={}".format(fileinfo))
		filename = fileinfo['filename'] 
		body = fileinfo['body'] 
		logging.info("filename={}".format(filename))
		filepath = os.path.join(UPLOAD_DIR, werkzeug.utils.secure_filename(filename))
		logging.info("filepath={}".format(filepath))

		try:
			f = open(filepath, "wb")
			f.write(body)
			f.close()
			logging.info("{} uploaded {}, saved as {}".format(self.request.remote_ip, filename, filepath))
			responce = {"result": "upload OK"}
		except IOError as e:
			logging.error("Failed to write file due to IOError %s", str(e))
			responce = {"result": "upload FAIL"}

		self.write(responce)

def make_app():
	settings = {
	"static_path": os.path.join(os.getcwd(), "uploaded"),
	"static_url_prefix": "/uploaded/",
	}
	return tornado.web.Application(
		handlers=[
		(r"/", IndexHandler),
		(r"/download", DownloadHandler),
		(r"/imageview", ImageviewHandler),
		(r"/upload_multipart", UploadHandler),
		],
		template_path=os.path.join(os.getcwd(), "templates"),
		#static_path=os.path.join(os.getcwd(), "statics"),
		**settings,
		debug=True)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = make_app()
	#app = tornado.web.Application(handlers=[(r"/", IndexHandler)],debug=True)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()


