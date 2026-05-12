# Генератор мемов с ИТД 🐸

Веб-приложение для генерации мемов с изображениями Пепе и кринжовыми надписями про социальную сеть "ИТД".

## ✨ Особенности

- 🌐 Веб-интерфейс с анимированным дизайном
- 📸 Генерация мемов по клику
- 🎨 4 стиля обводки текста: толстый, тень, неон, простой
- 🔤 79 кринжовых фраз про ИТД
- 💾 Возможность сохранения мемов
- 📊 Статистика сгенерированных/сохранённых мемов

## 🚀 Локальный запуск

### Установка зависимостей:
```bash
pip install -r requirements.txt
```

### Запуск сервера:
```bash
python web_app.py
```

Откройте http://localhost:5000 в браузере.

## 🌐 Деплой на Render.com (бесплатно)

### Шаг 1: Создайте репозиторий на GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/ВАШ_ЮЗЕРНЕЙМ/itd-memes.git
git push -u origin main
```

### Шаг 2: Деплой на Render

1. Зайдите на [render.com](https://render.com)
2. Создайте аккаунт (бесплатно)
3. Нажмите "New +" → "Web Service"
4. Подключите ваш GitHub репозиторий
5. Настройки:
   - **Name**: itd-memes (или любое имя)
   - **Region**: Frankfurt (или ближайший)
   - **Branch**: main
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn web_app:app`
6. Нажмите "Create Web Service"

### Шаг 3: Добавьте изображения

После деплоя вам нужно загрузить изображения Пепе в проект:

1. В Render откройте ваш сервис
2. Перейдите в "Shell" (вкладка сверху)
3. Загрузите изображения через drag-and-drop или используйте git

**Важно**: Render.com имеет лимит на размер бесплатного тарифа. Если изображений много (>100), рассмотрите использование внешнего хранилища (S3, Cloudinary).

## 📋 Структура проекта

```
.
├── web_app.py              # Flask приложение
├── templates/
│   └── index.html          # Frontend
├── requirements.txt        # Зависимости
├── Procfile               # Конфигурация для Render
├── .gitignore            # Игнорируемые файлы
└── *.jpg, *.png          # Изображения Пепе
```

## 🔧 Технологии

- **Backend**: Flask (Python)
- **Frontend**: HTML + CSS + JavaScript
- **Image Processing**: Pillow (PIL)
- **Production Server**: Gunicorn
- **Hosting**: Render.com (бесплатный тариф)

## ⚠️ Ограничения бесплатного тарифа Render

- 512 MB RAM
- 0.1 CPU
- Спящий режим после 15 минут неактивности
- Холодный старт ~30 секунд при первом запросе

Для более производительного приложения рассмотрите платные тарифы или другие хостинги (Railway, Fly.io, PythonAnywhere).
