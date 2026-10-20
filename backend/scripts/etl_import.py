import os
import sys
import csv
import asyncio
from typing import Generator, List, Dict, Any
from sqlalchemy import insert, select
from sqlalchemy.dialects.postgresql import insert as pg_insert

# Пробрасываем путь к родительской директории бэкенда для работы импортов
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import async_session_maker, engine
from models import Company, CompanyIndividualLink, Transaction

# Пути к реальным файлам данных из Google Диска
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
COMPANIES_CSV = os.path.join(DATA_DIR, "df_Uid_data_hack.csv")
LINKS_CSV = os.path.join(DATA_DIR, "df_Fid_Uid_link_hack.csv")
PAYMENTS_CSV = os.path.join(DATA_DIR, "df_Uid_payment_hack.csv")

CHUNK_SIZE = 1000  # Размер пакета для итераций импорта


def read_csv_in_chunks(file_path: str, chunk_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    """Считывает CSV-файл порциями с автоопределением разделителя и нормализацией заголовков"""
    if not os.path.exists(file_path):
        print(f"[ERROR] Файл не найден по пути: {file_path}")
        return

    with open(file_path, mode="r", encoding="utf-8-sig") as file:
        # Проверяем первую строчку, чтобы определить разделитель (запятая или точка с запятой)
        first_line = file.readline()
        delimiter = ";" if ";" in first_line else ","
        file.seek(0) # Возвращаем указатель в начало файла

        reader = csv.DictReader(file, delimiter=delimiter)
        chunk = []
        for row in reader:
            # Нормализуем ключи: удаляем пробелы и переводим в ВЕРХНИЙ регистр для стабильности
            normalized_row = {str(k).strip().upper(): v for k, v in row.items() if k is not None}
            chunk.append(normalized_row)
            
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk


def cast_to_bool(value: Any) -> bool:
    """Безопасно преобразует строковые флаги из CSV в логический тип Python"""
    if not value:
        return False
    val_str = str(value).strip().lower()
    return val_str in ("1", "true", "yes", "t", "y", "1.0")


async def import_companies():
    """Асинхронный импорт юридических лиц (df_Uid_data_hack.csv) с защитой от дублей"""
    print("[ETL] Старт импорта компаний...")
    count = 0

    async with async_session_maker() as session:
        for chunk in read_csv_in_chunks(COMPANIES_CSV, CHUNK_SIZE):
            batch = []
            for row in chunk:
                batch.append({
                    "id": row["SYNTHETIC_U"],
                    "group_id": row.get("GROUP_ID") if row.get("GROUP_ID") else None,
                    "org_type": row.get("ORG_TYPE", "Не указан"),
                    "okfs_name": row.get("OKFS_NAME", "Не указан"),
                    "revenue": float(row["REVENUE_COMPANY"]) if row.get("REVENUE_COMPANY") else 0.0,
                    "company_age_gradation": row.get("COMPANY_AGE_YEARS_GRADATION", "Не указан"),
                    "eco_mark_label": row.get("ECO_MARK_LABEL", "Не указан"),
                    "negative_mark": cast_to_bool(row.get("NEGATIVEMARK")),
                    "okved_code": row.get("MAINOKVED_CODE", "Не указан"),
                    "okved_name": row.get("MAINOKVED_NAME", "Не указан"),
                    "workers_fns": row.get("AMOUNT_WORKERS_FNS_GRADATION", "Не указан"),
                    "workers_spark": row.get("AMOUNT_WORKERS_SPARK_GRADATION", "Не указан"),
                    "city": row.get("CITY", "Не указан"),
                    "region": row.get("REGION", "Не указан"),
                    "cl_type": row.get("CL_TYPE", "действующий клиент"),
                    "cl_product_rko_mark": cast_to_bool(row.get("CL_PRODUCT_RKO_MARK")),
                    "cl_product_gar_mark": cast_to_bool(row.get("CL_PRODUCT_GAR_MARK")),
                    "cl_product_loa_mark": cast_to_bool(row.get("CL_PRODUCT_LOA_MARK")),
                    "cl_product_lea_mark": cast_to_bool(row.get("CL_PRODUCT_LEA_MARK")),
                    "cl_product_dep_mark": cast_to_bool(row.get("CL_PRODUCT_DEP_MARK")),
                    "cl_product_zpp_mark": cast_to_bool(row.get("CL_PRODUCT_ZPP_MARK")),
                    "fts_flag": cast_to_bool(row.get("FTS_FLAG")),
                    "fts_country_name": row.get("FTS_COUNTRY_NAME") if row.get("FTS_COUNTRY_NAME") else None,
                    "factoring_mark": cast_to_bool(row.get("FACTORING_MARK"))
                })
            
            # [ИСПРАВЛЕНИЕ] Переходим на pg_insert и добавляем директиву on_conflict_do_nothing
            stmt = pg_insert(Company).values(batch)
            safety_stmt = stmt.on_conflict_do_nothing(index_elements=["id"])
            
            await session.execute(safety_stmt)
            await session.commit()
            count += len(batch)
            print(f"[ETL] Обработано строк компаний: {count}")
    return count


async def import_individual_links(existing_companies: set):
    """Асинхронный импорт связей физлиц (df_Fid_Uid_link_hack.csv)"""
    print("[ETL] Старт импорта связей физлиц...")
    count = 0
    seen_links = set()  # Храним кортежи (synthetic_f, synthetic_u) для исключения дубликатов в пачке

    async with async_session_maker() as session:
        for chunk in read_csv_in_chunks(LINKS_CSV, CHUNK_SIZE):
            batch = []
            for row in chunk:
                f_id = row.get("SYNTHETIC_F")
                u_id = row.get("SYNTHETIC_U")
                # Валидация внешнего ключа: загружаем только если компания существует в базе
                if f_id and u_id and u_id in existing_companies:
                    link_key = (f_id, u_id)
                    if link_key not in seen_links:
                        seen_links.add(link_key)
                        batch.append({
                            "synthetic_f": f_id,
                            "synthetic_u": u_id,
                            "city_name": row.get("CITY_NAME", "Не указан"),
                            "rc_name": row.get("RC_NAME", "Не указан")
                        })
            
            if batch:
                await session.execute(insert(CompanyIndividualLink), batch)
                await session.commit()
                count += len(batch)
                print(f"[ETL] Загружено связей физлиц: {count}")
    return count


async def import_transactions(existing_companies: set):
    """Асинхронный импорт транзакций КИБ бизнеса (df_Uid_payment_hack.csv)"""
    print("[ETL] Старт импорта транзакций платежей...")
    count = 0
    seen_transactions = set()  # Храним кортежи (payer, beneficiary) для исключения дубликатов в пачке

    async with async_session_maker() as session:
        for chunk in read_csv_in_chunks(PAYMENTS_CSV, CHUNK_SIZE):
            batch = []
            for row in chunk:
                payer = row.get("PAYER")
                beneficiary = row.get("BENEFICIARY")
                
                # Валидация графа: оба участника платежа должны физически существовать в таблице companies
                if payer and beneficiary and payer in existing_companies and beneficiary in existing_companies:
                    tx_key = (payer, beneficiary)
                    if tx_key not in seen_transactions:
                        seen_transactions.add(tx_key)
                        batch.append({
                            "payer_id": payer,
                            "beneficiary_id": beneficiary,
                            "pay_amt": float(row["PAY_AMT"]) if row.get("PAY_AMT") else 0.0,
                            "pay_cnt": int(row["PAY_CNT"]) if row.get("PAY_CNT") else 0
                        })
            
            if batch:
                await session.execute(insert(Transaction), batch)
                await session.commit()
                count += len(batch)
                print(f"[ETL] Загружено транзакций: {count}")
    return count


async def main():
    print("=== НАЧАЛО ЗАПУСКА ОБНОВЛЕННОГО КИБ ETL ПАЙПЛАЙНА ===")
    start_time = asyncio.get_event_loop().time()
    
    # Шаг 1: Загружаем базовые профили компаний
    await import_companies()
    
    # Шаг 2: Получаем актуальный кэш всех ID компаний для валидации Foreign Keys
    async with async_session_maker() as session:
        result = await session.execute(select(Company.id))
        existing_companies = set(result.scalars().all())
    
    # Шаг 3: Параллельно/последовательно загружаем связанные файлы
    links_task = import_individual_links(existing_companies)
    tx_task = import_transactions(existing_companies)
    
    total_links, total_tx = await asyncio.gather(links_task, tx_task)
    
    end_time = asyncio.get_event_loop().time()
    print("\n=== ОТЧЕТ О ЗАГРУЗКЕ ДАННЫХ ДНЯ 2 ===")
    print(f"-> Всего компаний импортировано: {len(existing_companies)}")
    print(f"-> Всего связей физлиц (df_Fid_Uid_link_hack): {total_links}")
    print(f"-> Всего транзакций графа (df_Uid_payment_hack): {total_tx}")
    print(f"=== ETL ИМПОРТ ЗАВЕРШЕН УСПЕШНО за {end_time - start_time:.2f} сек. ===")


if __name__ == "__main__":
    asyncio.run(main())
