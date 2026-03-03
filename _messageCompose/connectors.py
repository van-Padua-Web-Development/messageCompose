from flask_limiter import Limiter
from flask import session, request
import json, os

def load_translations(folder="translations"):
    translations = {}

    base_path = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(base_path, folder)
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            module = filename[:-5]
            with open(os.path.join(folder_path, filename), encoding="utf-8") as f:
                translations[module] = json.load(f)
    return translations

limiter = Limiter(
    key_func=lambda: session.get('sid', request.remote_addr),
    default_limits=[]  # default empty, define per route
)


# oauth = OAuth()

# def oauth_register():
#     oauth.register(
#         name="google",
#         client_id=os.environ["GOOGLE_CLIENT_ID"],
#         client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
#         server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
#         client_kwargs={"scope": "openid email profile"}
#     )

    # oauth.register(
    #     name="facebook",
    #     client_id=os.environ["FACEBOOK_APP_ID"],
    #     client_secret=os.environ["FACEBOOK_APP_SECRET"],
    #     access_token_url="https://graph.facebook.com/v12.0/oauth/access_token",
    #     authorize_url="https://www.facebook.com/v12.0/dialog/oauth",
    #     api_base_url="https://graph.facebook.com/v12.0/",
    #     client_kwargs={"scope": "email"}
    # )