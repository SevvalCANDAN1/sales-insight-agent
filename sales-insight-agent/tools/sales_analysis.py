from strands import tool
from database.queries import fetch_sales_data

@tool
def get_product_sales_ranking(
    start_date: str,
    end_date: str,
    limit: int = 5
) -> dict:
    """
        Ranks products by sales amount, identifying those with the highest and lowest sales within the specified date range. 

        Args:
        start_date: Start date (YYYY-MM-DD). 
        end_date: End date (YYYY-MM-DD). 
        limit: The number of products to display for both the top and bottom rankings. 

        Returns:
        A list of the products with the highest and lowest sales.
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
            "message": "No sales data found for the specified date range."
        }

    sorted_products = sorted(
        products, 
        key=lambda x: x['total_sales'], 
        reverse=True)
    
    return {
        "top_products": sorted_products[:limit],
        "bottom_products": sorted_products[-limit:][::-1]
    }
