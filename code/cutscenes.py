from settings import WIDTH, HEIGHT


class CutsceneEngine:
    def __init__(self, screen, font, animation_player):
        self.screen = screen
        self.font = font
        self.animation_player = animation_player
        self.active = False
        self.current_cutscene = None
        self.step = 0
        self.timer = 0

    def start_cutscene(self, cutscene_id):
        self.active = True
        self.current_cutscene = cutscenes.get(cutscene_id, [])
        self.step = 0
        self.timer = 0

    def update(self, dt):
        if self.active:
            self.timer += dt
            if self.step < len(self.current_cutscene):
                action = self.current_cutscene[self.step]
                if action["type"] == "text":
                    if self.timer > action.get("duration", 3):
                        self.step += 1
                        self.timer = 0
                elif action["type"] == "animation":
                    # Trigger animation
                    self.animation_player.create_particles(
                        action["pos"], [self.screen], "aura"
                    )
                    if self.timer > action.get("duration", 2):
                        self.step += 1
                        self.timer = 0
                elif action["type"] == "end":
                    self.active = False

    def draw(self):
        if self.active and self.step < len(self.current_cutscene):
            action = self.current_cutscene[self.step]
            if action["type"] == "text":
                text_surf = self.font.render(action["text"], True, (255, 255, 255))
                self.screen.blit(
                    text_surf, (WIDTH // 2 - text_surf.get_width() // 2, HEIGHT // 2)
                )


# Cutscene data
cutscenes = {
    "village_attack": [
        {"type": "text", "text": "The village is under attack!", "duration": 2},
        {"type": "animation", "pos": (400, 300), "duration": 2},
        {"type": "text", "text": "You must flee or fight.", "duration": 2},
        {"type": "end"},
    ],
    "artifact_collected": [
        {
            "type": "text",
            "text": "You feel the power of the artifact surge through you.",
            "duration": 3,
        },
        {
            "type": "text",
            "text": "Visions of the past flash before your eyes.",
            "duration": 3,
        },
        {"type": "end"},
    ],
    "ending_good": [
        {
            "type": "text",
            "text": "With all artifacts purified, the Veil mends.",
            "duration": 3,
        },
        {"type": "text", "text": "You become the new Guardian.", "duration": 3},
        {"type": "end"},
    ],
    "ending_neutral": [
        {
            "type": "text",
            "text": "The Shadow Lord is contained, but corruption lingers.",
            "duration": 3,
        },
        {"type": "text", "text": "Eldoria enters an uneasy peace.", "duration": 3},
        {"type": "end"},
    ],
    "ending_bad": [
        {"type": "text", "text": "You embrace the darkness.", "duration": 3},
        {"type": "text", "text": "Eldoria falls to eternal shadow.", "duration": 3},
        {"type": "end"},
    ],
}
