from jpath.core.step import Step


# Encapsulate query information into this `Query` class
class Query:
    def __init__(self):
        self.steps = []

    def add_step(self, step: Step):
        self.steps.append(step)
