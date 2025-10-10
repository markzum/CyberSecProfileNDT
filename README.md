# CyberSec Profile Showcase

Визитка профиля «Информационная безопасность» для Национального детского технопарка Беларуси.

## Возможности

- 🌐 Flask-бэкенд с маршрутами `/`, `/intro`, `/team`, `/team-demo`.
- 🖥️ Главная страница в стиле «киберпанк» с приветствием и быстрыми ссылками.
- 🎬 Страница «Интро» с видеопрезентацией программы.
- 🕶️ **AR Дополненная реальность**: Страница команды с интерактивными 3D-карточками через AR.js
- 📱 Оптимизация под мобильные устройства, адаптивная сетка и полноэкранный режим камеры.
- 🎯 **10 уникальных AR-маркеров** для каждого члена команды

## Быстрый старт

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Приложение будет доступно по адресу <http://127.0.0.1:5000>.

## 🎯 AR-функциональность

### Быстрая демонстрация (без настройки)

1. Запустите приложение
2. Откройте <http://127.0.0.1:3750/team-demo>
3. Скачайте маркер Hiro: https://raw.githubusercontent.com/AR-js-org/AR.js/master/data/images/hiro.png
4. Наведите камеру на маркер - увидите AR-карточку!

### Полная настройка с 10 уникальными маркерами

**Для полноценного AR-опыта с 10 членами команды:**

1. **Установите зависимости для генерации маркеров:**
   ```bash
   pip install Pillow reportlab
   ```

2. **Сгенерируйте AR-маркеры:**
   ```bash
   python generate_markers.py
   ```
   Это создаст PNG изображения маркеров в `static/markers/`

3. **Создайте .patt файлы:**
   - Для каждого `marker-X.png` (где X от 1 до 10):
   - Откройте: https://jeromeetienne.github.io/AR.js/three.js/examples/marker-training/examples/generator.html
   - Загрузите изображение `marker-X.png`
   - Скачайте сгенерированный `.patt` файл
   - Переименуйте в `marker-X.patt` и сохраните в `static/markers/`

4. **Распечатайте маркеры:**
   - Используйте файлы `marker-X-highres.png` или `all_markers_print.pdf`
   - Рекомендуемый размер: 15x15 см
   - Повесьте на стену в штаб-квартире

5. **Запустите с HTTPS** (обязательно для доступа к камере):
   ```bash
   # Вариант 1: Используйте ngrok
   ngrok http 3750
   
   # Вариант 2: SSL сертификат
   openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
   # Затем измените app.py для использования SSL
   ```

6. **Откройте на телефоне** и наведите на маркеры!

**📚 Подробная инструкция:** См. [AR_SETUP_GUIDE.md](AR_SETUP_GUIDE.md)

## AR-маркеры

Для трёх членов команды используются barcode-маркеры с номерами 5, 12 и 23. Распечатывайте соответствующие маркеры из [официального генератора AR.js](https://jeromeetienne.github.io/AR.js/three.js/examples/marker-training/examples/generator.html), выбрав режим `Barcode` и указав нужное значение.

## Тесты

```bash
pytest
```

## Структура проекта

```
app.py                 # Flask-приложение
requirements.txt       # зависимости
static/
  css/styles.css       # глобальные стили
  js/main.js           # общий JS
  js/team-ar.js        # логика AR-сцены
templates/
  base.html            # базовый шаблон
  index.html           # главная
  intro.html           # страница интро
  team.html            # команда + AR
```

## Замечания по развёртыванию

- Для корректной работы AR на мобильных устройствах рекомендуется запускать сайт по HTTPS (например, через reverse proxy или GitHub Pages + ngrok).
- AR.js требует разрешение на использование камеры. При первом запуске браузер запросит доступ.
