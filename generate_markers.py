"""
Генератор AR-маркеров для команды
Создает 10 уникальных AR-маркеров с логотипами для каждого члена команды
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_marker_pattern(number, icon_name, color, size=512):
    """
    Создает уникальный паттерн для AR-маркера
    
    Args:
        number: номер маркера (1-10)
        icon_name: имя иконки/символа
        color: цвет маркера (RGB tuple)
        size: размер изображения в пикселях
    """
    # Создаем изображение
    img = Image.new('RGB', (size, size), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    
    # Размеры
    border_width = size // 8  # 12.5% границы
    inner_size = size - 2 * border_width
    
    # Черная рамка
    draw.rectangle(
        [0, 0, size-1, size-1],
        outline=(0, 0, 0),
        width=border_width
    )
    
    # Белая внутренняя область
    draw.rectangle(
        [border_width, border_width, size-border_width, size-border_width],
        fill=(255, 255, 255)
    )
    
    # Цветной квадрат в центре
    center_size = inner_size // 2
    center_x = size // 2 - center_size // 2
    center_y = size // 2 - center_size // 2
    
    draw.rectangle(
        [center_x, center_y, center_x + center_size, center_y + center_size],
        fill=color
    )
    
    # Добавляем уникальные элементы для каждого маркера
    # Это обеспечит уникальность распознавания
    
    # Позиции для уникальных квадратов (по углам)
    positions = [
        (border_width + 10, border_width + 10),  # Верхний левый
        (size - border_width - 60, border_width + 10),  # Верхний правый
        (border_width + 10, size - border_width - 60),  # Нижний левый
        (size - border_width - 60, size - border_width - 60),  # Нижний правый
    ]
    
    # Рисуем уникальный паттерн для каждого маркера
    for i, pos in enumerate(positions):
        if number & (1 << i):  # Используем биты номера для уникальности
            draw.rectangle(
                [pos[0], pos[1], pos[0] + 50, pos[1] + 50],
                fill=(0, 0, 0)
            )
        else:
            draw.ellipse(
                [pos[0], pos[1], pos[0] + 50, pos[1] + 50],
                fill=(100, 100, 100)
            )
    
    # Добавляем номер (для удобства идентификации)
    try:
        # Пытаемся использовать шрифт
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except:
        # Если шрифт не найден, используем стандартный
        font = ImageFont.load_default()
    
    text = str(number)
    # Получаем размер текста
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = center_y + center_size + 30
    
    draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
    
    return img

def create_all_markers():
    """Создает все 10 маркеров для команды"""
    
    # Определяем директорию для маркеров
    markers_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'markers')
    os.makedirs(markers_dir, exist_ok=True)
    
    # Конфигурация маркеров
    marker_configs = [
        (1, "CEO", (0, 255, 136)),      # Зеленый - Alex Cipher
        (2, "Security", (255, 107, 107)), # Красный - Maria Firewall
        (3, "OSINT", (78, 205, 196)),    # Бирюзовый - David OSINT
        (4, "Malware", (155, 89, 182)),  # Фиолетовый - Sarah Malware
        (5, "Forensics", (243, 156, 18)), # Оранжевый - John Forensic
        (6, "Cloud", (52, 152, 219)),    # Голубой - Emma Cloud
        (7, "RedTeam", (231, 76, 60)),   # Темно-красный - Mike RedOps
        (8, "Crypto", (22, 160, 133)),   # Темно-бирюзовый - Lisa Crypto
        (9, "Architect", (211, 84, 0)),  # Оранжево-коричневый - Robert
        (10, "SOC", (142, 68, 173)),     # Темно-фиолетовый - Anna SOC
    ]
    
    print("🎨 Генерация AR-маркеров для команды...")
    print("=" * 60)
    
    for number, name, color in marker_configs:
        # Создаем изображение маркера
        marker_img = create_marker_pattern(number, name, color)
        
        # Сохраняем как PNG (для печати)
        png_path = os.path.join(markers_dir, f'marker-{number}.png')
        marker_img.save(png_path, 'PNG')
        print(f"✓ Маркер {number:2d} ({name:12s}) создан: marker-{number}.png")
        
        # Создаем версию в высоком разрешении для печати
        high_res = create_marker_pattern(number, name, color, size=2048)
        high_res_path = os.path.join(markers_dir, f'marker-{number}-highres.png')
        high_res.save(high_res_path, 'PNG')
        print(f"   └─ Высокое разрешение: marker-{number}-highres.png")
    
    print("=" * 60)
    print(f"✅ Все маркеры созданы в папке: {markers_dir}")
    print("\n📋 Следующие шаги:")
    print("1. Откройте https://jeromeetienne.github.io/AR.js/three.js/examples/marker-training/examples/generator.html")
    print("2. Загрузите каждый marker-X.png файл")
    print("3. Скачайте сгенерированный .patt файл как marker-X.patt")
    print("4. Поместите .patt файлы в папку static/markers/")
    print("5. Распечатайте marker-X-highres.png файлы и повесьте на стену!")
    
    # Создаем PDF со всеми маркерами для удобной печати
    create_printable_sheet(marker_configs, markers_dir)

def create_printable_sheet(marker_configs, markers_dir):
    """Создает лист для печати со всеми маркерами"""
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        
        pdf_path = os.path.join(markers_dir, 'all_markers_print.pdf')
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        
        # Заголовок
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width/2, height - 2*cm, "CyberSec Team AR Markers")
        
        c.setFont("Helvetica", 10)
        c.drawCentredString(width/2, height - 2.8*cm, "Вырежьте и повесьте на стену")
        
        # Размещаем маркеры по 2 на страницу
        marker_size = 8 * cm
        x_positions = [3*cm, 12*cm]
        y_start = height - 6*cm
        
        for idx, (number, name, color) in enumerate(marker_configs):
            page_idx = idx // 4
            pos_idx = idx % 4
            
            if pos_idx == 0 and idx > 0:
                c.showPage()
                c.setFont("Helvetica-Bold", 20)
                c.drawCentredString(width/2, height - 2*cm, "CyberSec Team AR Markers")
            
            row = pos_idx // 2
            col = pos_idx % 2
            
            x = x_positions[col]
            y = y_start - row * (marker_size + 2*cm)
            
            # Добавляем изображение маркера
            img_path = os.path.join(markers_dir, f'marker-{number}.png')
            c.drawImage(img_path, x, y, width=marker_size, height=marker_size)
            
            # Добавляем подпись
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(x + marker_size/2, y - 0.5*cm, f"Marker {number}: {name}")
        
        c.save()
        print(f"\n📄 PDF для печати создан: all_markers_print.pdf")
        
    except ImportError:
        print("\n⚠️  Для создания PDF установите: pip install reportlab")
        print("   Или используйте отдельные PNG файлы для печати")

if __name__ == "__main__":
    create_all_markers()
