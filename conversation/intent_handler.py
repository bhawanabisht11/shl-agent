class IntentHandler:
    def __init__(self):
        self.reset()

    def reset(self):
        self.role = None
        self.level = None

    def update(self, message: str):
        text = message.lower()

        # -------- Experience --------
        if "intern" in text:
            self.level = "Intern"

        elif "entry" in text or "junior" in text:
            self.level = "Entry"

        elif "mid" in text:
            self.level = "Mid"

        elif "senior" in text:
            self.level = "Senior"

        # -------- Role --------
        if any(word in text for word in [
            "java",
            "python",
            "developer",
            "engineer",
            "sales",
            "manager",
            "analyst",
            "support",
            "tester",
            "qa",
            "data scientist"
        ]):
            self.role = message

    def is_complete(self):
        return self.role is not None and self.level is not None

    def next_question(self):
        if self.role is None:
            return "What role are you hiring for?"

        if self.level is None:
            return (
                "What experience level is the role?\n"
                "- Intern\n"
                "- Entry\n"
                "- Mid\n"
                "- Senior"
            )

        return None