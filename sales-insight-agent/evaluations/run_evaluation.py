from datetime import date

from agent.sales_agent import create_sales_agent
from evaluations.test_cases import TEST_CASES


def run_evaluation():
    agent = create_sales_agent()

    for test_case in TEST_CASES:
        print("=" * 60)
        print(f"TEST: {test_case['id']}")
        print(f"SORU: {test_case['question']}")
        print("=" * 60)

        try:
            response = agent(test_case["question"])

            print("\nAGENT RESPONSE:")
            print(response)

            print("\nEXPECTED TOOL:")
            print(test_case["expected_tool"])

            print("\nEXPECTED PARAMETERS:")
            print(test_case["expected_parameters"])

            print("\nSTATUS: RESPONSE GENERATED")

        except Exception as e:
            print("\nSTATUS: FAILED")
            print(f"ERROR: {e}")


if __name__ == "__main__":
    run_evaluation()