from strands import tool
from database.queries import fetch_sales_data

@tool
def get_sales_data(
    start_date: str,
    end_date: str,
    product_name: str = "",
    region_name: str = "",
    group_by: str = "month"
) -> list:
    """
        Retrieves sales data for the specified date range. 

        Args:
            start_date: Start date (YYYY-MM-DD). 
            end_date: End date (YYYY-MM-DD). 
            product_name: Optional filter for product name. 
            region_name: Optional filter for region name. 
            group_by: Grouping type (month, product, or region). 

        Returns:
            A list containing the sales amount, product quantity, and record count.
    """
    results = fetch_sales_data(
        start_date=start_date,
        end_date=end_date,
        product_name=product_name,
        region_name=region_name,
        group_by=group_by
    )

    return results
