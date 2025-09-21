import yaml
import numpy as np
from coe import ClassicalOrbitalElements

def run_test_case(test):
    """Run one test case and check results against expected values."""
    r = np.array(test["r"])
    v = np.array(test["v"])
    expected = test.get("expected", {})
    tol = expected.get("tolerance", 1e-3)

    coe = ClassicalOrbitalElements(r, v)
    results = coe.calculate()

    errors = []
    for key, exp_val in expected.items():
        if key == "tolerance":
            continue
        calc_val = results[key]
        if not np.isclose(calc_val, exp_val, atol=tol, rtol=0):
            errors.append(
                f"{key}: expected {exp_val}, got {calc_val:.4f} (tol={tol})"
            )

    return errors

def main():
    with open("test_cases.yaml", "r") as f:
        test_data = yaml.safe_load(f)

    all_passed = True
    for test in test_data["test_cases"]:
        print(f"Running test: {test['name']}...")
        errors = run_test_case(test)
        if errors:
            all_passed = False
            print(" ❌ FAIL")
            for err in errors:
                print("   ", err)
        else:
            print(" ✅ PASS")

    if all_passed:
        print("\nAll tests passed successfully!")
    else:
        print("\nSome tests failed. Please review the error messages.")

if __name__ == "__main__":
    main()
