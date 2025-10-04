import pygame


class Collectible(pygame.sprite.Sprite):
    def __init__(self, pos, groups, item_type, effect):
        super().__init__(groups)
        self.item_type = item_type
        self.effect = effect
        # Load image based on type
        self.image = pygame.image.load(
            f"../graphics/items/{item_type}.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def collect(self, player, quest_manager=None, story_manager=None):
        if self.effect == "health":
            player.health = min(player.stats["health"], player.health + 20)
        elif self.effect == "exp":
            player.exp += 10
        # etc.
        self.kill()


class Artifact(Collectible):
    def __init__(self, pos, groups, artifact_name):
        super().__init__(pos, groups, "artifact", "story")
        self.artifact_name = artifact_name

    def collect(self, player, quest_manager=None, story_manager=None):
        # Trigger story event
        if story_manager:
            story_manager.set_flag(f"{self.artifact_name}_collected", True)
            story_manager.set_flag("artifact_collected", True)  # Generic flag
        print(f"Collected {self.artifact_name}")
        self.kill()
