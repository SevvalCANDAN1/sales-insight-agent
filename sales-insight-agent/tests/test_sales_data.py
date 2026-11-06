
from database.queries import fetch_sales_data


def test_last_three_months():

    results = fetch_sales_data(
        start_date="2026-08-01",
        end_date="2026-10-31",
        group_by="month"
    )

    print("\nSON 3 AYIN SATIŞ VERİLERİ\n")

    for row in results:
        print(row)

    assert len(results) == 3


if __name__ == "__main__":
    test_last_three_months()
