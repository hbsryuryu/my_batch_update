import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    test_id = req.params.get("test_id")

    result_json = {"tests": [test_id]}
    return func.HttpResponse(
        json.dumps(result_json, ensure_ascii=False),
        mimetype="application/json",
        charset="utf-8",
        status_code=200
    )

