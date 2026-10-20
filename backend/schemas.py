from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

# ==========================================
# 1. ВСПОМОГАТЕЛЬНЫЕ ПЕРЕЧИСЛЕНИЯ (ENUMS)
# ==========================================

class UserRole(str, Enum):
    CEO = "CEO"
    CFO = "CFO"
    CHIEF_ACCOUNTANT = "ChiefAccountant"
    TREASURY_HEAD = "TreasuryHead"


class BankProductEnum(str, Enum):
    RKO = "cl_product_rko_mark"
    GUARANTEE = "cl_product_gar_mark"
    LOAN = "cl_product_loa_mark"
    LEASING = "cl_product_lea_mark"
    DEPOSIT = "cl_product_dep_mark"
    ZPP = "cl_product_zpp_mark"
    FACTORING = "factoring_mark"

# ==========================================
# 2. СХЕМЫ ДЛЯ ПОДТЯГИВАНИЯ СВЯЗАННЫХ СУЩНОСТЕЙ (ГРАФЫ)
# ==========================================

class TransactionSchema(BaseModel):
    """Схема транзакции для отображения в графе связей"""
    id: int
    payer_id: str = Field(..., description="ID компании-отправителя")
    beneficiary_id: str = Field(..., description="ID company-получателя")
    pay_amt: float = Field(..., description="Совокупный объем платежей")
    pay_cnt: int = Field(..., description="Количество транзакций")
    created_at: datetime

    class Config:
        from_attributes = True


class IndividualLinkSchema(BaseModel):
    """Схема связи физлица с компанией"""
    id: int
    synthetic_f: str = Field(..., description="ID связанного физлица")
    synthetic_u: str = Field(..., description="ID связанной компании")
    city_name: str = Field(..., description="Город проживания физлица")
    rc_name: str = Field(..., description="Регион проживания физлица")
    created_at: datetime

    class Config:
        from_attributes = True

# ==========================================
# 3. СХЕМА ПРОФИЛЯ КОМПАНИИ (АКТУАЛЬНЫЙ MODELS)
# ==========================================

class TargetCompanySchema(BaseModel):
    """Полный профиль компании, полностью синхронизированный с models.py"""
    id: str = Field(..., description="SYNTHETIC_U: Уникальный ID компании")
    group_id: Optional[str] = Field(None, description="GROUP_ID: ID группы компаний")
    org_type: str = Field(..., description="ORG_TYPE: Тип организации")
    okfs_name: str = Field(..., description="OKFS_NAME: Форма собственности")
    revenue: float = Field(..., description="REVENUE_COMPANY: Годовая выручка")
    company_age_gradation: str = Field(..., description="COMPANY_AGE_YEARS_GRADATION")
    eco_mark_label: str = Field(..., description="ECO_MARK_LABEL")
    negative_mark: bool = Field(..., description="NEGATIVEMARK")
    okved_code: str = Field(..., description="MAINOKVED_CODE")
    okved_name: str = Field(..., description="MAINOKVED_NAME")
    workers_fns: str = Field(..., description="AMOUNT_WORKERS_FNS_GRADATION")
    workers_spark: str = Field(..., description="AMOUNT_WORKERS_SPARK_GRADATION")
    city: str = Field(..., description="CITY")
    region: str = Field(..., description="REGION")
    cl_type: str = Field(..., description="CL_TYPE")
    
    # Флаги продуктов Альфа-Банка
    cl_product_rko_mark: bool
    cl_product_gar_mark: bool
    cl_product_loa_mark: bool
    cl_product_lea_mark: bool
    cl_product_dep_mark: bool
    cl_product_zpp_mark: bool
    fts_flag: bool
    fts_country_name: Optional[str] = None
    factoring_mark: bool

    class Config:
        from_attributes = True

# ==========================================
# 4. СХЕМЫ ДЛЯ ИНТЕРПРЕТАЦИИ И ТРАССИРУЕМОСТИ AI
# ==========================================

class UserContextSchema(BaseModel):
    role: UserRole
    comment: str


class NewsSourceSchema(BaseModel):
    title: str = Field(..., description="Заголовок обрабатываемой внешней новости")
    publish_date: str = Field(..., description="Дата публикации новости в виде строки") # <-- ИЗМЕНЕНО с datetime на str



class AiInterpretationSchema(BaseModel):
    what_happened: str = Field(..., description="Ответ ИИ: Что произошло")
    why_it_matters: str = Field(..., description="Ответ ИИ: Почему важно для этой компании")
    bank_expert_opinion: str = Field(..., description="Мнение экспертов Альфы из RAG")
    suggested_actions: List[str] = Field(..., description="Рекомендованные шаги")


class RagMaterialReference(BaseModel):
    id: int
    title: str


class TraceabilitySchema(BaseModel):
    """Блок прозрачности инсайта (Критерий №12)"""
    ai_model: str
    matched_rag_materials: List[RagMaterialReference]
    # Позволяет фронтенду отобразить, сколько связей и транзакций проанализировал агент
    analyzed_transactions_count: int
    analyzed_individuals_count: int


class NativeAdSchema(BaseModel):
    """Контекстное предложение продуктов КИБ на основе отсутствующих флагов"""
    product_to_offer: BankProductEnum
    title: str
    description: str
    action_url: str

# ==========================================
# 5. ИТОГОВЫЙ СТРУКТУРИРОВАННЫЙ ОТВЕТ API
# ==========================================

class InsightResponse(BaseModel):
    """Валидированный контракт ответа API для Фронтенда"""
    insight_id: str
    target_company: TargetCompanySchema
    user_context: UserContextSchema
    news_source: NewsSourceSchema
    ai_interpretation: AiInterpretationSchema
    traceability: TraceabilitySchema
    native_ad: Optional[NativeAdSchema] = None

    class Config:
        from_attributes = True


# ==========================================
# 6. СКОРРЕКТИРОВАННЫЙ MOCK ДЛЯ ФРОНТЕНДА
# ==========================================
MOCK_INSIGHTS: List[dict] = [
    {
        "insight_id": "ins_2026_999",
        "target_company": {
            "id": "COMP_A_15_BILLION",
            "group_id": "GROUP_ALPHA_METAL",
            "org_type": "АО",
            "okfs_name": "ЧАСТНАЯ СОБСТВЕННОСТЬ",
            "revenue": 18500000000.00,
            "company_age_gradation": "5-10 лет",
            "eco_mark_label": "Стабильный рост",
            "negative_mark": False,
            "okved_code": "24.1",
            "okved_name": "Производство чугуна, стали и ферросплавов",
            "workers_fns": "500-1000",
            "workers_spark": "600-1100",
            "city": "г. Череповец",
            "region": "Вологодская область",
            "cl_type": "CLIENT",
            "cl_product_rko_mark": True,
            "cl_product_gar_mark": False,
            "cl_product_loa_mark": True,
            "cl_product_lea_mark": False,
            "cl_product_dep_mark": True,
            "cl_product_zpp_mark": True,
            "fts_flag": True,
            "fts_country_name": "КИТАЙ",
            "factoring_mark": False
        },
        "user_context": {
            "role": "CFO",
            "comment": "Инсайт сгенерирован под боли Финансового директора (ликвидность, валютные риски)"
        },
        "news_source": {
            "title": "Введение новых экспортных пошлин на металлы со стороны КНР",
            "publish_date": "2026-10-19T14:30:00Z"
        },
        "ai_interpretation": {
            "what_happened": "Правительство КНР пересматривает таможенные тарифы на экспорт компонентов для металлургии с ноября 2026 года.",
            "why_it_matters": "Ваша компания импортирует сырье из Китая (подтверждено данными ФТС). Объемы входящих платежей вашим контрагентам-поставщикам за последние 3 месяца выросли. Рост пошлин увеличит себестоимость производства по вашему ОКВЭД 24.1 на 4.5%.",
            "bank_expert_opinion": "Согласно обзору Центра макроэкономических исследований Альфа-Банка 'Commodities performance (Август 2026)', волатильность на рынке промышленных металлов останется высокой до конца 3-го квартала. Банк рекомендует захеджировать риски.",
            "suggested_actions": [
                "Провести аудит цепочки поставок с привлечением контрагентов из пула вашей группы.",
                "Использовать инструменты торгового финансирования для минимизации кассовых разрывов."
            ]
        },
        "traceability": {
            "ai_model": "DeepSeek-V4.1-Flash",
            "matched_rag_materials": [
                {"id": 104, "title": "Commodities performance, август 2026"}
            ],
            "analyzed_transactions_count": 389,
            "analyzed_individuals_count": 12
        },
        "native_ad": {
            "product_to_offer": "factoring_mark",
            "title": "Факторинг от Альфа-Банка",
            "description": "У вас не подключен факторинг. Покройте кассовые разрывы из-за задержек поставок из Китая. Получите до 90% от суммы контракта сразу.",
            "action_url": "/api/v1/products/factoring/apply"
        }
    }
]
