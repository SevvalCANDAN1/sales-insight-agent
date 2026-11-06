TEST_CASES = [
    {
        "id": "E01",
        "question": (
            "2026-08-01 ile 2026-10-31 arasında "
            "aylık satışlarımızı getir."
        ),
        "expected_tool": "get_sales_data",
        "expected_parameters": {
            "start_date": "2026-08-01",
            "end_date": "2026-10-31",
            "group_by": "month"
        },
        "expected_behavior": (
            "Üç aylık satış verisini doğru aktarmalı."
        )
    }
]