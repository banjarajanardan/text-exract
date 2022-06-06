import os

from flask import Blueprint, jsonify, request
from tempfile import TemporaryDirectory

from ..config import CONFIG
from ..services.text_extractor import TextExtractor
from ..utils.auth import abort_json, make_response, login_required

document_blueprint = Blueprint("document", __name__)


@document_blueprint.route("/extract/text/", methods=["POST"])
@login_required
def extract_text():
    if "application/json" in request.headers.get("Content-Type", ""):
        text = request.json.get("text")
    elif "multipart/form-data" in request.headers.get("Content-Type", ""):
        files = request.files
        if not files:
            abort_json(400, "FILE_MISSING", "file required on form data")
        files = files.getlist("files")
        files = [(f.filename, f) for f in files]
        temp_dir = TemporaryDirectory()
        tmp_dir = temp_dir.name

        supported_files = CONFIG.SUPPORTED_FILES
        text = []
        for file_name, file_body in files:
            _, ext = os.path.splitext(file_name)

            if ext not in supported_files:
                abort_json(
                    400,
                    "UNSUPPORTED_FILE",
                    f"only {', '.join(supported_files)} types supported",
                )
            file_path = os.path.join(tmp_dir, file_name)
            file_body.save(file_path)
            extractor = TextExtractor(file_path)
            file_text = extractor.extract()
            text.append(file_text)
        text = "\n".join(text)

    else:
        abort_json(
            400,
            "INVALID_REQUEST",
            "content type can be mulipart/form-data or application/json only",
        )
    res = make_response(text)
    return res, 200


@document_blueprint.route("/health/", methods=["GET"])
def health():
    health_status = {
        "status": "success",
        "status_code": 200,
        "message": "successful request",
    }
    return make_response(health_status)
