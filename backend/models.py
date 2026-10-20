import datetime
from typing import List, Optional
from sqlalchemy import String, Numeric, Integer, Boolean, ForeignKey, DateTime, Text, Index, ARRAY, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    """Базовый декларативный класс для асинхронной SQLAlchemy 2.0"""
    pass


class Company(Base):
    """
    Таблица Юридических лиц. 
    Полностью мапится на df_Uid_data_hack.csv (Приложение 1)
    """
    __tablename__ = "companies"

    # Основные идентификаторы и типы
    id: Mapped[str] = mapped_column(String(50), primary_key=True, comment="SYNTHETIC_U: Уникальный ID компании")
    group_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True, comment="GROUP_ID: Идентификатор группы компаний")
    org_type: Mapped[str] = mapped_column(Text, nullable=False, comment="ORG_TYPE: Тип организации (ООО, АО и др.)")
    okfs_name: Mapped[str] = mapped_column(Text, nullable=False, comment="OKFS_NAME: Форма собственности")
    
    # Бизнес-метрики и градации
    revenue: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False, comment="REVENUE_COMPANY: Годовая выручка компании")
    company_age_gradation: Mapped[str] = mapped_column(String(50), nullable=False, comment="COMPANY_AGE_YEARS_GRADATION: Возраст компании")
    eco_mark_label: Mapped[str] = mapped_column(Text, nullable=False, comment="ECO_MARK_LABEL: Стадия развития бизнеса")
    negative_mark: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", comment="NEGATIVEMARK: Признак ключевого собственника")
    
    # Коды ОКВЭД
    okved_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True, comment="MAINOKVED_CODE: Код основного ОКВЭД")
    okved_name: Mapped[str] = mapped_column(Text, nullable=False, comment="MAINOKVED_NAME: Наименование ОКВЭД")
    
    # Численность персонала
    workers_fns: Mapped[str] = mapped_column(String(50), nullable=False, comment="AMOUNT_WORKERS_FNS_GRADATION: Персонал по ФНС")
    workers_spark: Mapped[str] = mapped_column(String(50), nullable=False, comment="AMOUNT_WORKERS_SPARK_GRADATION: Персонал по СПАРК")
    
    # География
    city: Mapped[str] = mapped_column(Text, nullable=False, comment="CITY: Город регистрации")
    region: Mapped[str] = mapped_column(Text, nullable=False, index=True, comment="REGION: Регион регистрации")
    
    # [ИСПРАВЛЕНО] Точное соответствие колонкам продуктов Альфа-Банка по ТЗ
    cl_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="CL_TYPE: Статус клиента (действующий/потенциальный)")
    cl_product_rko_mark: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", comment="CL_PRODUCT_RKO_MARK: Наличие РКО")
    cl_product_gar_mark: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", comment="CL_PRODUCT_GAR_MARK: Наличие Гарантий")
    cl_product_loa_mark: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", comment="CL_PRODUCT_LOA_MARK: Наличие Кредитов")
    cl_product_lea_mark: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", comment="CL_PRODUCT_LEA_MARK: Наличие Лизинга")
    cl_product_dep_mark: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", comment="CL_PRODUCT_DEP_MARK: Наличие Депозитов")
    cl_product_zpp_mark: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", comment="CL_PRODUCT_ZPP_MARK: Наличие Зарплатного проекта")
    
    # [ИСПРАВЛЕНО] Точное соответствие ФТС и Факторингу по ТЗ
    fts_flag: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", comment="FTS_FLAG: Наличие в базе ФТС")
    fts_country_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="FTS_COUNTRY_NAME: Страна торговли по ФТС")
    factoring_mark: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", comment="FACTORING_MARK: Наличие Факторинга")

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, server_default="NOW()")

    # [ПРОЕКТИРОВАНИЕ КАСТКАДОВ] Настройка связей на уровне SQLAlchemy ORM
    sent_transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction", 
        foreign_keys="[Transaction.payer_id]", 
        back_populates="payer", 
        lazy="selectin",
        cascade="all, delete-orphan"  # При удалении компании удаляются исходящие транзакции
    )
    received_transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction", 
        foreign_keys="[Transaction.beneficiary_id]", 
        back_populates="beneficiary", 
        lazy="selectin",
        cascade="all, delete-orphan"  # При удалении компании удаляются входящие транзакции
    )
    linked_individuals: Mapped[List["CompanyIndividualLink"]] = relationship(
        "CompanyIndividualLink", 
        back_populates="company", 
        lazy="selectin",
        cascade="all, delete-orphan"  # При удалении компании удаляются записи связей с физлицами
    )
    ai_logs: Mapped[List["AIAgentLog"]] = relationship(
        "AIAgentLog",
        back_populates="company",
        lazy="selectin"  # Без каскадного удаления (логи ИБ должны жить при удалении компании)
    )

    def __repr__(self) -> str:
        return f"<Company(id={self.id}, okved={self.okved_code}, revenue={self.revenue})>"


class CompanyIndividualLink(Base):
    """
    Таблица Связей Юридических и Физических лиц.
    Полностью мапится на df_Fid_Uid_link_hack.csv (Часть 1)
    """
    __tablename__ = "company_individual_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    synthetic_f: Mapped[str] = mapped_column(String(50), nullable=False, index=True, comment="SYNTHETIC_F: Уникальный ID физлица")
    
    # [ПРОЕКТИРОВАНИЕ КАСКАДОВ] CASCADE на уровне СУБД для обеспечения ссылочной целостности
    synthetic_u: Mapped[str] = mapped_column(
        String(50), 
        ForeignKey("companies.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True,
        comment="SYNTHETIC_U: Идентификатор связанной компании"
    )
    
    # География жизни физлица
    city_name: Mapped[str] = mapped_column(Text, nullable=False, comment="CITY_NAME: Город проживания физлица")
    rc_name: Mapped[str] = mapped_column(Text, nullable=False, comment="RC_NAME: Регион проживания физлица")
    
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, server_default="NOW()")

    # Обратная связь с компанией
    company: Mapped["Company"] = relationship("Company", back_populates="linked_individuals")

    def __repr__(self) -> str:
        return f"<IndividualLink(f_id={self.synthetic_f} -> u_id={self.synthetic_u})>"


class Transaction(Base):
    """
    Таблица Платежей/Транзакций между компаниями.
    Полностью мапится на df_Uid_payment_hack.csv (Часть 2)
    """
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # [ПРОЕКТИРОВАНИЕ КАСКАДОВ] Направленные связи графа B2B платежей с CASCADE удалением
    payer_id: Mapped[str] = mapped_column(
        String(50), 
        ForeignKey("companies.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True,
        comment="PAYER: Уникальный ID компании-отправителя"
    )
    beneficiary_id: Mapped[str] = mapped_column(
        String(50), 
        ForeignKey("companies.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True,
        comment="BENEFICIARY: Уникальный ID компании-получателя"
    )
    
    pay_amt: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False, comment="PAY_AMT: Совокупный объем платежей")
    pay_cnt: Mapped[int] = mapped_column(Integer, nullable=False, comment="PAY_CNT: Количество транзакций")
    
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, server_default="NOW()")

    # Обратные связи
    payer: Mapped["Company"] = relationship("Company", foreign_keys=[payer_id], back_populates="sent_transactions")
    beneficiary: Mapped["Company"] = relationship("Company", foreign_keys=[beneficiary_id], back_populates="received_transactions")

    def __repr__(self) -> str:
        return f"<Transaction(from={self.payer_id} to={self.beneficiary_id}, amt={self.pay_amt})>"


class BankAnalyticsRAG(Base):
    """
    База знаний внутренних экспертных материалов Альфа-Банка.
    Используется для RAG-экстракции (Приложение 2)
    """
    __tablename__ = "bank_analytics_rag"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="Название аналитического документа")
    content_chunk: Mapped[str] = mapped_column(Text, nullable=False, comment="Фрагмент/чанк текста для подачи в LLM")
    
    # Векторное поле для семантического поиска
    embedding: Mapped[Optional[List[float]]] = mapped_column(ARRAY(Float), nullable=True, comment="Векторный эмбеддинг текста")
    
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, server_default="NOW()")

    def __repr__(self) -> str:
        return f"<AnalyticsRAG(id={self.id}, title={self.title[:30]})>"


class AIAgentLog(Base):
    """
    Аудит-логирование сквозных действий ИИ для ИБ-контроля.
    (Критерий №12, Ограничение №6)
    """
    __tablename__ = "ai_agent_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(100), index=True, comment="ID сессии генерации")
    # [ПРОЕКТИРОВАНИЕ КАСКАДОВ] SET NULL для сохранения логов ИБ при удалении компании
    company_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True, comment="ID компании, по которой шел анализ (если применима)")

    agent_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True, comment="Название агента цепочки")
    llm_model: Mapped[str] = mapped_column(String(50), nullable=False, comment="Разрешенная модель из Приложения 3")

    action_step: Mapped[str] = mapped_column(String(255), nullable=False, comment="Текущий шаг (Планирование, Поиск, Анализ)")
    input_snapshot: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="Входной JSON-снимок данных для трассируемости")
    thought_process: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="Внутренние рассуждения ИИ (Chain-of-Thought)")
    output_result: Mapped[str] = mapped_column(Text, nullable=False, comment="Результат шага / выданный инсайт")

    security_flag: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", comment="Флаг детекции аномалий ИБ")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, server_default="NOW()")

    # Обратная связь для логирования
    company: Mapped["Company"] = relationship("Company", back_populates="ai_logs")
    
    def __repr__(self) -> str:
        return f"<AgentLog(id={self.id}, agent={self.agent_name}, step={self.action_step})>"


# ==============================================================================
# СОСТАВНЫЕ ВЫСОКОНАГРУЖЕННЫЕ ИНДЕКСЫ ДЛЯ ГРАФОВЫХ И ОТРAСЛЕВЫХ ВЫБОРОК
# ==============================================================================

# Оптимизация поиска: Кто кому платил внутри графа B2B
Index("ix_transactions_payer_beneficiary_amt", Transaction.payer_id, Transaction.beneficiary_id, Transaction.pay_amt)

# Оптимизация поиска: Фильтрация компаний холдинга по ОКВЭД и региону для оценки долей рынка
Index("ix_companies_okved_region_revenue", Company.okved_code, Company.region, Company.revenue)
