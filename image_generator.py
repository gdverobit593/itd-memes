import os
import random
import argparse
from PIL import Image, ImageDraw, ImageFont

# Кринжовые фразы про ИТД
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
    
    # Человечные/странные
    "здесь обитают люди которые кусают провода",
    "ИТД = боль и только боль",
    "я как чат-бот в чате-боте",
    "чувствую что умираю заживо от ИТД",
    "это не контент, это психологическое оружие",
    "забыл зачем я вообще сюда пришёл",
    "даже бабушка постит лучше",
    "ретро видео в 240p более достойно",
    
    # Мета-комментарии
    "создатели сами не юзают свой сервис",
    "инвесторы просят деньги назад",
    "шутка вышла из-под контроля",
    "социальный эксперимент над нами",
    "кто придумал это и почему свободен",
    "Илон Маск сказал НЕТ",
    "даже ИИ отказывается давать оценку ИТД",
    
    # Странные философские
    "видел ли ты слёзы в коде?",
    "не жизнь, а медленная смерть онлайн",
    "если есть бог, вот его худшая работа",
    "существа здесь потеряли свой путь",
    "девятый круг ада завидует ИТД",
    "я теряю веру в человечество ежедневно",
    
    # Кринжовые/вызывающие смех
    "красивый дизайн, но контент — мусор",
    "страдай, но со стилем",
    "vibes? нет, antivibes",
    "контент но наоборот",
    "мемы здесь мертвы до загрузки",
    "крипто потеряла смысл но ИТД нет",
    
    # Провокационные
    "это не буллинг, это образование",
    "токсичность теперь это фича",
    "твоя деградация — мой лайк",
    "деньги в огонь за ИТД",
    "даже мама говорит удалить приложение",
    "батя вышел из чата насовсем",
    
    # Абсурдные сравнения
    "как писать на ассемблере в 2026",
    "жить с 100 кричащими соседями — это ИТД",
    "слово 'крах' было создано для ИТД",
    "ощущение от плохой вечеринки × 1000",
    "Java выглядит проще чем ИТД",
    "даже COBOL более актуален",
    
    # Экзистенциальные
    "в чём смысл жизни если ИТД существует",
    "это не соцсеть, это зеркало ада",
    "рождение комплексов в реальном времени",
    "запах отчаяния витает в воздухе",
    "люби себя — удали ИТД",
    "я уже не верю в лучшее",
    
    # Совсем странные
    "ОШИБКА: человечество не найдено",
    "404: смысл жизни не найден",
    "куплю у кого-то аккаунт побогаче",
    "это не ошибка, это фича от дьявола",
    "системный сбой или воля судьбы?",
    "если это сон то зачем я не просыпаюсь",
    "деньги которые я потратил на это — оплачены",
    "помогите моей психике пережить это",
    "ИТД vs здравый смысл — 1:0 для ИТД",
    
    # С упоминаниями подписчиков (только @username)
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
    "@youcrash упал в пропасть под названием ИТД",
    "@bl4z1k горит как файерволл в ИТД",
    
    "@blin_w и я страдаем от ИТД вместе",
    "даже враги @artem85 не пожелают ИТД",
    "@boknak потерял здравомыслие из-за ИТД",
    "@eblan_42 забанил ИТД навечно",
    "@olesaa пишет мне в ВК спасайся от ИТД",
    "@youcrash запостил о ИТД и удалил",
    "ИТД это то что объединяет @blin_w и меня",
    
    "все подписчики включая @artem85 бегут от ИТД",
    "@boknak создал мем про ИТД",
    "даже @eblan_42 не может пошутить про ИТД",
    "@olesaa готова пожертвовать чем угодно лишь бы избежать ИТД",
    "@youcrash.exe запустил ИТД и вылетел",
    "@kiss_love скажет что ИТД это ошибка",
    "@bl4z1k скажет что это не фича",
    
    # Ещё про ИТД
    "ИТД это не социальная сеть это издевательство",
    "все наши проблемы начались с ИТД",
    "история помнит много плохого но ИТД забыть не сможет",
    "ИТД это то что разделило людей на людей и подписчиков",
    "архипелаг Гулаг по сравнению с ИТД это райский остров",
    "Нострадамус забыл предсказать про ИТД",
    "ИТД это вирус для которого нет вакцины",
    "кому нужна ИТД когда есть видеозвонки в групповом чате",
]


def find_images(input_dir, count=10):
    """Найти случайные картинки из папки"""
    exts = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif'}
    files = [f for f in os.listdir(input_dir) if os.path.splitext(f.lower())[1] in exts]
    if not files:
        raise FileNotFoundError(f"No images found in {input_dir}")
    return [os.path.join(input_dir, f) for f in random.sample(files, min(count, len(files)))]


def load_font(size):
    """Загрузить шрифт или вернуть стандартный"""
    candidates = ["arial.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf", "C:\\Windows\\Fonts\\arial.ttf"]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_text_with_outline(draw, pos, text, font, outline_style="thick"):
    """Рисовать текст с обводкой разного стиля"""
    x, y = pos
    
    if outline_style == "thick":
        # Толстая обводка (5px)
        for adj_x in range(-5, 6):
            for adj_y in range(-5, 6):
                if adj_x != 0 or adj_y != 0:
                    draw.text((x+adj_x, y+adj_y), text, font=font, fill=(0, 0, 0, 255))
        draw.text(pos, text, font=font, fill=(255, 255, 255, 255))
        
    elif outline_style == "shadow":
        # Тень (смещение)
        draw.text((x+4, y+4), text, font=font, fill=(0, 0, 0, 200))
        draw.text((x+2, y+2), text, font=font, fill=(50, 50, 50, 255))
        draw.text(pos, text, font=font, fill=(255, 255, 255, 255))
        
    elif outline_style == "neon":
        # Неоновый эффект (двойная обводка)
        for adj in range(-3, 4):
            draw.text((x+adj, y-3), text, font=font, fill=(0, 255, 255, 150))
            draw.text((x+adj, y+3), text, font=font, fill=(255, 0, 255, 150))
        draw.text(pos, text, font=font, fill=(255, 255, 255, 255))
        
    else:  # simple
        # Простая обводка (2px)
        for adj_x in [-2, -1, 0, 1, 2]:
            for adj_y in [-2, -1, 0, 1, 2]:
                if adj_x != 0 or adj_y != 0:
                    draw.text((x+adj_x, y+adj_y), text, font=font, fill=(0, 0, 0, 255))
        draw.text(pos, text, font=font, fill=(255, 255, 255, 255))


def draw_text_on_image(img_path, text, out_dir, outline_style="thick"):
    """Нанести текст на картинку с обводкой"""
    img = Image.open(img_path).convert('RGBA')
    w, h = img.size

    # Подготовка текста
    font_size = max(40, w // 8)
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
        draw_text_with_outline(d, (x, y), line_text, font, outline_style)
        y += line_height

    out = Image.alpha_composite(img, txt).convert('RGB')
    
    # Сохранить результат
    base = os.path.basename(img_path)
    name, ext = os.path.splitext(base)
    out_name = f"idt_{name}.jpg"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, out_name)
    out.save(out_path, quality=95)
    return out_path


def main():
    parser = argparse.ArgumentParser(description='Генератор мемов с ИТД: 10 картинок с кринжовыми надписями')
    parser.add_argument('--input-dir', '-i', default='.', help='Папка с исходными картинками')
    parser.add_argument('--output-dir', '-o', default='output', help='Папка для результата')
    parser.add_argument('--count', '-c', type=int, default=10, help='Количество картинок (default: 10)')
    parser.add_argument('--seed', type=int, default=None, help='Сид для случайности')
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    if not os.path.isdir(args.input_dir):
        raise NotADirectoryError(f"Input directory not found: {args.input_dir}")

    # Выбрать случайные картинки
    print(f"🐸 Ищу {args.count} картинок Пепа из папки {args.input_dir}...")
    img_paths = find_images(args.input_dir, args.count)
    print(f"✅ Найдено {len(img_paths)} картинок\n")

    # Стили обводки для разнообразия
    outline_styles = ["thick", "shadow", "neon", "simple"]
    
    # Обработать каждую картинку
    results = []
    for idx, img_path in enumerate(img_paths, 1):
        # Выбрать случайный текст и стиль
        text = random.choice(ITD_PHRASES)
        style = outline_styles[idx % len(outline_styles)]
        
        print(f"[{idx}/{len(img_paths)}] Обрабатываю {os.path.basename(img_path)}...")
        print(f"       Текст: {text}")
        print(f"       Стиль: {style}")
        
        try:
            out_path = draw_text_on_image(img_path, text, args.output_dir, style)
            results.append(out_path)
            print(f"       ✅ Сохранено: {os.path.basename(out_path)}\n")
        except Exception as e:
            print(f"       ❌ Ошибка: {e}\n")

    print(f"\n🎉 Готово! Обработано {len(results)} из {len(img_paths)} картинок")
    print(f"📁 Результаты в папке: {os.path.abspath(args.output_dir)}")


if __name__ == '__main__':
    main()
