class StoryManager:
    def __init__(self):
        self.flags = {}
        self.variables = {}

    def set_flag(self, flag, value):
        self.flags[flag] = value

    def get_flag(self, flag):
        return self.flags.get(flag, False)

    def update_on_action(self, action):
        if action == "collect_artifact":
            self.set_flag("artifact_collected", True)
            if self.get_flag("artifact_collected") and self.get_flag(
                "defeated_minions"
            ):
                self.set_flag("can_defeat_boss", True)

    def get_ending(self, completion_percent):
        if completion_percent > 80:
            return "good"
        elif completion_percent > 50:
            return "neutral"
        else:
            return "bad"
