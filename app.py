from datetime import datetime, timezone

from flask import Flask, render_template


def create_app() -> Flask:
    """Application factory for the CyberSec profile site."""
    app = Flask(__name__)

    @app.context_processor
    def inject_globals():
        return {"current_year": datetime.now(timezone.utc).year}

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/intro")
    def intro():
        return render_template("intro.html")

    @app.route("/team")
    def team():
        return render_template("team.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
