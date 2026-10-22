import glob
import json
import os

from sequence import analyze_sequence

TESTS_DIR = os.path.join(os.path.dirname(__file__), "..", "tests")


def load_cases(step: str):
    cases = []
    pattern = os.path.join(TESTS_DIR, f"{step}_case*_input.txt")
    for input_path in sorted(glob.glob(pattern)):
        case_name = os.path.basename(input_path).replace("_input.txt", "")
        output_path = None
        for ext in (".json", ".txt"):
            candidate = os.path.join(TESTS_DIR, f"{case_name}_output{ext}")
            if os.path.exists(candidate):
                output_path = candidate
                break
        if output_path is None:
            continue

        with open(input_path) as f:
            raw_input = f.read().rstrip("\n")
        with open(output_path) as f:
            expected = json.load(f)

        cases.append((case_name, raw_input, expected))
    return cases


def run_step1():
    cases = load_cases("step1")
    passed = 0
    for case_name, raw_input, expected in cases:
        try:
            actual = analyze_sequence(raw_input)
        except NotImplementedError:
            print(f"[SKIP] {case_name}: analyze_sequence not implemented yet")
            continue
        except Exception as e:
            print(f"[ERROR] {case_name}: raised {e!r}")
            continue

        if actual == expected:
            print(f"[PASS] {case_name}")
            passed += 1
        else:
            print(f"[FAIL] {case_name}")
            print(f"       expected: {expected}")
            print(f"       actual:   {actual}")

    print(f"\n{passed}/{len(cases)} step1 cases passed")


if __name__ == "__main__":
    run_step1()
