from tools.sales_data import get_sales_data


def test_sales_tool():
    results = get_sales_data(
        start_date="2026-08-01",
        end_date="2026-10-31",
        group_by="month"
    )

    print("\nSTRANDS SALES TOOL TESTİ\n")

    for row in results:
        print(row)

    assert len(results) == 3
    print("\nTest başarılı!")


if __name__ == "__main__":
    test_sales_tool()