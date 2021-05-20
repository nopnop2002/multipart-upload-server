# multipart-upload-server
multipart/form-data upload server for Flask &amp; Tornado

You can choose the one you like.   

# Using Tornado

## Install Tornado
```
sudo apt install python-pip python-setuptools
python -m pip install -U pip
python -m pip install -U wheel
python -m pip install tornado
```

## Start WEB Server using Tornado
```
git clonse https://github.com/nopnop2002/multipart-upload-server
cd multipart-upload-server/tornado
python upload.py
```

## Upload file using curl
```
curl -X POST -F upfile=@tornado/tornado-web-service.jpg http://localhost:8080/upload_multipart

ls -l tornado/UPLOADED/
-rw-rw-r-- 1 nop nop 13189  5月 21 08:58 tornado-web-service.jpg
```

---

# Using Flask

## Install Flask
```
sudo apt install python-pip python-setuptools
python -m pip install -U pip
python -m pip install -U wheel
python -m pip install flask
```

## Start WEB Server using Flask
```
git clonse https://github.com/nopnop2002/multipart-upload-server
cd multipart-upload-server/flask
python upload.py
```

