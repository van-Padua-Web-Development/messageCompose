from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__, url_prefix='/<lang>')

@main_bp.route('/')
def home(lang):
    return render_template(f"/main.html", lang=lang)

