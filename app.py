from datetime import datetime, timezone
import os

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

    @app.route("/team-demo")
    def team_demo():
        return render_template("team-demo.html")

    return app


app = create_app()


if __name__ == "__main__":
    # Проверяем, нужен ли SSL
    use_ssl = os.environ.get('USE_SSL', '').lower() == 'true'
    
    if use_ssl:
        # Запуск с SSL
        if os.path.exists('cert.pem') and os.path.exists('key.pem'):
            print("🔒 Запуск с HTTPS...")
            app.run(host="127.0.0.1", port=3750, debug=True, 
                   ssl_context=('cert.pem', 'key.pem'))
        else:
            print("❌ SSL сертификаты не найдены. Создайте их командой:")
            print("openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365")
    else:
        # Обычный запуск
        print("🚀 Запуск сервера...")
        print("📱 Демо: http://127.0.0.1:3750/team-demo")
        print("🎯 Полная версия: http://127.0.0.1:3750/team")
        app.run(host="127.0.0.1", port=3750, debug=True)
