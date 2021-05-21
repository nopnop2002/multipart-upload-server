# -*- coding: utf-8 -*-
import os
import werkzeug
from datetime import datetime
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
import json

from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int)

# ex) set UPLOAD_DIR_PATH=C:/tmp/flaskUploadDir
UPLOAD_DIR = os.getenv("UPLOAD_DIR_PATH")
logging.info("UPLOAD_DIR={}".format(UPLOAD_DIR))
if (UPLOAD_DIR == None):
	UPLOAD_DIR = os.path.join(os.getcwd(), "UPLOADED")
	logging.info("UPLOAD_DIR={}".format(UPLOAD_DIR))

if (os.path.exists(UPLOAD_DIR) == False):
	logging.warning("UPLOAD_DIR [{}] not found. Create this".format(UPLOAD_DIR))
	os.mkdir(UPLOAD_DIR)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		print("IndexHandler:get")
		self.write("Hello World")

class UploadHandler(tornado.web.RequestHandler):
	def post(self):
		logging.info("UploadHandler:post")
		logging.info("self.request={}".format(self.request))
		#print("self.request.files={}".format(self.request.files))

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
	return tornado.web.Application([
		(r"/", IndexHandler),
		(r"/upload_multipart", UploadHandler),
	],debug=True)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = make_app()
	#app = tornado.web.Application(handlers=[(r"/", IndexHandler)],debug=True)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()


