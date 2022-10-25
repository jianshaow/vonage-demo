# vonage-demo

## local run
~~~ shell
# prepare environment
sudo apt-get install python3-venv
python -m venv --system-site-packages flask
source flask/bin/activate
pip install --upgrade pip
pip install flask
pip install -U flask-cors

# run flask app
python www/app.py
~~~

## run on docker
~~~ shell
export image_ver=0.0.1
docker build -t jianshao/vonage-demo:$image_ver .
docker push jianshao/vonage-demo:$image_ver
docker run -d --name vonage-demo --rm -p 5000:5000 jianshao/vonage-demo:$image_ver
~~~
