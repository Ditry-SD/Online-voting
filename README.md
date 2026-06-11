# 🗳️ Система онлайн голосования

Веб-приложение для проведения онлайн голосования. Курсовой проект по дисциплине "Интернет-технологии".

## 🚀 Функциональность

- ✅ Просмотр списка кандидатов с описанием
- ✅ Голосование за выбранного кандидата
- ✅ Защита от повторного голосования (по IP-адресу)
- ✅ Страница с результатами голосования
- ✅ Сброс голосов для тестирования
- ✅ Адаптивный дизайн (Bootstrap 5)
- ✅ Автоматическая документация API (Swagger UI)
- ✅ Автоматическое добавление тестовых данных при первом запуске
- ✅ Контейнеризация (Docker + Docker Compose)

## 🛠️ Технологии

| Компонент | Технология |
|-----------|------------|
| **Backend** | Python 3.9, FastAPI, SQLAlchemy |
| **База данных** | SQLite |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5 |
| **Контейнеризация** | Docker, Docker Compose |
| **Веб-сервер** | Uvicorn |
| **API документация** | Swagger UI (автоматически) |

## 📦 Установка и запуск

### Локальный запуск (Windows)

bash
# 1. Клонировать репозиторий
git clone https://github.com/Ditry-SD/online-voting.git
cd online-voting

# 2. Создать и активировать виртуальное окружение
python -m venv venv
venv\Scripts\activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Запустить приложение
uvicorn backend.main:app --reload

После запуска открыть в браузере: http://localhost:8000

Запуск через Docker
bash
# 1. Клонировать репозиторий
git clone https://github.com/Ditry-SD/online-voting.git
cd online-voting

# 2. Собрать и запустить контейнер
docker-compose up --build
После запуска открыть в браузере: http://localhost:8000

📡 API Endpoints
Метод	URL	Описание
GET	/	Главная страница со списком кандидатов
GET	/results	Страница с результатами голосования
GET	/api/candidates	Получить список всех кандидатов (JSON)
POST	/api/vote/{candidate_id}	Проголосовать за кандидата по его ID
POST	/api/reset-votes	Сбросить все голоса (для тестирования)
GET	/docs	Интерактивная документация API (Swagger UI)
📁 Структура проекта
text
online-voting/
├── backend/                    # Серверная часть приложения
│   ├── __init__.py            # Инициализация Python-пакета
│   ├── main.py                # Основной файл с API-эндпоинтами
│   ├── models.py              # Модели таблиц базы данных
│   └── database.py            # Настройка подключения к БД
├── frontend/                   # Клиентская часть приложения
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css      # Стили оформления страниц
│   │   └── js/
│   │       └── voting.js      # Логика голосования (AJAX)
│   └── templates/
│       ├── index.html         # Главная страница
│       └── results.html       # Страница результатов
├── Dockerfile                  # Инструкция для сборки Docker-образа
├── docker-compose.yml          # Конфигурация для Docker Compose
├── requirements.txt            # Список Python-зависимостей
├── .dockerignore               # Исключения для Docker
├── .gitignore                  # Игнорируемые Git файлы
└── README.md                   # Описание проекта (этот файл)
🌿 Стратегия ветвления (Git)
В проекте используется Git Flow:

Ветка	Назначение
main	Стабильная версия для продакшена
develop	Основная ветка разработки
feature/*	Новый функционал
bugfix/*	Исправление ошибок
Текущие ветки:
main — стабильная версия

develop — разработка

feature/docker-improvements — улучшение Docker-конфигурации

feature/documentation — документация проекта

feature/roles-and-security — роли и безопасность

feature/tests — тестирование

Порядок работы с ветками:
bash
# Создание новой ветки от develop
git checkout develop
git checkout -b feature/my-feature

# После завершения работы
git add .
git commit -m "feat: описание изменений"
git push origin feature/my-feature
🔒 Защита от повторного голосования
Приложение отслеживает IP-адрес каждого голосующего. При попытке проголосовать повторно с того же IP-адреса выводится предупреждение, и голос не учитывается. Информация о голосах сохраняется в базе данных SQLite.

📊 Страница результатов
Страница /results отображает:

Общее количество проголосовавших

Количество голосов за каждого кандидата

Прогресс-бары для наглядного сравнения результатов

Кнопку сброса голосов для тестирования

## 🗂️ Схема базы данных
candidates
├── id (INTEGER, PK)
├── name (VARCHAR, UNIQUE)
├── description (VARCHAR)
└── votes (INTEGER)

votes
├── id (INTEGER, PK)
├── user_ip (VARCHAR)
├── candidate_id (INTEGER, FK)
└── timestamp (DATETIME)

👨‍💻 Автор
ФИО: Морозов Дмитрий Владимирович
Группа: ПИН-б-з-22-1
Дисциплина: Интернет-технологии
Год: 2026