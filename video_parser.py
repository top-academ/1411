#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import shutil
from pathlib import Path
from urllib.parse import unquote
import html

def find_html_files(root_dir):
    """Находит все HTML файлы в директории и поддиректориях"""
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(('.html', '.htm')):
                html_files.append(os.path.join(root, file))
    return html_files

def extract_video_urls(html_content):
    """Извлекает URL видео из HTML"""
    # Ищем ссылки на видео с top-academy.site
    pattern = r'https://top-academy\.site/wp-content/uploads/[^"\s<>]+'
    urls = re.findall(pattern, html_content)
    
    # Фильтруем только видео файлы
    video_urls = []
    for url in urls:
        clean_url = url.split('?')[0].split('"')[0].split("'")[0].split('>')[0]
        if clean_url.endswith(('.mp4', '.webm', '.avi', '.mov')):
            video_urls.append(clean_url)
    
    return list(set(video_urls))  # Убираем дубликаты

def get_video_filename(url):
    """Получает имя файла из URL"""
    filename = url.split('/')[-1]
    filename = unquote(filename)
    return filename

def create_video_folder(html_file_path):
    """Создает папку для видео на основе имени HTML файла"""
    html_dir = os.path.dirname(html_file_path)
    html_name = os.path.basename(html_file_path)
    
    folder_name = os.path.splitext(html_name)[0] + '_files'
    video_folder = os.path.join(html_dir, folder_name)
    os.makedirs(video_folder, exist_ok=True)
    
    return video_folder

def download_video(url, output_path):
    """Скачивает видео через curl"""
    print(f"  Скачивание: {url}")
    print(f"  Сохранение в: {output_path}")
    
    try:
        result = subprocess.run(
            ['curl.exe', '-L', '-o', output_path, url],
            capture_output=True,
            text=True,
            timeout=300  # 5 минут таймаут
        )
        
        if result.returncode == 0 and os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"  ✓ Скачано: {file_size / (1024*1024):.2f} MB")
            return True
        else:
            print(f"  ✗ Ошибка скачивания")
            if result.stderr:
                print(f"  Ошибка: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ Исключение: {e}")
        return False

def copy_player_js(video_folder):
    """Копирует player.js в папку с видео"""
    player_js_source = os.path.join(os.getcwd(), 'src', 'player.js')
    
    if not os.path.exists(player_js_source):
        print(f"  ⚠ player.js не найден в src/player.js")
        return False
    
    player_js_dest = os.path.join(video_folder, 'player.js')
    
    try:
        shutil.copy2(player_js_source, player_js_dest)
        print(f"  ✓ player.js скопирован")
        return True
    except Exception as e:
        print(f"  ✗ Ошибка копирования player.js: {e}")
        return False

def replace_video_player(html_content, video_urls, video_folder_name):
    """Заменяет сложный плеер на Playerjs"""
    modified_html = html_content
    player_counter = 0
    
    for url in video_urls:
        filename = get_video_filename(url)
        local_path = f"./{video_folder_name}/{filename}"
        modified_html = modified_html.replace(url, local_path)
        url_encoded = url.replace('%', '%25')
        modified_html = modified_html.replace(url_encoded, local_path)

        url_decoded = unquote(url)
        if url_decoded != url:
            modified_html = modified_html.replace(url_decoded, local_path)
    
    # Теперь заменяем все блоки с mejs-плеером на Playerjs
    pattern = r'<span class="mejs-offscreen">Видеоплеер</span><div[^>]*id="mep_\d+"[^>]*>.*?</div>\s*</div>\s*</div>\s*</div>'
    
    # Для каждого найденного блока проверяем, есть ли в нем наш локальный путь
    def replace_player_block(match):
        nonlocal player_counter
        block = match.group(0)
        for url in video_urls:
            filename = get_video_filename(url)
            local_path = f"./{video_folder_name}/{filename}"
            if local_path in block:
                player_id = f"player{player_counter}"
                player_counter += 1
                # Заменяем весь блок на Playerjs
                return f'''<div id="{player_id}"></div>
<script>
   var {player_id} = new Playerjs({{id:"{player_id}", file:"{local_path}"}});
</script>'''
        return block
    
    modified_html = re.sub(pattern, replace_player_block, modified_html, flags=re.DOTALL)
    
    return modified_html

def add_player_js_to_html(html_content, video_folder_name):
    """Добавляет ссылку на player.js в HTML в <head>"""
    player_script = f'<script src="./{video_folder_name}/player.js" type="text/javascript"></script>'
    
    if player_script in html_content or f'src="./{video_folder_name}/player.js"' in html_content:
        return html_content
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', f'{player_script}\n</head>', 1)
    elif '</HEAD>' in html_content:
        html_content = html_content.replace('</HEAD>', f'{player_script}\n</HEAD>', 1)
    else:
        if '</body>' in html_content:
            html_content = html_content.replace('</body>', f'{player_script}\n</body>', 1)
        elif '</BODY>' in html_content:
            html_content = html_content.replace('</BODY>', f'{player_script}\n</BODY>', 1)
        else:
            html_content = player_script + '\n' + html_content
    
    return html_content

def process_html_file(html_file_path):
    """Обрабатывает один HTML файл"""
    print(f"\n{'='*80}")
    print(f"Обработка: {html_file_path}")
    print(f"{'='*80}")
    
    # Читаем HTML файл
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except UnicodeDecodeError:
        # Пробуем другую кодировку
        with open(html_file_path, 'r', encoding='cp1251') as f:
            html_content = f.read()

    video_urls = extract_video_urls(html_content)
    
    if not video_urls:
        print("  Видео не найдено")
        return
    
    print(f"  Найдено видео: {len(video_urls)}")

    video_folder = create_video_folder(html_file_path)
    video_folder_name = os.path.basename(video_folder)
    print(f"  Папка для видео: {video_folder}")

    downloaded_count = 0
    for url in video_urls:
        filename = get_video_filename(url)
        output_path = os.path.join(video_folder, filename)

        if os.path.exists(output_path):
            print(f"  ⊙ Уже существует: {filename}")
            downloaded_count += 1
        else:
            if download_video(url, output_path):
                downloaded_count += 1

    if downloaded_count > 0:
        print(f"\n  Обновление HTML файла...")
        
        # Копируем player.js в папку с видео
        copy_player_js(video_folder)

        modified_html = replace_video_player(html_content, video_urls, video_folder_name)
        modified_html = add_player_js_to_html(modified_html, video_folder_name)
        
        # Сохраняем модифицированный HTML
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(modified_html)
        
        print(f"  ✓ HTML обновлен с player.js")
    
    print(f"\n  Итого скачано: {downloaded_count}/{len(video_urls)}")

def main():
    """Главная функция"""
    print("="*80)
    print("Парсер видео из HTML файлов")
    print("="*80)
    root_dir = os.getcwd()
    print(f"\nПоиск HTML файлов в: {root_dir}")
    
    # Находим все HTML файлы
    html_files = find_html_files(root_dir)
    print(f"Найдено HTML файлов: {len(html_files)}")
    
    if not html_files:
        print("HTML файлы не найдены!")
        return
    # Обрабатываем каждый файл
    total_processed = 0
    for html_file in html_files:
        try:
            process_html_file(html_file)
            total_processed += 1
        except Exception as e:
            print(f"\n✗ Ошибка при обработке {html_file}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*80}")
    print(f"Обработка завершена!")
    print(f"Обработано файлов: {total_processed}/{len(html_files)}")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
