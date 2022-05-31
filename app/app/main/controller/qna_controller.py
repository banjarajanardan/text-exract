from flask import Blueprint, request
from json.decoder import JSONDecodeError

from ..config import CONFIG
from ..utils.auth import abort_json, login_required, make_response
from ..utils.errors import ServiceUnavailable
from ..utils.utils import send_post_request

qna_blueprint = Blueprint("qna", __name__)


@qna_blueprint.route("/find/answers/", methods=["POST"])
@login_required
def get_answer():
    if "application/json" in request.headers.get("Content-Type", ""):
        text = request.json.get("text", "")
        questions = request.json.get("query", "")
        delimiter = request.json.get("delimiter", "\n")

        if not (text and questions):
            abort_json(400, "MISSING_INPUT", "text and query are required in json body")

        api_url = CONFIG.QNA_API
        questions = questions.split(delimiter)
        json_body = {"inputs": {"context": text}}
        answers = []
        for question in questions:
            json_body["inputs"]["question"] = question
            try:
                r = send_post_request(api_url, {}, json_body)
                answers.append(r.json())
            except (ServiceUnavailable, JSONDecodeError):
                answers.append({"answer": "", "start": 0, "end": 0, "score": 0})

    else:
        abort_json(
            400,
            "INVALID_REQUEST",
            "content type can be mulipart/form-data or application/json only",
        )

    res = make_response(answers)
    return res, 200
