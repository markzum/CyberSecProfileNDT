from datetime import datetime, timezone
import os

from flask import Flask, render_template, send_from_directory


TEAM_MEMBERS = [
    {
        "key": "camera",
        "name": "Сергей Александрович",
        "role": "Тимлидер",
        "bio": (
            "Педагог, фотограф, смм-специалист. Работает в Национальном детском "
            "технопарке и Академии образования."
        ),
        "image": "camera.jpg",
        "marker": "camera.patt",
        "text_offset": "-0.28 0.32 0.02",
        "socials": [
            {"label": "Instagram", "url": "https://www.instagram.com/serge.magazine?igsh=NTF3bXhqM3UxN20w"},
            {"label": "Telegram", "url": "https://t.me/leibuk"},
        ],
    },
    {
        "key": "bolt",
        "name": "Эльвира Юрьевна",
        "role": "Тимлидер",
        "bio": "Супер-тимлидер!",
        "image": "bolt.jpg",
        "marker": "bolt.patt",
        "text_offset": "-0.28 0.32 0.02",
        "socials": [
            {"label": "Instagram", "url": "https://www.instagram.com/_lux_loxx"},
        ],
    },
    {
        "key": "sunny",
        "name": "Алина Рожкова",
        "role": "Генеральный стратег",
        "bio": (
            "Самый крутой стратег тактики и по совместительству духовный лидер "
            "информационной безопасности."
        ),
        "image": "sunny.jpg",
        "marker": "sunny.patt",
        "text_offset": "-0.28 0.32 0.02",
        "socials": [
            {"label": "Instagram", "url": "https://www.instagram.com/aliinsse"},
            {"label": "Telegram", "url": "https://t.me/aliinsse"},
        ],
    },
    {
        "key": "check-circle",
        "name": "Владислав Грищенко",
        "role": "Стратег тактики",
        "bio": "Самый крутой стратег тактики и духовный лидер команды.",
        "image": "check-circle.jpg",
        "marker": "check-circle.patt",
        "text_offset": "-0.28 0.32 0.02",
        "socials": [
            {"label": "Instagram", "url": "https://www.instagram.com/grvlad2008"},
            {"label": "Telegram", "url": "https://t.me/v1arr"},
        ],
    },
    {
        "key": "female",
        "name": "Дарья Рожнова",
        "role": "Стратег кодекса",
        "bio": (
            "Девочка из Тюмени, любит вязать и кошек, прогает, изучает всякое "
            "интересное и живёт свою лучшую жизнь (пытается по крайней мере...)."
        ),
        "image": "female.jpg",
        "marker": "female.patt",
        "text_offset": "-0.28 0.32 0.02",
        "socials": [
            {"label": "VK", "url": "https://vk.com/dmeowd"},
            {"label": "Telegram", "url": "https://t.me/dmeowd"},
        ],
    },
    {
        "key": "person-shield",
        "name": "Матвей Дайнеко",
        "role": "Стратег видео",
        "bio": "Нам природа дарит смысл, мы сполна его берём.",
        "image": "person-shield.jpg",
        "marker": "person-shield.patt",
        "text_offset": "-0.28 0.32 0.02",
        "socials": [],
    },
    {
        "key": "sync-desktop",
        "name": "Максим Палыч Парипа",
        "role": "Стратег финансов",
        "bio": (
            "Белорусский учёный, общественный деятель и предприниматель, известный "
            "достижениями в ИТ, активной гражданской позицией и вкладом в молодёжную "
            "политику Беларуси."
        ),
        "image": "sync-desktop.jpg",
        "marker": "sync-desktop.patt",
        "text_offset": "-0.28 0.32 0.02",
        "socials": [
            {"label": "Telegram", "url": "https://t.me/maksim_paripa"},
        ],
    },
    {
        "key": "sync-saved-locally",
        "name": "Иван Дерябин",
        "role": "Стратег спорта",
        "bio": "*Засекречен*",
        "image": "sync-saved-locally.jpg",
        "marker": "sync-saved-locally.patt",
        "text_offset": "-0.28 0.32 0.02",
        "socials": [],
    },
    {
        "key": "visibility-lock",
        "name": "Егор Фалько",
        "role": "Стратег досуга",
        "bio": "Лудоман, есть сестра, прошёл в технопарк с первого раза, ест чисто сахар всухую.",
        "image": "visibility-lock.jpg",
        "marker": "visibility-lock.patt",
        "text_offset": "-0.28 0.32 0.02",
        "socials": [
            {"label": "Telegram", "url": "https://t.me/bikhk"},
        ],
    },
    {
        "key": "settings-accessibility",
        "name": "Дмитрий Ермоленко",
        "role": "Стратег звука",
        "bio": "404. Описание не найдено.",
        "image": "settings-accessibility.jpg",
        "marker": "settings-accessibility.patt",
        "text_offset": "-0.28 0.32 0.02",
        "socials": [],
    },
    {
        "key": "zoom-in",
        "name": "Добрыня Иванов",
        "role": "Стратег информации",
        "bio": "Ббрррр патапим тралалела тралалла.",
        "image": "zoom-in.jpg",
        "marker": "zoom-in.patt",
        "text_offset": "-0.28 0.32 0.02",
        "socials": [
            {"label": "Telegram", "url": "https://t.me/Dobriva_Ivanov"},
        ],
    },
    {
        "key": "memory",
        "name": "Марк Мещеряков",
        "role": "Стратег творчества",
        "bio": "Гений, миллиа... Fullstack-, Python-, Android-разработчик, хацкер.",
        "image": "memory.jpg",
        "marker": "memory.patt",
        "text_offset": "-0.22 0.28 0.02",
        "socials": [
            {"label": "Portfolio", "url": "https://schoolzum.ru/markzum"},
            {"label": "GitHub", "url": "https://github.com/markzum"},
            {"label": "Telegram", "url": "https://t.me/markzum"},
        ],
    },
]


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
        return render_template("team_overview.html", team_members=TEAM_MEMBERS)

    @app.route("/team/ar")
    def team_ar():
        return render_template("team.html", team_members=TEAM_MEMBERS)

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
