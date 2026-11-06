from datetime import date
from psycopg2.extras import RealDictCursor
from database.connection import get_connection

GROUP_OPTIONS = {
    "month": """
        TO_CHAR(
            DATE_TRUNC('month', s.sale_date),
            'YYYY-MM'
        )
    """,
    "product": "p.product_name",
    "region": "r.region_name"
}

def fetch_sales_data(
    start_date: str,
    end_date: str,
    product_name: str = "",
    region_name: str = "",
    group_by: str = "month"
):
    """
        Retrieves sales data from PostgreSQL based on date, product, and region filters.
    """
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)

    if start > end:
        raise ValueError("Start date must be before or equal to end date.")
    if group_by not in GROUP_OPTIONS:
        raise ValueError(
            f"Invalid group_by value. Must be one of: {', '.join(GROUP_OPTIONS.keys())}"
        )
    group_expression = GROUP_OPTIONS[group_by]

    query = f"""
        SELECT
            {group_expression} AS group_name,
            SUM(s.total_amount) AS total_sales,
            SUM(s.quantity) AS total_quantity,
            COUNT(*) AS transaction_count

        FROM sales s

        JOIN products p
            ON s.product_id = p.product_id

        JOIN regions r
            ON s.region_id = r.region_id

        WHERE
            s.sale_date >= %s::date
            AND s.sale_date < (%s::date + INTERVAL '1 day')

            AND (
                %s = ''
                OR p.product_name ILIKE %s
            )

            AND (
                %s = ''
                OR r.region_name ILIKE %s
            )

        GROUP BY 1
        ORDER BY 1;
    """

    connection = get_connection()
    try:
        with connection.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                query,
                (
                    start_date,
                    end_date,
                    product_name,
                    f"%{product_name}%",
                    region_name,
                    f"%{region_name}%"
                )
            )

            rows = cursor.fetchall()

            return [
                {
                    "group_name": row["group_name"],
                    "total_sales": float(row["total_sales"]),
                    "total_quantity": int(row["total_quantity"]),
                    "transaction_count": int(
                        row["transaction_count"]
                    )
                }
                for row in rows
            ]

    finally:
        connection.close()