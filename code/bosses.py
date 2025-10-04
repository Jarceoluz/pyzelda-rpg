from random import choice
from enemy import Enemy


class Boss(Enemy):
    def __init__(
        self,
        monster_name,
        pos,
        groups,
        obstacle_sprites,
        damage_player,
        trigger_death_particles,
        add_exp,
        trigger_exp_particles=None,
        pathfinding_grid=None,
        tile_size=None,
        quest_manager=None,
    ):
        super().__init__(
            monster_name,
            pos,
            groups,
            obstacle_sprites,
            damage_player,
            trigger_death_particles,
            add_exp,
            trigger_exp_particles,
            pathfinding_grid,
            tile_size,
            quest_manager,
        )
        self.phase = 1
        self.max_phases = 3

    def check_phase(self):
        health_percent = self.health / self.monster_info["health"]
        if health_percent < 0.6 and self.phase == 1:
            self.phase = 2
            self.enter_phase_2()
        elif health_percent < 0.3 and self.phase == 2:
            self.phase = 3
            self.enter_phase_3()

    def enter_phase_2(self):
        # Increase speed or attacks
        self.speed *= 1.5

    def enter_phase_3(self):
        # Add special ability
        pass

    def update(self, dt):
        self.hit_reaction()
        self.move(self.speed, self.pos, dt)
        self.animate(dt)
        self.cooldown()
        self.check_phase()
        self.check_death()


class FireGuardianBoss(Boss):
    def __init__(
        self,
        monster_name,
        pos,
        groups,
        obstacle_sprites,
        damage_player,
        trigger_death_particles,
        add_exp,
        trigger_exp_particles=None,
        pathfinding_grid=None,
        tile_size=None,
        quest_manager=None,
    ):
        super().__init__(
            monster_name,
            pos,
            groups,
            obstacle_sprites,
            damage_player,
            trigger_death_particles,
            add_exp,
            trigger_exp_particles,
            pathfinding_grid,
            tile_size,
            quest_manager,
        )
        self.element = "fire"
        self.attack_patterns = ["melee", "fireball", "aoe"]

    def enter_phase_2(self):
        super().enter_phase_2()
        self.attack_patterns.append("fire_wave")

    def enter_phase_3(self):
        super().enter_phase_3()
        self.attack_patterns.append("inferno")

    def actions(self, player):
        super().actions(player)
        if self.status == "attack":
            # Choose attack pattern
            pattern = choice(self.attack_patterns)
            if pattern == "fireball":
                # Shoot fireball
                pass
            elif pattern == "aoe":
                # Area of effect fire
                pass
            # etc.


class IceQueenBoss(Boss):
    def __init__(
        self,
        monster_name,
        pos,
        groups,
        obstacle_sprites,
        damage_player,
        trigger_death_particles,
        add_exp,
        trigger_exp_particles=None,
        pathfinding_grid=None,
        tile_size=None,
        quest_manager=None,
    ):
        super().__init__(
            monster_name,
            pos,
            groups,
            obstacle_sprites,
            damage_player,
            trigger_death_particles,
            add_exp,
            trigger_exp_particles,
            pathfinding_grid,
            tile_size,
            quest_manager,
        )
        self.element = "ice"
        self.max_phases = 4

    def enter_phase_2(self):
        self.speed *= 1.2
        # Ice shield

    def enter_phase_3(self):
        # Summon ice minions
        pass

    def enter_phase_4(self):
        # Ultimate ice blast
        pass

    def check_phase(self):
        health_percent = self.health / self.monster_info["health"]
        if health_percent < 0.75 and self.phase == 1:
            self.phase = 2
            self.enter_phase_2()
        elif health_percent < 0.5 and self.phase == 2:
            self.phase = 3
            self.enter_phase_3()
        elif health_percent < 0.25 and self.phase == 3:
            self.phase = 4
            self.enter_phase_4()


class ShadowLordBoss(Boss):
    def __init__(
        self,
        monster_name,
        pos,
        groups,
        obstacle_sprites,
        damage_player,
        trigger_death_particles,
        add_exp,
        trigger_exp_particles=None,
        pathfinding_grid=None,
        tile_size=None,
        quest_manager=None,
    ):
        super().__init__(
            monster_name,
            pos,
            groups,
            obstacle_sprites,
            damage_player,
            trigger_death_particles,
            add_exp,
            trigger_exp_particles,
            pathfinding_grid,
            tile_size,
            quest_manager,
        )
        self.element = "shadow"
        self.invisible_timer = 0

    def enter_phase_2(self):
        self.invisible_timer = 3000  # 3 seconds invisible

    def enter_phase_3(self):
        # Shadow clones
        pass

    def update(self, dt):
        super().update(dt)
        if self.invisible_timer > 0:
            self.invisible_timer -= dt
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)
