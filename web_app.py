from flask import Flask, send_file, render_template
from PIL import Image, ImageDraw, ImageFont
import random
import os
from io import BytesIO
import base64
import logging
import sys

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Счётчик для глитча
glitch_counter = 0

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
        
        # Выбрать текст и стиль
        text = random.choice(ITD_PHRASES)
        style = random.choice(STYLES)
        
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
