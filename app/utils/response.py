from flask import jsonify

def success_response(data=None, code=200):
    response_body = {
        'code': code,
        'result': {
            'data': data
        }
    }
    return jsonify(response_body), code

def error_response(message, code=400):
    response_body = {
        'response': {
            'message': message
        }
    }
    return jsonify(response_body), code
