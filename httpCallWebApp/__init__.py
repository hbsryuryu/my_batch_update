import azure.functions as func
import logging
import os
import json
import datetime
import uuid

from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery

from openai import AzureOpenAI
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column,Integer, String, Boolean, DateTime, Text, ForeignKey, JSON, inspect
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# .env ファイルの読み込み
load_dotenv(override=True)



@app.route(route="test", methods=["GET"])
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

