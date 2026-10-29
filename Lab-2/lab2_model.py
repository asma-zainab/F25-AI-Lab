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
percepts = [
    (29, True),
    (29, True),
    (20, True),
    (26, True),
    (19, True),
    (29, False),
    (29, False)
]
for step, percept in enumerate(percepts, 1):
    previous_mode = agent.previous_mode
    temp = percept[0]
    occupied = percept[1]
    target_mode, send_command = agent.act(temp, occupied)
    if send_command:
        action = "Send command"
    else:
        action = "No command"
    print("Step:", step)
    print("Previous mode:", previous_mode)
    print("Percept:", percept)
    print("Target mode:", target_mode)
    print("Action:", action)
    print()