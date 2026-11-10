
import os
import random
import psycopg2
from psycopg2.extras import execute_values
from datetime import date, timedelta
from decimal import Decimal

from dotenv import load_dotenv

load_dotenv()

random.seed(42)


def get_admin_connection():
    """
    Connects as the database owner, since seeding needs write access
    that the read-only agent user does not have.
    """
    required_variables = [
        "DB_HOST",
        "DB_PORT",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD"
    ]
    missing = [
        variable
        for variable in required_variables
        if not os.getenv(variable)
    ]

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )


PRODUCTS = [
    ("Laptop", "Elektronik", 35000),
    ("Telefon", "Elektronik", 22000),
    ("Tablet", "Elektronik", 15000),
    ("Kulaklık", "Elektronik", 2500),
    ("Monitör", "Elektronik", 8000),
    ("Klavye", "Aksesuar", 1800),
    ("Mouse", "Aksesuar", 900),
    ("Yazıcı", "Elektronik", 6500),
    ("Ofis Koltuğu", "Mobilya", 7500),
    ("Çalışma Masası", "Mobilya", 9000),
    ("Kitaplık", "Mobilya", 5500),
    ("Kanepe", "Mobilya", 25000),
    ("Mont", "Giyim", 4000),
    ("Ayakkabı", "Giyim", 3000),
    ("Tişört", "Giyim", 750),
    ("Pantolon", "Giyim", 1800),
    ("Klima", "Ev Aletleri", 18000),
    ("Buzdolabı", "Ev Aletleri", 32000),
    ("Çamaşır Makinesi", "Ev Aletleri", 24000),
    ("Kahve Makinesi", "Ev Aletleri", 4500)
]


REGIONS = [
    ("Marmara", "İstanbul"),
    ("İç Anadolu", "Ankara"),
    ("Ege", "İzmir"),
    ("Akdeniz", "Antalya"),
    ("Karadeniz", "Trabzon")
]


MONTH_FACTORS = {
    1: 0.90,
    2: 0.85,
    3: 1.00,
    4: 1.05,
    5: 1.10,
    6: 1.15,
    7: 1.20,
    8: 1.10,
    9: 0.95,
    10: 1.00,
    11: 1.15,
    12: 1.30
}


START_DATE = date(2025, 11, 1)
END_DATE = date(2026, 10, 31)


def generate_sales(product_ids, region_ids):
    sales = []

    days = (END_DATE - START_DATE).days

    for _ in range(5000):
        sale_date = START_DATE + timedelta(
            days=random.randint(0, days)
        )

        product_name, category, base_price = random.choice(PRODUCTS)

        product_id = product_ids[product_name]
        region_id = random.choice(list(region_ids.values()))

        quantity = random.randint(1, 10)

   
        quantity = max(
            1,
            round(quantity * MONTH_FACTORS[sale_date.month])
        )

        price_variation = random.uniform(0.90, 1.10)

        unit_price = Decimal(
            str(round(base_price * price_variation, 2))
        )

        sales.append((
            product_id,
            region_id,
            sale_date,
            quantity,
            unit_price
        ))

    return sales


def main():
    connection = None

    try:
        connection = get_admin_connection()

        with connection:
            with connection.cursor() as cursor:

                cursor.execute("""
                    SELECT
                        (SELECT COUNT(*) FROM products),
                        (SELECT COUNT(*) FROM regions),
                        (SELECT COUNT(*) FROM sales);
                """)

                counts = cursor.fetchone()

                if any(counts):
                    raise RuntimeError(
                        "Tablolarda zaten veri var. "
                        "Tekrar veri eklenmedi."
                    )

      
                cursor.executemany(
                    """
                    INSERT INTO products (product_name, category)
                    VALUES (%s, %s)
                    """,
                    [(p[0], p[1]) for p in PRODUCTS]
                )

                cursor.execute(
                    "SELECT product_id, product_name FROM products"
                )

                product_ids = {
                    name: product_id
                    for product_id, name in cursor.fetchall()
                }

           
                cursor.executemany(
                    """
                    INSERT INTO regions (region_name, city)
                    VALUES (%s, %s)
                    """,
                    REGIONS
                )

                cursor.execute(
                    "SELECT region_id, region_name FROM regions"
                )

                region_ids = {
                    name: region_id
                    for region_id, name in cursor.fetchall()
                }

                sales_data = generate_sales(
                    product_ids,
                    region_ids
                )

        
                execute_values(
                    cursor,
                    """
                    INSERT INTO sales (
                        product_id,
                        region_id,
                        sale_date,
                        quantity,
                        unit_price
                    )
                    VALUES %s
                    """,
                    sales_data,
                    page_size=1000
                )

                print("Sentetik veriler başarıyla eklendi!")
                print(f"Ürün sayısı: {len(PRODUCTS)}")
                print(f"Bölge sayısı: {len(REGIONS)}")
                print(f"Satış kaydı: {len(sales_data)}")

    except Exception as error:
        print("Hata oluştu:", error)
        raise

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    main()
