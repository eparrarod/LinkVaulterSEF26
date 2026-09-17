from __future__ import annotations

from flask import Flask, jsonify, redirect, render_template, request, url_for

from .analytics import count_active, favorite_rate
from .models import new_link, next_link_id, normalize_tags, normalize_title, normalize_url
from .search import active_links, favorites_first, search_text
from .validation import is_nonblank_title, is_safe_url, is_unique_url


SEED_LINKS = [
    {"id": 1, "title": "Python Documentation", "url": "https://docs.python.org/3/", "tags": ["python", "docs"], "favorite": True, "archived": False, "visits": 8, "created_at": "2026-09-14T09:00:00+00:00"},
    {"id": 2, "title": "Flask Documentation", "url": "https://flask.palletsprojects.com/", "tags": ["python", "web"], "favorite": False, "archived": False, "visits": 4, "created_at": "2026-09-15T09:00:00+00:00"},
    {"id": 3, "title": "Old Course Link", "url": "https://example.com/archive", "tags": ["course"], "favorite": False, "archived": True, "visits": 1, "created_at": "2026-09-01T09:00:00+00:00"},
]


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)
    app.config.update(TESTING=testing, SECRET_KEY="development-only")
    app.config["LINKS"] = [dict(item, tags=list(item["tags"])) for item in SEED_LINKS]

    @app.get("/")
    def index():
        links = active_links(app.config["LINKS"])
        query = request.args.get("q", "")
        if query:
            links = search_text(links, query)
        links = favorites_first(links)
        return render_template(
            "index.html",
            links=links,
            query=query,
            active_count=count_active(app.config["LINKS"]),
            favorite_rate=favorite_rate(active_links(app.config["LINKS"])),
        )

    @app.post("/links")
    def add_link():
        title = request.form.get("title", "")
        url = request.form.get("url", "")
        tags = request.form.get("tags", "").split(",")
        if not is_nonblank_title(title) or not is_safe_url(url):
            return "Invalid title or URL", 400
        if not is_unique_url(url, app.config["LINKS"]):
            return "URL already saved", 409
        item = new_link(
            next_link_id(app.config["LINKS"]),
            normalize_title(title),
            normalize_url(url),
            normalize_tags(tags),
        )
        app.config["LINKS"].append(item)
        return redirect(url_for("index"))

    @app.post("/links/<int:link_id>/favorite")
    def toggle_favorite(link_id: int):
        item = next((x for x in app.config["LINKS"] if x["id"] == link_id), None)
        if item is None:
            return "Link not found", 404
        item["favorite"] = not item["favorite"]
        return redirect(url_for("index"))

    @app.get("/api/links")
    def api_links():
        return jsonify(app.config["LINKS"])

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    create_app().run(debug=True)

