from datetime import datetime, timezone
import os

from flask import Flask, render_template, send_from_directory


def create_app() -> Flask:
    """Application factory for the CyberSec profile site."""
    app = Flask(__name__)

    @app.context_processor
    def inject_globals():
        return {"current_year": datetime.now(timezone.utc).year}

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/presentation")
    def presentation():
        return render_template("presentation.html")

    @app.route("/trailer")
    def trailer():
        return render_template("trailer.html")

    @app.route("/team")
    def team():
        return render_template("team.html")

    @app.route('/big_files/<path:filename>')
    def big_files(filename):
        return send_from_directory('big_files', filename)

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
        # print("🚀 Запуск сервера...")
        # print("🎯 Полная версия: http://127.0.0.1:3750/team")
        app.run(host="127.0.0.1", port=3750, debug=False)
