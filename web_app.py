from flask import Flask, send_file, render_template, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import random
import os
from io import BytesIO
import base64
import logging
import sys
import json
from datetime import datetime

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Счётчик для глитча
glitch_counter = 0

# Секретный код для добавления подписчиков
SECRET_CODE = "pepe2024"

# База подписчиков в памяти (для Render)
subscribers_db = []

# Загрузка подписчиков
def load_subscribers():
    global subscribers_db
    logger.info(f"Загрузка {len(subscribers_db)} подписчиков из памяти")
    return subscribers_db

# Сохранение подписчиков
def save_subscribers(subscribers):
    global subscribers_db
    try:
        subscribers_db = subscribers
        logger.info(f"Сохранено {len(subscribers)} подписчиков в память")
    except Exception as e:
        logger.error(f"Ошибка сохранения подписчиков: {e}")

# Извлечение @имен из фраз
def extract_usernames_from_phrase(phrase):
    usernames = []
    words = phrase.split()
    for word in words:
        if word.startswith('@'):
            usernames.append(word)
    return usernames

# Те же кринжовые фразы про ИТД
ITD_PHRASES = [
    # Депрессивные/экзистенциальные
    "ИТД — худшая соцсеть в истории",
    "зачем ИТД вообще существует",
    "я потерял 10 лет жизни в ИТД",
    "ИТД: место, где мозги идут в отпуск",
    "новая мера наказания — ИТД",
    "если любишь себя, избегай ИТД",
    "ИТД для тех, кто отчаялся",
    "почему я в ИТД? помогите!",
    "боже, спаси от ИТД",
    "кому вообще нужна эта ИТД",
    "ИТД — сплошное разочарование",
    "ещё долго ждать конца ИТД?",
    "даже день рождения веселее чем ИТД",
    
    # Странные/абсурдные
    "контент ИТД хуже чем Тик-Ток",
    "Пепа не спасёт ИТД",
    "даже спам красивее ИТД",
    "воин света, не лезь в ИТД",
    "ИТД создана чтобы мучить человечество",
    "как правильно НЕ делать соцсеть — смотри ИТД",
    "лучше смотри на стену",
    
    # Вызывающие/провокационные
    "худше чем читать спецификацию PHP",
    "даже 4chan выглядит позитивной в сравнении",
    "запретить нельзя помиловать — это про ИТД",
    "издевательство под видом маркетинга",
    "почему VK лучше — вопрос риторический",
    "я смотрю YT Shorts вместо ИТД",
    "твоя карма: пользователь ИТД",
    
    # С подписчиками
    "@blin_w в ИТД? соболезнуем",
    "@artem85 был заражен вирусом ИТД",
    "@boknak спасайся, ИТД близко",
    "@eblan_42 попал в ловушку ИТД",
    "@olesaa уже потеряла надежду на ИТД",
    "@kiss_love влюбилась в ИТД на беду себе",
    "@youcrash столкнулся с реальностью ИТД",
    "@bl4z1k сгорел на ИТД",
    
    "в ИТД даже @blin_w чувствует боль",
    "@artem85 бежит от ИТД на скорости света",
    "@boknak молится спастись из ИТД",
    "@eblan_42 забыл пароль в ИТД и рад",
    "@olesaa советует всем избегать ИТД",
    "ИТД это то что объединяет @blin_w и меня",
    
    # Абсурдные
    "ОШИБКА: человечество не найдено",
    "404: смысл жизни не найден",
    "куплю у кого-то аккаунт побогаче",
    "это не ошибка, это фича от дьявола",
    "системный сбой или воля судьбы?",
    "если это сон то зачем я не просыпаюсь",
    "деньги которые я потратил на это — оплачены",
    "помогите моей психике пережить это",
    "ИТД vs здравый смысл — 1:0 для ИТД",
    
    "ИТД это не социальная сеть это издевательство",
    "все наши проблемы начались с ИТД",
    "история помнит много плохого но ИТД забыть не сможет",
    "архипелаг Гулаг по сравнению с ИТД это райский остров",
    "Нострадамус забыл предсказать про ИТД",
    "ИТД это вирус для которого нет вакцины",
]

# Стили контура (только черный)
STYLES = ["thick", "simple"]

def load_font(size):
    """Загрузить шрифт или вернуть стандартный"""
    candidates = [
        "arial.ttf",
        "DejaVuSans-Bold.ttf",
        "DejaVuSans.ttf",
        # Windows
        "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        # macOS
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    
    logger.warning("Не удалось загрузить шрифт, используется стандартный")
    return ImageFont.load_default()


def draw_text_with_outline(draw, pos, text, font, outline_style="thick"):
    """Рисовать текст с черной обводкой"""
    x, y = pos
    
    if outline_style == "thick":
        for adj_x in range(-4, 5):
            for adj_y in range(-4, 5):
                if adj_x != 0 or adj_y != 0:
                    draw.text((x+adj_x, y+adj_y), text, font=font, fill=(0, 0, 0, 255))
        draw.text(pos, text, font=font, fill=(255, 255, 255, 255))
        
    else:  # simple
        for adj_x in [-2, -1, 0, 1, 2]:
            for adj_y in [-2, -1, 0, 1, 2]:
                if adj_x != 0 or adj_y != 0:
                    draw.text((x+adj_x, y+adj_y), text, font=font, fill=(0, 0, 0, 255))
        draw.text(pos, text, font=font, fill=(255, 255, 255, 255))


def apply_glitch(img):
    """Применить дикий глитч эффект к изображению"""
    w, h = img.size
    pixels = img.load()
    
    # RGB сдвиг (хроматическая аберрация)
    shift = random.randint(5, 15)
    direction = random.choice(['horizontal', 'vertical'])
    
    if direction == 'horizontal':
        for y in range(h):
            for x in range(w - shift):
                r, g, b = pixels[x + shift, y]
                pixels[x, y] = (r, pixels[x, y][1], pixels[x, y][2])
    else:
        for x in range(w):
            for y in range(h - shift):
                r, g, b = pixels[x, y + shift]
                pixels[x, y] = (r, pixels[x, y][1], b)
    
    # Случайные горизонтальные полосы
    for _ in range(random.randint(3, 8)):
        y = random.randint(0, h - 1)
        height = random.randint(1, 5)
        for py in range(min(y + height, h)):
            for x in range(w):
                if random.random() > 0.5:
                    pixels[x, py] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    # Случайные пиксельные искажения
    for _ in range(random.randint(50, 150)):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        pixels[x, y] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    return img


def generate_image():
    """Генерировать одну случайную картинку с мемом"""
    try:
        # Выбрать случайную картинку из папки
        images_dir = "."
        exts = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif'}
        files = [f for f in os.listdir(images_dir) if os.path.splitext(f.lower())[1] in exts]
        
        if not files:
            logger.error("Изображения не найдены в директории")
            return None
        
        img_file = random.choice(files)
        img_path = os.path.join(images_dir, img_file)
        
        # Открыть картинку
        img = Image.open(img_path).convert('RGBA')
        w, h = img.size
        
        # Загрузить подписчиков для добавления в фразы
        subscribers = load_subscribers()
        subscriber_usernames = [s['username'] for s in subscribers]
        
        # Выбрать текст и стиль
        text = random.choice(ITD_PHRASES)
        style = random.choice(STYLES)
        
        # Автоматически добавлять @имена в базу
        usernames = extract_usernames_from_phrase(text)
        logger.info(f"Найдены @имена в тексте: {usernames}")
        if usernames:
            for username in usernames:
                if username not in subscriber_usernames:
                    logger.info(f"Добавление нового подписчика: {username}")
                    subscribers.append({
                        'username': username,
                        'added_at': datetime.now().isoformat(),
                        'source': text
                    })
            save_subscribers(subscribers)
            subscriber_usernames = [s['username'] for s in subscribers]
            logger.info(f"Всего подписчиков в базе: {len(subscribers)}")
        
        # Иногда добавлять подписчиков в текст
        if subscriber_usernames and random.random() < 0.3:  # 30% шанс
            random_subscriber = random.choice(subscriber_usernames)
            # Добавляем подписчика в случайное место текста
            words = text.split()
            insert_pos = random.randint(0, len(words))
            words.insert(insert_pos, random_subscriber)
            text = ' '.join(words)
        
        # Подготовка текста (уменьшенный размер)
        font_size = max(30, w // 12)
        font = load_font(font_size)
        
        # Создать слой для текста
        txt = Image.new('RGBA', img.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)
        
        # Разбить текст на строки
        lines = []
        words = text.split()
        line = ''
        for word in words:
            test = (line + ' ' + word).strip()
            bbox = d.textbbox((0, 0), test, font=font)
            test_width = bbox[2] - bbox[0]
            if test_width > w * 0.85:
                if line:
                    lines.append(line)
                line = word
            else:
                line = test
        if line:
            lines.append(line)
        
        # Расчет высоты текста
        line_height = 0
        for l in lines:
            bbox = d.textbbox((0, 0), l, font=font)
            line_height = max(line_height, bbox[3] - bbox[1])
        
        total_h = len(lines) * line_height
        padding = int(h * 0.05)
        y = h - total_h - padding
        
        # Рисовать строки
        for line_text in lines:
            bbox = d.textbbox((0, 0), line_text, font=font)
            tw = bbox[2] - bbox[0]
            x = (w - tw) // 2
            draw_text_with_outline(d, (x, y), line_text, font, style)
            y += line_height
        
        # Добавить водяной знак @sozdatelpepe в нижний правый угол
        watermark_text = "@sozdatelpepe"
        watermark_font_size = max(15, w // 40)
        watermark_font = load_font(watermark_font_size)
        
        bbox = d.textbbox((0, 0), watermark_text, font=watermark_font)
        wm_width = bbox[2] - bbox[0]
        wm_height = bbox[3] - bbox[1]
        wm_x = w - wm_width - int(w * 0.02)
        wm_y = h - wm_height - int(h * 0.02)
        
        # Рисовать водяной знак полупрозрачным белым с черной обводкой
        for adj_x in [-2, -1, 0, 1, 2]:
            for adj_y in [-2, -1, 0, 1, 2]:
                if adj_x != 0 or adj_y != 0:
                    d.text((wm_x + adj_x, wm_y + adj_y), watermark_text, font=watermark_font, fill=(0, 0, 0, 150))
        d.text((wm_x, wm_y), watermark_text, font=watermark_font, fill=(255, 255, 255, 200))
        
        out = Image.alpha_composite(img, txt).convert('RGB')
        
        # Глобальный счётчик для глитча
        global glitch_counter
        glitch_counter += 1
        
        # Применять глитч каждые 4-6 картинок
        if glitch_counter % random.randint(4, 6) == 0:
            out = apply_glitch(out)
        
        return out
        
    except Exception as e:
        logger.error(f"Ошибка при генерации изображения: {e}")
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate')
def generate():
    """API endpoint для генерации картинки"""
    try:
        img = generate_image()
        
        if img is None:
            logger.error("Не удалось сгенерировать изображение")
            return {'error': 'No images found'}, 404
        
        # Сохранить в BytesIO
        img_io = BytesIO()
        img.save(img_io, 'JPEG', quality=95)
        img_io.seek(0)
        
        # Кодировать в base64
        img_base64 = base64.b64encode(img_io.getvalue()).decode()
        
        return {'image': f'data:image/jpeg;base64,{img_base64}'}
        
    except Exception as e:
        logger.error(f"Ошибка в endpoint /generate: {e}")
        return {'error': 'Internal server error'}, 500


@app.route('/admin/subscribers', methods=['GET', 'POST'])
def admin_subscribers():
    """Секретный эндпоинт для управления подписчиками"""
    if request.method == 'POST':
        data = request.get_json()
        code = data.get('code', '')
        
        if code != SECRET_CODE:
            return {'error': 'Неверный код доступа'}, 403
        
        action = data.get('action', 'view')
        
        if action == 'view':
            subscribers = load_subscribers()
            return {'subscribers': subscribers}
        elif action == 'add':
            username = data.get('username', '')
            if username.startswith('@'):
                subscribers = load_subscribers()
                if username not in [s['username'] for s in subscribers]:
                    subscribers.append({
                        'username': username,
                        'added_at': datetime.now().isoformat(),
                        'source': 'manual'
                    })
                    save_subscribers(subscribers)
                    return {'message': f'Пользователь {username} добавлен'}
                else:
                    return {'message': f'Пользователь {username} уже существует'}
            else:
                return {'error': 'Имя должно начинаться с @'}, 400
        elif action == 'delete':
            username = data.get('username', '')
            subscribers = load_subscribers()
            subscribers = [s for s in subscribers if s['username'] != username]
            save_subscribers(subscribers)
            return {'message': f'Пользователь {username} удален'}
        
        return {'error': 'Неизвестное действие'}, 400
    
    # GET запрос - показываем простую админку
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Админка подписчиков</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f0f0f0; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
            input, button { padding: 10px; margin: 5px; }
            button { background: #007bff; color: white; border: none; cursor: pointer; }
            button:hover { background: #0056b3; }
            .subscriber { padding: 10px; border: 1px solid #ddd; margin: 5px 0; border-radius: 5px; }
            .error { color: red; }
            .success { color: green; }
            .scroll-container { max-height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; border-radius: 5px; }
            .subscriber-item { padding: 10px; border-bottom: 1px solid #eee; position: relative; }
            .delete-btn { float: right; background: #dc3545; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Админка подписчиков ИТД</h1>
            <div>
                <input type="password" id="code" placeholder="Секретный код">
                <button onclick="loadSubscribers()">Загрузить подписчиков</button>
            </div>
            <div>
                <input type="text" id="username" placeholder="@username">
                <button onclick="addSubscriber()">Добавить подписчика</button>
            </div>
            <div id="message"></div>
            <div id="subscribers"></div>
        </div>
        
        <script>
            async function loadSubscribers() {
                const code = document.getElementById('code').value;
                try {
                    const response = await fetch('/admin/subscribers', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({code: code, action: 'view'})
                    });
                    const data = await response.json();
                    if (response.ok) {
                        displaySubscribers(data.subscribers);
                    } else {
                        showMessage(data.error, 'error');
                    }
                } catch (e) {
                    showMessage('Ошибка соединения', 'error');
                }
            }
            
            async function addSubscriber() {
                const code = document.getElementById('code').value;
                const username = document.getElementById('username').value;
                try {
                    const response = await fetch('/admin/subscribers', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({code: code, action: 'add', username: username})
                    });
                    const data = await response.json();
                    if (response.ok) {
                        showMessage(data.message, 'success');
                        loadSubscribers();
                    } else {
                        showMessage(data.error, 'error');
                    }
                } catch (e) {
                    showMessage('Ошибка соединения', 'error');
                }
            }
            
            async function deleteSubscriber(username) {
                const code = document.getElementById('code').value;
                try {
                    const response = await fetch('/admin/subscribers', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({code: code, action: 'delete', username: username})
                    });
                    const data = await response.json();
                    if (response.ok) {
                        showMessage(data.message, 'success');
                        loadSubscribers();
                    } else {
                        showMessage(data.error, 'error');
                    }
                } catch (e) {
                    showMessage('Ошибка соединения', 'error');
                }
            }
            
            function displaySubscribers(subscribers) {
                const div = document.getElementById('subscribers');
                div.innerHTML = '<h3>Подписчики (' + subscribers.length + ')</h3>';
                div.innerHTML += '<div class="scroll-container">';
                subscribers.forEach(s => {
                    div.innerHTML += '<div class="subscriber-item">' + 
                        '<strong>' + s.username + '</strong> - ' + 
                        new Date(s.added_at).toLocaleString() + 
                        '<br><small style="color: #666;">Источник: ' + (s.source || 'авто') + '</small>' +
                        ' <button class="delete-btn" onclick="deleteSubscriber(\\'' + s.username + '\\')">Удалить</button>' +
                        '<div style="clear: both;"></div></div>';
                });
                div.innerHTML += '</div>';
            }
            
            function showMessage(msg, type) {
                const div = document.getElementById('message');
                div.innerHTML = '<div class="' + type + '">' + msg + '</div>';
                setTimeout(() => div.innerHTML = '', 3000);
            }
        </script>
    </body>
    </html>
    '''


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
