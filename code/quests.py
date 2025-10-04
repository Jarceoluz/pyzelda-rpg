import json
from enum import Enum


class QuestState(Enum):
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


class Objective:
    def __init__(self, data):
        self.type = data["type"]  # 'kill', 'collect', etc.
        self.target = data["target"]
        self.count = data["count"]
        self.progress = 0
        self.completed = False


class Quest:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.objectives = [Objective(obj) for obj in data["objectives"]]
        self.rewards = data["rewards"]
        self.prerequisites = data["prerequisites"]
        self.state = QuestState.NOT_STARTED
        self.parent_quests = data.get("parent_quests", [])
        self.child_quests = data.get("child_quests", [])

    def check_prerequisites(self, player_stats, story_flags):
        for prereq in self.prerequisites:
            if prereq["type"] == "flag":
                if not story_flags.get(prereq["flag"], False):
                    return False
            elif prereq["type"] == "stat":
                if player_stats.get(prereq["stat"], 0) < prereq["value"]:
                    return False
            else:
                # Unknown prerequisite type
                return False
        return True

    def update_objective(self, obj_type, target, amount=1):
        if self.state == QuestState.NOT_STARTED:
            self.state = QuestState.ACTIVE
        for obj in self.objectives:
            if obj.type == obj_type and obj.target == target:
                obj.progress += amount
                if obj.progress >= obj.count:
                    obj.completed = True
        if all(obj.completed for obj in self.objectives):
            self.complete()

    def complete(self):
        self.state = QuestState.COMPLETED
        # Rewards will be distributed by QuestManager


class QuestManager:
    def __init__(self):
        self.quests = {}
        self.player = None  # To be set later
        self.load_quests()

    def set_player(self, player):
        self.player = player

    def load_quests(self):
        with open("data/quests/quests.json", "r") as f:
            data = json.load(f)
            for qid, qdata in data.items():
                self.quests[qid] = Quest(qdata)

    def start_quest(self, qid, player_stats, story_flags):
        quest = self.quests[qid]
        if quest.check_prerequisites(player_stats, story_flags):
            quest.state = QuestState.ACTIVE
            # Notify UI - could add event here

    def update_quest(self, event_type, target, amount=1):
        for quest in self.quests.values():
            if quest.state == QuestState.ACTIVE:
                quest.update_objective(event_type, target, amount)
                if quest.state == QuestState.COMPLETED:
                    self.distribute_rewards(quest)

    def distribute_rewards(self, quest):
        if self.player:
            for reward, value in quest.rewards.items():
                if reward == "exp":
                    self.player.exp += value
                # Add more rewards as needed
        print(f"Rewards distributed for {quest.title}")

    def get_active_quests(self):
        return [q for q in self.quests.values() if q.state == QuestState.ACTIVE]
