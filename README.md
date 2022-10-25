# vonage-demo

## local run
~~~ shell
# prepare environment
sudo apt-get install python3-venv
python -m venv --system-site-packages flask
source flask/bin/activate
pip install --upgrade pip
pip install flask

# run flask app
python www/app.py
~~~

## run on docker
~~~ shell
export image_ver=0.0.1
docker build -t jianshao/vonage-demo:$image_ver .
docker push jianshao/vonage-demo:$image_ver
docker run -d --name vonage-demo --rm -p 5000:5000 jianshao/vonage-demo:$image_ver
docker stop vonage-demo
~~~

## test wiht curl
~~~ shell
curl http://127.0.0.1:5000/api/answer?uuid=1234
curl http://127.0.0.1:5000/api/asr -H 'Content-Type: application/json' -d '{"speech":{"results":[{"text":"1234"}]}}'
~~~

## deploy on k8s
~~~ shell
kubectl apply -f manifests/deploy.yaml
kubectl apply -f manifests/ingress.yaml
~~~