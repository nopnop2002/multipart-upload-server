# multipart-upload-server
multipart/form-data upload server for Flask &amp; Tornado

You can choose the one you like.

# Using Tornado

## Install Tornado
```
sudo apt install python3-pip python3-setuptools python3-magic
python3 -m pip install -U pip
python3 -m pip install -U wheel
python3 -m pip install Werkzeug
python3 -m pip install tornado
```

## Start WEB Server using Tornado
```
git clone https://github.com/nopnop2002/multipart-upload-server
cd multipart-upload-server/tornado
python3 upload.py
```

## Upload file using curl
```
curl -X POST -F upfile=@$HOME/multipart-upload-server/tornado/tornado-web-service.jpg http://localhost:8080/upload_multipart

ls -l $HOME/multipart-upload-server/tornado/uploaded/
-rw-rw-r-- 1 nop nop 13189  5月 21 08:58 tornado-web-service.jpg
```

---

# Using Flask

## Install Flask
```
sudo apt install python3-pip python3-setuptools python3-magic
python3 -m pip install -U pip
python3 -m pip install -U wheel
python3 -m pip install -U Werkzeug
python3 -m pip install flask
```

## Start WEB Server using Flask
```
git clone https://github.com/nopnop2002/multipart-upload-server
cd multipart-upload-server/flask
python3 upload.py
```

## Upload file using curl
```
curl -X POST -F upfile=@$HOME/multipart-upload-server/flask/Flask_logo.png http://localhost:8080/upload_multipart

ls -l $HOME/multipart-upload-server/flask/uploaded/
-rw-rw-r-- 1 nop nop 13189  5月 21 08:58 Flask_logo.png
```

---

# View file
![multipart-upload-server-1](https://user-images.githubusercontent.com/6020549/119225534-4af78000-bb3f-11eb-83fc-d3c93b31e4eb.jpg)

![multipart-upload-server-2](https://user-images.githubusercontent.com/6020549/119225542-5054ca80-bb3f-11eb-95a3-f558e606f68c.jpg)

![multipart-upload-server-3](https://user-images.githubusercontent.com/6020549/119225537-4b901680-bb3f-11eb-9f0c-e009b5f6c56d.jpg)

