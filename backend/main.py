import os
import sys

# Добавляем корневую папку проекта в пути Python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.database import engine, SessionLocal, Base
from backend import models

# Создаем приложение FastAPI
app = FastAPI(title="Online Voting System")

# Создаем все таблицы в базе данных при запуске
Base.metadata.create_all(bind=engine)

# Настраиваем пути к статическим файлам и шаблонам
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "frontend", "templates")

# Монтируем папку со статическими файлами (CSS, JS, изображения)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Настраиваем шаблонизатор Jinja2
templates = Jinja2Templates(directory=TEMPLATES_DIR)

def get_db():
    """
    Функция-генератор для получения сессии базы данных.
    Автоматически закрывает соединение после использования.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/candidates")
def get_candidates(db: Session = Depends(get_db)):
    """
    API endpoint: получение списка всех кандидатов.
    Возвращает JSON со всеми кандидатами и количеством голосов.
    """
    candidates = db.query(models.Candidate).all()
    return candidates

@app.post("/api/vote/{candidate_id}")
def vote(candidate_id: int, request: Request, db: Session = Depends(get_db)):
    """
    API endpoint: голосование за кандидата.
    Проверяет, не голосовал ли уже этот IP-адрес.
    """
    # Получаем IP-адрес голосующего
    user_ip = request.client.host
    
    # Проверяем, не голосовал ли уже этот IP
    existing_vote = db.query(models.Vote).filter(
        models.Vote.user_ip == user_ip
    ).first()
    
    if existing_vote:
        raise HTTPException(
            status_code=400, 
            detail="Вы уже голосовали! С одного IP можно голосовать только один раз."
        )
    
    # Ищем кандидата по ID
    candidate = db.query(models.Candidate).filter(
        models.Candidate.id == candidate_id
    ).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Кандидат не найден")
    
    # Увеличиваем счетчик голосов кандидата
    candidate.votes += 1
    
    # Сохраняем информацию о голосе
    vote_record = models.Vote(
        user_ip=user_ip,
        candidate_id=candidate_id
    )
    db.add(vote_record)
    
    # Сохраняем все изменения в базе данных
    db.commit()
    
    return {
        "message": "Голос успешно учтен!",
        "candidate": candidate.name,
        "total_votes": candidate.votes
    }

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    """
    Главная страница приложения.
    Отображает HTML-шаблон со списком кандидатов.
    """
    candidates = db.query(models.Candidate).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"candidates": candidates}
    )

# Автоматическое добавление тестовых данных при первом запуске
@app.on_event("startup")
def startup_event():
    """
    Выполняется при запуске приложения.
    Добавляет тестовых кандидатов, если база данных пуста.
    """
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже кандидаты в базе
        candidates_count = db.query(models.Candidate).count()
        
        if candidates_count == 0:
            print("База данных пуста. Добавляем тестовых кандидатов...")
            
            test_candidates = [
                models.Candidate(
                    name="Иван Петров",
                    description="Опытный руководитель с 10-летним стажем. "
                                "Выступает за цифровизацию и внедрение инноваций."
                ),
                models.Candidate(
                    name="Мария Сидорова",
                    description="Молодой специалист с инновационными идеями. "
                                "Фокус на экологических проектах и образовании."
                ),
                models.Candidate(
                    name="Алексей Иванов",
                    description="Технический эксперт в области IT. "
                                "Предлагает программу развития кибербезопасности."
                ),
                models.Candidate(
                    name="Елена Кузнецова",
                    description="Социальный работник с 15-летним опытом. "
                                "Приоритет - социальная защита населения."
                ),
                models.Candidate(
                    name="Дмитрий Соколов",
                    description="Предприниматель, создавший 500 рабочих мест. "
                                "Программа поддержки малого и среднего бизнеса."
                ),
            ]
            
            for candidate in test_candidates:
                db.add(candidate)
            
            db.commit()
            print(f"Успешно добавлено {len(test_candidates)} тестовых кандидатов!")
        else:
            print(f"В базе данных уже есть {candidates_count} кандидатов.")
            
    except Exception as e:
        print(f"Ошибка при инициализации данных: {e}")
        db.rollback()
    finally:
        db.close()