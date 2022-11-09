from http import HTTPStatus

from apiflask import APIBlueprint, abort
from auth_app.social.providers import GoogleOAuth
from auth_app.social.schemas import ProviderIn, CallbackOut
from flask import redirect, request, jsonify

from auth_app.tracing import loging, trace

blueprint = APIBlueprint("social", __name__, url_prefix="/auth/social")


@blueprint.get("/login")
@blueprint.input(ProviderIn, location="query")
@trace
@loging
def login(query):
    if query["provider"] == "google":
        request_uri = GoogleOAuth().login(request)
    else:
        return abort(HTTPStatus.BAD_REQUEST, "Not valid provide")

    return redirect(request_uri)


@blueprint.get("/login/callback")
@blueprint.input(ProviderIn, location="query")
@blueprint.output(CallbackOut)
@trace
@loging
def callback(query):
    if query["provider"] == "google":
        tokens = GoogleOAuth().callback(request)
        if not tokens:
            return abort(HTTPStatus.BAD_REQUEST, message="User email not available or not verified by Google.")
        return jsonify(tokens)
    return abort(HTTPStatus.BAD_REQUEST, "Not valid provider")
