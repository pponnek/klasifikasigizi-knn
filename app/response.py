from flask import jsonify, make_response

def success_response(values, message):
    res = {
        'status': 'success',
        'data': values,
        'message': message
    }
    return make_response(jsonify(res), 200)

def error_response(values, message):
    res = {
        'status': 'error',
        'data': values,
        'message': message
    }
    return make_response(jsonify(res), 400)