import logging
import random

from flask import Flask, jsonify, make_response, render_template, request
from jinja2.exceptions import TemplateNotFound

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
event_logger = logging.getLogger('event')
logging.getLogger('werkzeug').setLevel(logging.WARNING)

app = Flask(__name__)
global_vars = {
    "verifyResult": "waiting",
    "verifyCode": ""
}

index_tmpl = 'index.tmpl'


@app.route('/api/answer', methods=['GET'])
def answer():
    logger.info("recieve an answer:\n%s", request.query_string.decode("utf-8"))
    body, status = get_resp_body('answer', request)
    logger.info('return ncco:\n%s', body)
    response = make_response(body, status)
    response.content_type = 'application/json'
    return response


@app.route('/api/asr', methods=['POST'])
def asr():
    logger.info("receive an asr:\n%s", request.get_data(as_text=True))
    results = request.json['speech']['results']
    for i, result in enumerate(results):
        text = result['text']
        code = global_vars['verifyCode']
        logger.debug('index %s, text:%s, code: %s', i, text, code)
        if code in text:
            global_vars['verifyResult'] = "pass"
            body, status = get_resp_body(
                'asr-correct', request, context={"code": " ".join(code)})
            logger.info('return ncco:\n%s', body)
            response = make_response(body, status)
            response.content_type = 'application/json'
            return response
    global_vars['verifyResult'] = "failed"
    body, status = get_resp_body(
        'asr-wrong', request, context={"text": results[0]['text']})
    logger.info('return ncco:\n%s', body)
    response = make_response(body, status)
    response.content_type = 'application/json'
    return response


@app.route('/api/login', methods=['POST'])
def login():
    json = request.json
    msisdn = json['msisdn']
    password = json['password']
    code = generate_code()
    response = make_response(
        {"require2fa": True, "2falist": ["voice"], "code": code}, 200)
    response.content_type = 'application/json'
    global_vars['verifyResult'] = "waiting"
    return response


@app.route('/api/queryCode', methods=['GET'])
def query_code():
    return jsonify({"code": global_vars["verifyCode"]})


def generate_code():
    code_list = [1, 4, 5, 6, 9]
    random.shuffle(code_list)
    code = ""
    for i in range(4):
        code = str(code_list[i]) + code
    global_vars['verifyCode'] = code
    logger.info('current code is: %s', code)
    global_vars['verifyResult'] = "waiting"
    return code


@app.route('/api/refreshCode', methods=['POST'])
def refresh_code():
    code = generate_code()
    return jsonify({"code": code})


@app.route('/api/verifyResult', methods=['POST'])
def verify_result():
    return jsonify({"status": global_vars['verifyResult']})


@app.route('/api/event', methods=['POST'])
def event():
    event_logger.info('recieve an event:\n%s', request.get_data(as_text=True))
    return ""


@app.route('/', methods=['GET'])
@app.route('/portal', methods=['GET'])
@app.route('/voiceAuth', methods=['GET'])
def index():
    return render_template(index_tmpl)


def get_resp_body(result, request, context=dict()):
    status = 200
    resp_body_tmpl = '{}.json'.format(result)
    try:
        body = render_template(
            resp_body_tmpl, request=request, context=context)
    except TemplateNotFound:
        body = ""
        status = 404
    return body, status


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
