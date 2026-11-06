
from tools.sales_analysis import get_product_sales_ranking


def test_revenue_ranking():
    results = get_product_sales_ranking(
        start_date="2026-08-01",
        end_date="2026-10-31",
        limit=5,
        sort_by="total_sales"
    )

    print("\nTOP 5 - REVENUE RANKING")
    for product in results["top_products"]:
        print(product)

    print("\nBOTTOM 5 - REVENUE RANKING")
    for product in results["bottom_products"]:
        print(product)

    assert len(results["top_products"]) == 5
    assert len(results["bottom_products"]) == 5
    assert results["sort_by"] == "total_sales"

    metric = results["sort_by"]

    top_values = [
        product[metric]
        for product in results["top_products"]
    ]

    bottom_values = [
        product[metric]
        for product in results["bottom_products"]
    ]

    assert top_values == sorted(top_values, reverse=True)
    assert bottom_values == sorted(bottom_values)


def test_quantity_ranking():
    results = get_product_sales_ranking(
        start_date="2026-08-01",
        end_date="2026-10-31",
        limit=5,
        sort_by="total_quantity"
    )

    print("\nTOP 5 - QUANTITY RANKING")
    for product in results["top_products"]:
        print(product)

    print("\nBOTTOM 5 - QUANTITY RANKING")
    for product in results["bottom_products"]:
        print(product)

    assert len(results["top_products"]) == 5
    assert len(results["bottom_products"]) == 5
    assert results["sort_by"] == "total_quantity"

    metric = results["sort_by"]

    top_values = [
        product[metric]
        for product in results["top_products"]
    ]

    bottom_values = [
        product[metric]
        for product in results["bottom_products"]
    ]

    assert top_values == sorted(top_values, reverse=True)
    assert bottom_values == sorted(bottom_values)


if __name__ == "__main__":
    test_revenue_ranking()
    test_quantity_ranking()
