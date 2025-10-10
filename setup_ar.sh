#!/bin/bash

# AR Setup Helper Script
# Помощник по настройке AR для CyberSec Team

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        CyberSec Team AR - Скрипт быстрой настройки            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода с цветом
print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Проверка Python
print_step "Проверка Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python найден: $PYTHON_VERSION"
else
    print_error "Python3 не найден. Установите Python 3.7 или выше."
    exit 1
fi

# Проверка виртуального окружения
print_step "Проверка виртуального окружения..."
if [ -d ".venv" ]; then
    print_success "Виртуальное окружение найдено"
else
    print_warning "Виртуальное окружение не найдено. Создаём..."
    python3 -m venv .venv
    print_success "Виртуальное окружение создано"
fi

# Активация окружения
print_step "Активация виртуального окружения..."
source .venv/bin/activate
print_success "Окружение активировано"

# Установка зависимостей
print_step "Проверка зависимостей..."
pip install -q -r requirements.txt
print_success "Основные зависимости установлены"

# Установка дополнительных зависимостей для генерации маркеров
print_step "Установка зависимостей для генерации маркеров..."
pip install -q Pillow reportlab
print_success "Pillow и reportlab установлены"

# Создание директории для маркеров
print_step "Создание директории для маркеров..."
mkdir -p static/markers
print_success "Директория static/markers создана"

# Меню выбора действий
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    Выберите действие                           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "1) Генерация AR-маркеров (PNG изображения)"
echo "2) Запуск демо-версии (с маркером Hiro)"
echo "3) Запуск полной версии (требуются .patt файлы)"
echo "4) Запуск с HTTPS (самоподписанный сертификат)"
echo "5) Показать инструкцию по созданию .patt файлов"
echo "6) Проверить наличие всех необходимых файлов"
echo "0) Выход"
echo ""

read -p "Введите номер действия: " choice

case $choice in
    1)
        print_step "Генерация AR-маркеров..."
        python3 generate_markers.py
        echo ""
        print_success "Маркеры сгенерированы!"
        print_warning "Теперь создайте .patt файлы (выберите пункт 5 для инструкции)"
        ;;
    
    2)
        print_step "Запуск демо-версии..."
        echo ""
        print_success "Приложение запущено!"
        echo ""
        print_warning "Откройте в браузере: http://127.0.0.1:3750/team-demo"
        print_warning "Скачайте маркер Hiro: https://raw.githubusercontent.com/AR-js-org/AR.js/master/data/images/hiro.png"
        echo ""
        python3 app.py
        ;;
    
    3)
        print_step "Проверка наличия .patt файлов..."
        PATT_COUNT=$(ls -1 static/markers/*.patt 2>/dev/null | wc -l)
        
        if [ "$PATT_COUNT" -eq 10 ]; then
            print_success "Найдено $PATT_COUNT .patt файлов"
            print_step "Запуск полной версии..."
            echo ""
            print_success "Приложение запущено!"
            print_warning "Откройте в браузере: http://127.0.0.1:3750/team"
            echo ""
            python3 app.py
        else
            print_error "Найдено только $PATT_COUNT из 10 .patt файлов"
            print_warning "Создайте .patt файлы перед запуском полной версии"
            print_warning "Выберите пункт 5 для инструкции"
        fi
        ;;
    
    4)
        print_step "Создание самоподписанного SSL сертификата..."
        
        if [ ! -f "cert.pem" ] || [ ! -f "key.pem" ]; then
            openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=localhost"
            print_success "SSL сертификат создан"
        else
            print_success "SSL сертификат уже существует"
        fi
        
        print_step "Запуск с HTTPS..."
        echo ""
        print_success "Приложение запущено с HTTPS!"
        print_warning "Откройте в браузере: https://127.0.0.1:3750/team-demo"
        print_warning "⚠️  Браузер покажет предупреждение о безопасности - это нормально для самоподписанного сертификата"
        print_warning "Нажмите 'Дополнительно' → 'Продолжить на сайт'"
        echo ""
        
        # Запуск с SSL (требует модификации app.py)
        export USE_SSL=true
        python3 app.py
        ;;
    
    5)
        echo ""
        echo "╔════════════════════════════════════════════════════════════════╗"
        echo "║          Инструкция по созданию .patt файлов                   ║"
        echo "╚════════════════════════════════════════════════════════════════╝"
        echo ""
        echo "Для каждого из 10 маркеров (marker-1.png ... marker-10.png):"
        echo ""
        echo "1. Откройте в браузере:"
        echo "   ${BLUE}https://jeromeetienne.github.io/AR.js/three.js/examples/marker-training/examples/generator.html${NC}"
        echo ""
        echo "2. Нажмите кнопку 'Upload' и выберите marker-X.png"
        echo ""
        echo "3. Оставьте 'Pattern Ratio' на значении 0.5"
        echo ""
        echo "4. Нажмите 'Download Marker' - скачается файл pattern-marker.patt"
        echo ""
        echo "5. Переименуйте его в marker-X.patt (где X - номер маркера)"
        echo ""
        echo "6. Переместите в папку static/markers/"
        echo ""
        echo "7. Повторите для всех 10 маркеров"
        echo ""
        print_success "После создания всех .patt файлов запустите полную версию (пункт 3)"
        echo ""
        ;;
    
    6)
        echo ""
        echo "╔════════════════════════════════════════════════════════════════╗"
        echo "║                Проверка файлов                                 ║"
        echo "╚════════════════════════════════════════════════════════════════╝"
        echo ""
        
        # Проверка PNG маркеров
        print_step "PNG маркеры:"
        PNG_COUNT=$(ls -1 static/markers/*.png 2>/dev/null | wc -l)
        if [ "$PNG_COUNT" -gt 0 ]; then
            print_success "Найдено $PNG_COUNT PNG файлов"
            ls static/markers/*.png 2>/dev/null | while read file; do
                echo "  ✓ $(basename $file)"
            done
        else
            print_error "PNG маркеры не найдены. Запустите генерацию (пункт 1)"
        fi
        
        echo ""
        
        # Проверка .patt файлов
        print_step ".patt файлы:"
        PATT_COUNT=$(ls -1 static/markers/*.patt 2>/dev/null | wc -l)
        if [ "$PATT_COUNT" -eq 10 ]; then
            print_success "Найдено $PATT_COUNT .patt файлов - всё готово! ✅"
            ls static/markers/*.patt 2>/dev/null | while read file; do
                echo "  ✓ $(basename $file)"
            done
        elif [ "$PATT_COUNT" -gt 0 ]; then
            print_warning "Найдено $PATT_COUNT из 10 .patt файлов"
            ls static/markers/*.patt 2>/dev/null | while read file; do
                echo "  ✓ $(basename $file)"
            done
        else
            print_error ".patt файлы не найдены. См. инструкцию (пункт 5)"
        fi
        
        echo ""
        
        # Проверка PDF
        print_step "PDF для печати:"
        if [ -f "static/markers/all_markers_print.pdf" ]; then
            print_success "PDF файл создан"
        else
            print_warning "PDF не найден. Будет создан при генерации маркеров"
        fi
        
        echo ""
        print_success "Проверка завершена"
        ;;
    
    0)
        print_success "Выход"
        exit 0
        ;;
    
    *)
        print_error "Неверный выбор"
        exit 1
        ;;
esac

echo ""
print_success "Готово!"
