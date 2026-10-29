def check_application(
    score, documents_complete, cgpa, attendance
):
    if(
        score>=70 and documents_complete and cgpa>=3.2 and attendance>=80
        ):
        return "Review"
    else:
        return "Hold"
tests = [
    {
        "name": "All conditions pass",
        "input": (80, True, 3.5, 85),
        "expected": "Review",
        "reason": "All four conditions are satisfied."
    },
    {
        "name": "Cgpa condition fails",
        "input": (80, True, 3.0, 85),
        "expected": "Hold",
        "reason": "Cgpa is below than 3.2."
    },
    {
        "name": "Attendance fails",
        "input": (80, True, 3.5, 77),
        "expected": "Hold",
        "reason": "Attendance is below 80."
    },
    {
        "name": "Score boundary",
        "input": (70, True, 3.5, 85),
        "expected": "Review",
        "reason": "Score 70 meets the >= 70 threshold."
    }
]
for test in tests:
    actual = check_application(*test["input"])
    print("\nTest:", test["name"])
    print("Input:", test["input"])
    print("Expected:", test["expected"])
    print("Actual:", actual)
    print("Reason:", test["reason"])
    print("Test passed:", actual == test["expected"])