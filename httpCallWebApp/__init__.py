import azure.functions as func
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


# @app.route(route="test", methods=["GET"])

@app.route(route="")
def get_chats(req: func.HttpRequest) -> func.HttpResponse:
    # func.HttpResponse("Invalid JSON in request body.", status_code=400)
    test_id = req.params.get("test_id")

    result_json = {"tests": [test_id]}
    return func.HttpResponse(
        json.dumps(result_json, ensure_ascii=False),
        mimetype="application/json",
        charset="utf-8",
        status_code=200
    )

