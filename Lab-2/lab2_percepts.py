class ClassroomAgent:
    def act(self, temp, occupied):
        if not occupied:
            return "ECO"
        elif temp > 26:
            return "COOL"
        elif temp < 20:
            return "WARM"
        else:
            return "IDLE"
agent = ClassroomAgent()
percepts = [
    (29, True),
    (29, True),
    (20, True),
    (26, True),
    (19, True),
    (29, False)
]
for step, percept in enumerate(percepts, 1):
    temp = percept[0]
    occupied = percept[1]

    mode = agent.act(temp, occupied)

    print(step, percept, "target mode:", mode)