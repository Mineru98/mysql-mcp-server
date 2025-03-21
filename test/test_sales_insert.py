# -*- coding:utf-8 -*-
from pprint import pprint

import numpy as np
import pandas as pd
import pymysql
import pymysql.cursors
from pymysql.err import OperationalError
from tqdm import tqdm


# MySQL 연결 설정
def create_db_connection():
    try:
        connection = pymysql.connect(
            host="localhost",  # 호스트명
            database="mcp_test",  # 데이터베이스 이름
            user="root",  # MySQL 사용자 이름
            password="mcpTest1234!!!",  # MySQL 비밀번호
            charset="utf8mb4",  # 문자 인코딩
            cursorclass=pymysql.cursors.DictCursor,
        )
        print("Successfully connected to MySQL database")
        return connection
    except OperationalError as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


# 테이블 생성 함수
def create_table(connection):
    try:
        with connection.cursor() as cursor:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS sales_data (
                ID INT AUTO_INCREMENT PRIMARY KEY COMMENT '고유 식별자로 자동 증가하는 기본 키',
                YEAR INT NOT NULL COMMENT '데이터가 기록된 연도 (예: 2020)',
                MONTH INT NOT NULL CHECK (MONTH BETWEEN 1 AND 12) COMMENT '데이터가 기록된 월 (1~12, 예: 1은 1월)',
                SUPPLIER VARCHAR(255) DEFAULT NULL COMMENT '주류를 공급한 업체 이름 (예: REPUBLIC NATIONAL DISTRIBUTING CO), NULL 허용',
                ITEM_CODE VARCHAR(50) NOT NULL COMMENT '품목을 식별하는 고유 코드 (예: 100009)',
                ITEM_DESCRIPTION VARCHAR(255) NOT NULL COMMENT '품목의 상세 설명 및 용량 (예: BOOTLEG RED - 750ML)',
                ITEM_TYPE VARCHAR(50) NOT NULL COMMENT '주류 유형 (예: WINE, BEER, LIQUOR, NON-ALCOHOL)',
                RETAIL_SALES FLOAT DEFAULT NULL COMMENT '소매점에서 소비자에게 판매된 금액 또는 수량 (예: 0.82, 단위 미확인), NULL 허용',
                RETAIL_TRANSFERS FLOAT DEFAULT NULL COMMENT '소매점 간 이동하거나 재고 조정 수량 (예: 1), NULL 허용',
                WAREHOUSE_SALES FLOAT DEFAULT NULL COMMENT '창고에서 판매된 수량 (예: 2), NULL 허용'
            );
            """
            cursor.execute(create_table_query)
            connection.commit()
            print("Table created successfully")
    except Exception as e:
        print(f"Error while creating table: {e}")


def preprocess_record(record):
    """NaN 및 NumPy 타입을 SQL 친화적으로 변환"""
    return tuple(
        (
            None
            if pd.isna(x)
            else x.item() if isinstance(x, (np.integer, np.floating)) else x
        )
        for x in record
    )


# 데이터 삽입 함수
def insert_data(connection, df, chunk_size=1000):
    try:
        # DataFrame을 레코드 리스트로 변환
        records = df.to_records(index=False)
        total_rows = len(records)

        # chunk 단위로 데이터 삽입
        with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO sales_data (
                YEAR, MONTH, SUPPLIER, ITEM_CODE, ITEM_DESCRIPTION, 
                ITEM_TYPE, RETAIL_SALES, RETAIL_TRANSFERS, WAREHOUSE_SALES
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            with tqdm(total=total_rows, desc="Inserting data") as pbar:
                for i in range(0, total_rows, chunk_size):
                    chunk = [
                        preprocess_record(records[j])
                        for j in range(i, min(i + chunk_size, total_rows))
                    ]
                    cursor.executemany(insert_query, chunk)
                    pbar.update(len(chunk))
            connection.commit()

            print(f"Successfully inserted {total_rows} rows")

    except Exception as e:
        pprint(chunk)
        print(f"Error while inserting data: {e}")


# 메인 실행
def main():
    file = "Warehouse_and_Retail_Sales.csv"
    df = pd.read_csv(file)

    object_columns = df.select_dtypes(include=["object"]).columns
    df[object_columns] = df[object_columns].astype(str)

    # 데이터베이스 연결
    connection = create_db_connection()
    if connection:
        create_table(connection)
        insert_data(connection, df)
        connection.close()
        print("Database connection closed")


if __name__ == "__main__":
    main()
