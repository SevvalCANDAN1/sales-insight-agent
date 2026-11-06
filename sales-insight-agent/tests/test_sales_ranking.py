from tools.sales_analysis import get_product_sales_ranking

def test_product_sales_ranking():
    results = get_product_sales_ranking(
        start_date="2026-08-01",
        end_date="2026-10-31",
        limit=5
    )

    print("\nEN ÇOK SATAN 5 ÜRÜN\n")
    for product in results["top_products"]:
        print(product["group_name"], product["total_sales"])

    print("\nEN AZ SATAN 5 ÜRÜN\n")
    for product in results["bottom_products"]:
        print(product["group_name"], product["total_sales"])

    assert len(results["top_products"]) == 5
    assert len(results["bottom_products"]) == 5

    top_sales = [p["total_sales"] for p in results["top_products"]]
    bottom_sales = [p["total_sales"] for p in results["bottom_products"]]

    assert top_sales == sorted(top_sales, reverse=True)
    assert bottom_sales == sorted(bottom_sales)

    print("\nTest başarılı!")

if __name__ == "__main__":
    test_product_sales_ranking()