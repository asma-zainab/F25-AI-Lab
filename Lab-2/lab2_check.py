class ClassroomAgent:
    def __init__(self):
        self.previous_mode = None
    def act(self, temp, occupied):
        if not occupied:
            target_mode = "ECO"
        elif temp > 26:
            target_mode = "COOL"
        elif temp < 20:
            target_mode = "WARM"
        else:
            target_mode = "IDLE"

        if target_mode == self.previous_mode:
            send_command = False
        else:
            send_command = True

        self.previous_mode = target_mode

        return target_mode, send_command
agent = ClassroomAgent()
tests = [
    (29, True, "COOL", True),
    (29, True, "COOL", False),
    (20, True, "IDLE", True),
    (26, True, "IDLE", False),
    (19, True, "WARM", True),
    (29, False, "ECO", True),
    (29, False, "ECO", False)
]
test_number = 1
for test in tests:
    temp = test[0]
    occupied = test[1]
    expected_mode = test[2]
    expected_command = test[3]
    actual_mode, actual_command = agent.act(temp, occupied)
    if actual_mode == expected_mode and actual_command == expected_command:
        print("Test", test_number, "Passed")
    else:
        print("Test", test_number, "Failed")
        print("Expected:", expected_mode, expected_command)
        print("Actual:", actual_mode, actual_command)
    test_number = test_number + 1
