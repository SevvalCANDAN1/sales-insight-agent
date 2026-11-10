from agent.sales_agent import create_sales_agent
from evaluations.test_cases import TEST_CASES

from strands.hooks import BeforeToolCallEvent


def normalize_parameters(params):
    """Normalize tool parameters for comparison."""
    return dict(params)


def evaluate_tool_call(actual_call, expected_tool, expected_parameters):
    """Compare the actual tool call with the expected tool and parameters."""

    actual_tool = actual_call["tool_name"]
    actual_parameters = normalize_parameters(actual_call["parameters"])

    tool_pass = actual_tool == expected_tool

    parameter_results = {}

    for key, expected_value in expected_parameters.items():
        actual_value = actual_parameters.get(key)

        parameter_results[key] = {
            "expected": expected_value,
            "actual": actual_value,
            "pass": actual_value == expected_value
        }

    parameters_pass = all(
        result["pass"]
        for result in parameter_results.values()
    )

    overall_pass = tool_pass and parameters_pass

    return {
        "tool_pass": tool_pass,
        "parameters_pass": parameters_pass,
        "overall_pass": overall_pass,
        "actual_tool": actual_tool,
        "actual_parameters": actual_parameters,
        "parameter_results": parameter_results,
    }


def run_evaluation(test_case):

    print("\n" + "=" * 60)
    print(f"TEST: {test_case['id']}")
    print("=" * 60)

    print(f"\nQUESTION:")
    print(test_case["question"])

    expected_tool = test_case["expected_tool"]
    expected_parameters = test_case["expected_parameters"]

    print("\nEXPECTED TOOL:")
    print(expected_tool)

    print("\nEXPECTED PARAMETERS:")
    print(expected_parameters)

    captured_tool_calls = []

    agent = create_sales_agent()

    def capture_tool_call(event: BeforeToolCallEvent):
        tool_use = event.tool_use

        captured_tool_calls.append({
            "tool_name": tool_use["name"],
            "parameters": tool_use.get("input", {})
        })

    agent.add_hook(
        capture_tool_call,
        BeforeToolCallEvent
    )

    print("\nAGENT RESPONSE:\n")

    try:
        response = agent(test_case["question"])
        print(response)
    except Exception as e:
        print(f"\nAgent failed during execution: {e}")

        return {
            "test_id": test_case["id"],
            "status": "FAIL",
            "reason": "Agent execution error"
        }

    print("\n" + "-" * 60)
    print("CAPTURED TOOL CALLS")
    print("-" * 60)

    if not captured_tool_calls:
        print("No tool call was captured.")

        return {
            "test_id": test_case["id"],
            "status": "FAIL",
            "reason": "No tool call captured"
        }

    for index, call in enumerate(captured_tool_calls, start=1):
        print(f"\nTool Call #{index}")
        print(f"Tool: {call['tool_name']}")
        print(f"Parameters: {call['parameters']}")

    # Compare the first captured tool call with the expected call for now.
    actual_call = captured_tool_calls[0]

    result = evaluate_tool_call(
        actual_call,
        expected_tool,
        expected_parameters
    )

    print("\n" + "-" * 60)
    print("EVALUATION")
    print("-" * 60)

    print(
        f"\nTool name: "
        f"{'PASS' if result['tool_pass'] else 'FAIL'}"
    )

    print(
        f"Expected: {expected_tool}"
    )

    print(
        f"Actual:   {result['actual_tool']}"
    )

    print("\nParameters:")

    for key, parameter_result in result["parameter_results"].items():

        status = "PASS" if parameter_result["pass"] else "FAIL"

        print(
            f"  {key}: {status}"
        )

        print(
            f"      Expected: {parameter_result['expected']}"
        )

        print(
            f"      Actual:   {parameter_result['actual']}"
        )

    print("\n" + "=" * 60)

    if result["overall_pass"]:
        print("STATUS: PASS")
    else:
        print("STATUS: FAIL")

    print("=" * 60)

    result["test_id"] = test_case["id"]
    return result


def main():

    results = []

    for test_case in TEST_CASES:
        result = run_evaluation(test_case)
        results.append(result)

    print("\n\n" + "=" * 60)
    print("FINAL EVALUATION SUMMARY")
    print("=" * 60)

    passed = 0
    failed = 0

    for result in results:

        status = result["status"] \
            if "status" in result \
            else (
                "PASS"
                if result["overall_pass"]
                else "FAIL"
            )

        print(
            f"{result['test_id']}: {status}"
        )

        if status == "PASS":
            passed += 1
        else:
            failed += 1

    print("\n" + "-" * 60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {len(results)}")

    if failed == 0:
        print("\nOverall: PASS")
    else:
        print("\nOverall: FAIL")


if __name__ == "__main__":
    main()
