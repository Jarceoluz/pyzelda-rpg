import pygame
from ui import DialogueBox


class DialogueSystem:
    def __init__(self, story_manager, screen, font):
        self.story_manager = story_manager
        self.screen = screen
        self.font = font
        self.active = False
        self.current_dialogue = {}
        self.current_choice = 0
        self.dialogue_box = DialogueBox(screen, font)

    def start_dialogue(self, npc_id):
        self.active = True
        self.current_dialogue = dialogues.get(npc_id, {})
        self.current_choice = 0

    def update(self, events):
        if self.active:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.current_choice = max(0, self.current_choice - 1)
                    elif event.key == pygame.K_DOWN:
                        choices = self.current_dialogue.get("choices", [])
                        self.current_choice = min(
                            len(choices) - 1, self.current_choice + 1
                        )
                    elif event.key == pygame.K_RETURN:
                        self.select_choice()

    def select_choice(self):
        choices = self.current_dialogue.get("choices", [])
        if self.current_choice < len(choices):
            choice = choices[self.current_choice]
            flag = choice.get("flag")
            if flag:
                self.story_manager.set_flag(flag, True)
            # Display response, then end
            self.active = False

    def draw(self):
        if self.active:
            greeting = self.current_dialogue.get("greeting", "")
            choices = self.current_dialogue.get("choices", [])
            self.dialogue_box.draw(greeting, choices, self.current_choice)


# Dialogue data
dialogues = {
    "mentor": {
        "greeting": "Ah, young hero. The artifacts call to you.",
        "choices": [
            {
                "text": "Tell me about the artifacts.",
                "response": "They are fragments of the Guardians, hidden across Eldoria.",
                "flag": "artifact_info_given",
            },
            {
                "text": "I need training.",
                "response": "Very well, let us begin.",
                "flag": "training_started",
            },
            {
                "text": "What is the Shadow Lord?",
                "response": "A fallen Guardian, corrupting the world.",
                "flag": "shadow_lord_info",
            },
            {"text": "Goodbye.", "response": "Farewell, hero."},
        ],
    },
    "villager": {
        "greeting": "Trouble is brewing in the land.",
        "choices": [
            {
                "text": "What trouble?",
                "response": "Monsters are attacking villages.",
                "flag": "villager_warned",
            },
            {
                "text": "I will help.",
                "response": "Thank you, brave one.",
                "flag": "villager_helped",
            },
            {
                "text": "Not my problem.",
                "response": "Suit yourself.",
                "flag": "villager_ignored",
            },
        ],
    },
    "merchant": {
        "greeting": "Welcome to my shop, traveler.",
        "choices": [
            {"text": "Show me your wares.", "response": "Here are my goods."},
            {
                "text": "Tell me about the land.",
                "response": "Eldoria is vast, with many dangers.",
                "flag": "land_info",
            },
            {"text": "Goodbye.", "response": "Safe travels."},
        ],
    },
}
