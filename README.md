# Система онлайн голосования

Веб-приложение для проведения онлайн голосования. Курсовой проект по интернет-технологиям.

## Технологии

- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Контейнеризация:** Docker, Docker Compose
- **CI/CD:** GitHub Actions

## Функциональность

- Просмотр списка кандидатов
- Голосование за кандидата
- Защита от повторного голосования (по IP)
- Автоматическая документация API (Swagger UI)
- Автоматическое добавление тестовых данных

## Установка и запуск

### Локальный запуск

```bash
# Клонировать репозиторий
git clone https://github.com/ВАШ_ЛОГИН/online-voting.git
cd online-voting

# Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Установить зависимости
pip install -r requirements.txt

# Запустить приложение
uvicorn backend.main:app --reload

Открыть в браузере: http://localhost:8000
