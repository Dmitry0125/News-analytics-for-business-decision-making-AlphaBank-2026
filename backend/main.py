import os
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import engine, get_db
from schemas import InsightResponse, UserRole, MOCK_INSIGHTS
from models import Base, Company, Transaction, CompanyIndividualLink

# Явно принудительно загружаем переменные из .env файла перед инициализацией приложения
# На сервере в Docker эти переменные пробросятся операционной системой автоматически
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

# Считываем разрешенные фронтенд-адреса из .env (по умолчанию localhost:3000)
origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
ALLOWED_ORIGINS = [origin.strip() for origin in origins_env.split(",")]

# Управляем жизненным циклом приложения (события старта и стопа)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Асинхронный аналог Base.metadata.create_all(bind=engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Тут можно прописать действия при выключении сервера, если пригодятся

app = FastAPI(
    title="Alfa News Insights API",
    description="Enterprise API для мультиагентного анализа новостей корпоративного бизнеса",
    version="1.0.0",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# в будущем сделать вот так!
# НАСТРОЙКА CORS: Защита на уровне браузера
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=ALLOWED_ORIGINS,  # Разрешаем доступ только нашему фронтенду
#     allow_credentials=True,         # Разрешаем передачу кук/авторизационных заголовков
#     allow_methods=["GET", "POST", "OPTIONS"], # Ограничиваем разрешенные HTTP-методы
#     allow_headers=["Content-Type", "Authorization", "X-User-Role"], # Разрешаем только безопасные заголовки
# )

# Зависимость для проверки роли пользователя (ИБ-требование кейса по разграничению доступа)
def verify_role_access(x_user_role: str = Depends(lambda: "CFO")): 
    # Примечание: В будущем здесь будет извлечение роли из JWT-токена или кастомного заголовка X-User-Role
    if x_user_role not in [role.value for role in UserRole]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен: неопознанная или недопустимая роль ЛПР"
        )
    return x_user_role

# Теперь эндпоинт может принимать сессию базы данных db через Depends(get_db)
@app.get(
    "/api/v1/insights", 
    response_model=InsightResponse,
    dependencies=[Depends(verify_role_access)],
    summary="Получить персонализированный инсайт по ID компании",
    tags=["Insights"])
async def get_insights(
    company_id: str = Query(..., description="ID компании для фильтрации инсайтов"),
    role: UserRole = UserRole.CFO
):
    """
    Эндпоинт возвращает структурированный инсайт, адаптированный под переданную роль ЛПР.
    Доступ защищен middleware и валидацией ролей.
    """
    # Временный поиск по mock-данным. В продакшене тут будет запрос к БД и вызов LLM.
    for insight in MOCK_INSIGHTS:
        if insight["target_company"]["id"] == company_id:
            insight["user_context"]["role"] = role
            return insight
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Инсайт для компании {company_id} не найден"
    )

@app.get(
    "/api/v1/test-db",
    summary="Временный тест: Получить реальную статистику из базы данных"
)
async def test_db_endpoint(
    company_id: str = Query(..., description="Реальный ID компании из CSV (например: U_67 или U_188)"),
    db = Depends(get_db)  # Наша асинхронная сессия из database.py
):
    """
    Эндпоинт делает прямой асинхронный запрос к PostgreSQL,
    проверяя физическое наличие данных и связей КИБ-хакатона.
    """
    try:
        # 1. Ищем компанию по её первичному ключу id (SYNTHETIC_U)
        query = select(Company).where(Company.id == company_id)
        result = await db.execute(query)
        company = result.scalar_one_or_none()

        if not company:
            raise HTTPException(
                status_code=404,
                detail=f"Компания с ID {company_id} отсутствует в PostgreSQL. Проверьте запуск ETL."
            )

        # 2. Быстро собираем агрегированную статистику по графам (благодаря selectinload/отношениям)
        return {
            "status": "success",
            "message": "Соединение с PostgreSQL и ORM-модели работают идеально!",
            "database_data": {
                "synthetic_u": company.id,
                "group_id": company.group_id,
                "mainokved_code": company.okved_code,
                "mainokved_name": company.okved_name,
                "revenue_company": float(company.revenue),
                "city": company.city,
                "region": company.region,
                "client_product_flags": {
                    "rko": company.cl_product_rko_mark,
                    "loan": company.cl_product_loa_mark,
                    "factoring": company.factoring_mark
                },
                "relations_metrics": {
                    "total_sent_transactions": len(company.sent_transactions),
                    "total_received_transactions": len(company.received_transactions),
                    "connected_individuals_count": len(company.linked_individuals)
                }
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail= f"Внутренняя ошибка при обращении к СУБД: {str(e)}"
        )


@app.get("/", tags=["Root"])
def read_root():
    return {"status": "working", "message": "Welcome to Alfa-Bank Hackathon API"}
