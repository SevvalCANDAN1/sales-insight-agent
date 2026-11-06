from tools.sales_data import get_sales_data
from tools.sales_analysis import get_product_sales_ranking


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

def test_product_ranking_tool():
    results = get_product_sales_ranking(
        start_date="2026-08-01",
        end_date="2026-10-31",
        limit=5
    )
    print("\nSTRANDS PRODUCT RANKING TOOL TESTİ\n")

    print("TOP 5 BEST-SELLING PRODUCTS:\n")
    for product in results["top_products"]:
        print(product["group_name"], product["total_sales"])
    
    print("TOP 5 WORST-SELLING PRODUCTS:\n")
    for product in results["bottom_products"]:
        print(product["group_name"], product["total_sales"])

    assert len(results["top_products"]) == 5
    assert len(results["bottom_products"]) == 5

    print("\nget_product_sales_ranking test was successful!")

if __name__ == "__main__":
    test_sales_tool()
    test_product_ranking_tool()