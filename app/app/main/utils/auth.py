from flask import abort, jsonify, request
from loguru import logger

from ..config import CONFIG


def login_required(func):
    def inner():
        if request.headers.get("token") != CONFIG.AUTH_TOKEN:
            abort_json(401, "UNAUTHORIZED", "authentication header invalid")
        return func()

    return inner


def abort_json(status_code=400, error="", message="", status="fail"):
    response = jsonify(
        {
            "status": status,
            "message": message,
            "error": error,
            "status_code": status_code,
        }
    )

    logger.error(f"| {error} || {message} || {status_code} |")
    response.status_code = status_code
    response.headers["Access-Control-Allow-Origin"] = "*"
    abort(response)


def make_response(data="", status_code=200, error="", message="", status="success"):
    response = jsonify(
        {
            "data": data,
            "status": status,
            "message": message,
            "error": error,
            "status_code": status_code,
        }
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    logger.info(f"| {error} || {message} || {status_code} |")

    return response
