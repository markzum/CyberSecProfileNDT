# AR Markers Directory

Эта папка содержит .patt файлы для AR-маркеров.

## Как создать .patt файлы:

1. Сначала сгенерируйте PNG изображения маркеров:
   ```bash
   python generate_markers.py
   ```

2. Для каждого marker-X.png создайте .patt файл:
   - Откройте: https://jeromeetienne.github.io/AR.js/three.js/examples/marker-training/examples/generator.html
   - Загрузите marker-X.png
   - Скачайте сгенерированный .patt файл
   - Переименуйте в marker-X.patt
   - Поместите в эту папку

## Необходимые файлы:

- marker-1.patt (CEO / Team Lead - Alex Cipher)
- marker-2.patt (Security Analyst - Maria Firewall)
- marker-3.patt (OSINT Specialist - David OSINT)
- marker-4.patt (Malware Analyst - Sarah Malware)
- marker-5.patt (Forensics Expert - John Forensic)
- marker-6.patt (Cloud Security Engineer - Emma Cloud)
- marker-7.patt (Red Team Operator - Mike RedOps)
- marker-8.patt (Cryptography Specialist - Lisa Crypto)
- marker-9.patt (Security Architect - Robert Architect)
- marker-10.patt (SOC Analyst - Anna SOC)

## Проверка:

После создания всех файлов, в этой папке должно быть 10 файлов .patt
