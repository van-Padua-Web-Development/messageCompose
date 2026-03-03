import os
from flask import Flask, g, request, redirect, abort, session
from datetime import timedelta
from .connectors import load_translations, limiter 
# from _messageCompose.models.user import User
# ------------------------------
# Flask App Factory
# ------------------------------
def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    # ------------------------------
    # App Configuration settings
    # ------------------------------
    app.config.update(
    SECRET_KEY=os.getenv('FLASK_SECRET_KEY'),
    PERMANENT_SESSION_LIFETIME=timedelta(days=1),
    REMEMBER_COOKIE_DURATION=timedelta(days=30),
    REMEMBER_COOKIE_SECURE=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_SAMESITE='Lax'
)
    # ------------------------------
    # Flask Login Manager
    # ------------------------------

    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(user_id)
    
    # # 1️⃣ Initialize OAuth ONCE
    # oauth.init_app(app)

    # # 2️⃣ Register providers ONCE
    # oauth_register()

    # ------------------------------
    # Blueprint Routes
    # ------------------------------

    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    # from .auth import auth_bp
    # app.register_blueprint(auth_bp)

    # from .routes.seo import seo_bp
    # app.register_blueprint(seo_bp)

    # from .routes.honeypot import honeypot_bp
    # app.register_blueprint(honeypot_bp)

    from .api.v1 import api_bp
    app.register_blueprint(api_bp)

    # ------------------------------
    # Language settings
    # ------------------------------
    translations = load_translations()

    @app.context_processor
    def inject_helpers():
        # make t() available in templates
        def t(module, key, lang):
            return translations.get(module, {}).get(key, {}).get(lang, key)
        return {"t": t}
    
    @app.before_request
    def set_language():
        lang = request.args.get("lang") or request.cookies.get("lang")
        lang = lang or request.accept_languages.best_match(
            ["nl", "en", "fr", "de", "it", "es", "da", "sv", "no"]
        ) or "nl"
        g.lang = lang
        request.lang = lang

    # Ensure language prefix
    @app.before_request
    def ensure_lang_prefix():
        # Paths to skip
        SKIP_PATHS = [
            "/static/",
            "/api/",
            "/auth/",
            "/sitemap.xml",
            "/robots.txt",
            "/wp-login.php",
            "/phpmyadmin",
            "/wp-admin/setup-config.php",
        ]
        SUPPORTED_LANGS = ["nl", "en", "fr", "de", "it", "es", "da", "sv", "no"]

        # Skip if path matches any skip path
        if any(request.path.startswith(p) for p in SKIP_PATHS):
            print("skip path matched")
            return

        # Skip already prefixed URLs
        if any(request.path.startswith(f"/{l}/") for l in SUPPORTED_LANGS):
            return

        # Redirect to language-prefixed URL
        lang = getattr(g, "lang", "nl")
        redirect_path = f"/{lang}{request.path}" if request.path != "/" else f"/{lang}/"
        return redirect(redirect_path, code=301)

    # ------------------------------
    # Hotlinking fixing
    # ------------------------------

#    # @app.before_request
#     def prevent_hotlinking():
#         ALLOWED_DOMAINS = ["vpwd.nl", "www.vpwd.nl"]
#         WHITELIST_USER_AGENTS = ["Googlebot", "Googlebot-Image", "WhatsApp", "Bingbot", "Slackbot", "Discordbot"]
# 
#         referer = request.headers.get("Referer")
#         user_agent = request.headers.get("User-Agent", "")
#         # Only intercept static files
#         if not request.path.startswith("/static/"):
#             return
#         
#         # Exclude sitemap.xml and robots.txt (they are not static assets)
#         if request.path in ["/sitemap.xml", "/robots.txt"]:
#             return
# 
#         referer = request.headers.get("Referer")
#         if (
#             (not referer or not any(domain in referer for domain in ALLOWED_DOMAINS))
#             and not any(bot.lower() in user_agent.lower() for bot in WHITELIST_USER_AGENTS)
#         ):
#             abort(403)  # Forbidden 
    # ------------------------------
    # Rate Limiting
    # ------------------------------
    @app.before_request
    def ensure_session():
        if 'sid' not in session:
            import uuid
            session['sid'] = str(uuid.uuid4())

    limiter.init_app(app)
    # ------------------------------
    # MySQL Teardown
    # ------------------------------

    # @app.teardown_appcontext
    # def close_connector(exception=None):
    #     db.session.remove()


    # ------------------------------
    # End Return
    # ------------------------------

    return app