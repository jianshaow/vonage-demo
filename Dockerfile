FROM python:alpine

RUN pip install --upgrade pip
RUN pip install flask

COPY www /www

EXPOSE 5000

CMD [ "python", "/www/app.py" ]
