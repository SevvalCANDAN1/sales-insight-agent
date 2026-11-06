from strands import tool
from database.queries import fetch_sales_data

@tool
def get_product_sales_ranking(
    start_date: str,
    end_date: str,
    limit: int = 5,
    sort_by: str = "total_sales"
) -> dict:
    """
        Ranks products by total sales revenue or quantity sold.

        Args:
            start_date: Start date (YYYY-MM-DD).
            end_date: End date (YYYY-MM-DD).
            limit: Number of products to display in each ranking.
            sort_by: Ranking metric. Use "total_sales" for revenue
                    or "total_quantity" for quantity sold.

        Returns:
            Top and bottom products according to the selected metric.
    """

    if limit < 1 or limit > 20:
        raise ValueError("Limit must be between 1 and 20.")

    products = fetch_sales_data(
        start_date=start_date,
        end_date=end_date,
        group_by="product"
    )

    if not products:
        return {
            "top_products": [],
            "bottom_products": [],
            "sort_by": sort_by,
            "message": "No sales data found for the specified date range."
        }

    sorted_products = sorted(
        products,
        key=lambda x: x[sort_by],
        reverse=True
    )
    
    return {
        "top_products": sorted_products[:limit],
        "bottom_products": sorted_products[-limit:][::-1],
        "sort_by": sort_by
    }
