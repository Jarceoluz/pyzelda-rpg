import unittest
from unittest.mock import MagicMock, patch, call
import sys
import os
import pygame

# Add code directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'code'))

from entity import Entity

class TestEntity(unittest.TestCase):
    """Test Entity class."""

    @patch('pygame.sprite.Sprite.__init__')
    def test_init(self, mock_sprite_init):
        """Test Entity __init__."""
        groups = [MagicMock()]
        pos = (100, 100)

        entity = Entity(groups, pos)

        mock_sprite_init.assert_called_once_with(groups)
        self.assertEqual(entity.frame_index, 0)
        self.assertEqual(entity.animation_speed, 4)
        self.assertEqual(entity.direction, pygame.math.Vector2())

    def test_move(self):
        """Test move method."""
        entity = Entity.__new__(Entity)
        entity.pos = pygame.math.Vector2(100, 100)
        entity.direction = pygame.math.Vector2(1, 1)
        entity.hitbox = MagicMock()
        entity.hitbox.centerx = MagicMock()
        entity.hitbox.centery = MagicMock()
        entity.rect = MagicMock()
        entity.rect.centerx = MagicMock()
        entity.rect.centery = MagicMock()
        entity.obstacle_sprites = MagicMock()
        entity.collision = MagicMock()

        speed = 50
        pos = pygame.math.Vector2(100, 100)
        dt = 0.016

        entity.move(speed, pos, dt)

        self.assertEqual(entity.pos, pos)
        # direction normalized
        self.assertAlmostEqual(entity.direction.magnitude(), 1.0)
        # hitbox and rect updated
        from unittest.mock import call
        entity.collision.assert_has_calls([call('horizontal'), call('vertical')])

    def test_collision_horizontal(self):
        """Test collision horizontal."""
        entity = Entity.__new__(Entity)
        entity.hitbox = MagicMock()
        entity.hitbox.colliderect.return_value = True
        entity.rect = MagicMock()
        entity.pos = pygame.math.Vector2(100, 100)
        entity.direction = pygame.math.Vector2(1, 0)  # moving right

        obstacle = MagicMock()
        obstacle.hitbox = MagicMock()
        obstacle.hitbox.left = 120
        entity.obstacle_sprites = MagicMock()
        entity.obstacle_sprites.sprites.return_value = [obstacle]

        entity.collision('horizontal')

    def test_collision_vertical(self):
        """Test collision vertical."""
        entity = Entity.__new__(Entity)
        entity.hitbox = MagicMock()
        entity.hitbox.colliderect.return_value = True
        entity.rect = MagicMock()
        entity.pos = pygame.math.Vector2(100, 100)
        entity.direction = pygame.math.Vector2(0, 1)  # moving down

        obstacle = MagicMock()
        obstacle.hitbox = MagicMock()
        obstacle.hitbox.top = 80
        entity.obstacle_sprites = MagicMock()
        entity.obstacle_sprites.sprites.return_value = [obstacle]

        entity.collision('vertical')

    def test_collision_horizontal_left(self):
        """Test collision horizontal moving left."""
        entity = Entity.__new__(Entity)
        entity.hitbox = MagicMock()
        entity.hitbox.colliderect.return_value = True
        entity.rect = MagicMock()
        entity.pos = pygame.math.Vector2(100, 100)
        entity.direction = pygame.math.Vector2(-1, 0)  # moving left

        obstacle = MagicMock()
        obstacle.hitbox = MagicMock()
        obstacle.hitbox.right = 80
        entity.obstacle_sprites = MagicMock()
        entity.obstacle_sprites.sprites.return_value = [obstacle]

        entity.collision('horizontal')

    def test_collision_vertical_up(self):
        """Test collision vertical moving up."""
        entity = Entity.__new__(Entity)
        entity.hitbox = MagicMock()
        entity.hitbox.colliderect.return_value = True
        entity.rect = MagicMock()
        entity.pos = pygame.math.Vector2(100, 100)
        entity.direction = pygame.math.Vector2(0, -1)  # moving up

        obstacle = MagicMock()
        obstacle.hitbox = MagicMock()
        obstacle.hitbox.bottom = 120
        entity.obstacle_sprites = MagicMock()
        entity.obstacle_sprites.sprites.return_value = [obstacle]

        entity.collision('vertical')

    @patch('pygame.time.get_ticks')
    @patch('entity.sin')
    def test_wave_value(self, mock_sin, mock_get_ticks):
        """Test wave_value."""
        mock_get_ticks.return_value = 0
        mock_sin.return_value = 0.5

        entity = Entity.__new__(Entity)
        result = entity.wave_value()

        self.assertEqual(result, 255)

        mock_sin.return_value = -0.5
        result = entity.wave_value()

        self.assertEqual(result, 0)

    def test_animate(self):
        """Test animate method."""
        entity = Entity.__new__(Entity)
        entity.frame_index = 0
        entity.animation_speed = 4
        entity.status = 'idle'
        entity.animations = {'idle': [MagicMock(), MagicMock()]}
        entity.image = MagicMock()
        entity.rect = MagicMock()

        dt = 0.25  # 1/4 = 0.25, so frame_index +=1

        entity.animate(dt)

        self.assertEqual(entity.frame_index, 1)
        self.assertEqual(entity.image, entity.animations['idle'][1])

    def test_animate_wrap(self):
        """Test animate with frame wrap."""
        entity = Entity.__new__(Entity)
        entity.frame_index = 1.9
        entity.animation_speed = 4
        entity.status = 'idle'
        entity.animations = {'idle': [MagicMock(), MagicMock()]}
        entity.image = MagicMock()
        entity.rect = MagicMock()

        dt = 0.1  # frame_index +=0.4, 1.9+0.4=2.3 %2 =0.3

        entity.animate(dt)

        self.assertAlmostEqual(entity.frame_index, 0.3)

    def test_move_zero_direction(self):
        """Test move with zero direction."""
        entity = Entity.__new__(Entity)
        entity.pos = pygame.math.Vector2(100, 100)
        entity.direction = pygame.math.Vector2(0, 0)
        entity.hitbox = MagicMock()
        entity.hitbox.centerx = MagicMock()
        entity.hitbox.centery = MagicMock()
        entity.rect = MagicMock()
        entity.rect.centerx = MagicMock()
        entity.rect.centery = MagicMock()
        entity.obstacle_sprites = MagicMock()
        entity.collision = MagicMock()

        speed = 50
        pos = pygame.math.Vector2(100, 100)
        dt = 0.016

        entity.move(speed, pos, dt)

        self.assertEqual(entity.pos, pos)
        # direction not normalized since magnitude 0
        self.assertEqual(entity.direction, pygame.math.Vector2(0, 0))
        entity.collision.assert_has_calls([call('horizontal'), call('vertical')])

    def test_collision_no_sprites(self):
        """Test collision with no obstacle sprites."""
        entity = Entity.__new__(Entity)
        entity.hitbox = MagicMock()
        entity.obstacle_sprites = MagicMock()
        entity.obstacle_sprites.sprites.return_value = []

        entity.collision('horizontal')
        # No assertions, just ensure no error

    def test_collision_no_hitbox(self):
        """Test collision with sprite without hitbox."""
        entity = Entity.__new__(Entity)
        entity.hitbox = MagicMock()
        entity.obstacle_sprites = MagicMock()
        obstacle = MagicMock()
        del obstacle.hitbox  # no hitbox
        entity.obstacle_sprites.sprites.return_value = [obstacle]

        entity.collision('horizontal')
        # No assertions

    def test_animate_no_animations(self):
        """Test animate without animations."""
        entity = Entity.__new__(Entity)
        entity.frame_index = 0
        entity.animation_speed = 4

        dt = 0.25

        entity.animate(dt)

        self.assertEqual(entity.frame_index, 1)  # still incremented

    def test_animate_no_status(self):
        """Test animate without status."""
        entity = Entity.__new__(Entity)
        entity.frame_index = 0
        entity.animation_speed = 4
        entity.animations = {'idle': [MagicMock()]}

        dt = 0.25

        entity.animate(dt)

        self.assertEqual(entity.frame_index, 1)

    def test_animate_no_image(self):
        """Test animate without image."""
        entity = Entity.__new__(Entity)
        entity.frame_index = 0
        entity.animation_speed = 4
        entity.status = 'idle'
        entity.animations = {'idle': [MagicMock(), MagicMock()]}

        dt = 0.25

        entity.animate(dt)

        self.assertEqual(entity.frame_index, 1)

    def test_animate_no_rect(self):
        """Test animate without rect."""
        entity = Entity.__new__(Entity)
        entity.frame_index = 0
        entity.animation_speed = 4
        entity.status = 'idle'
        entity.animations = {'idle': [MagicMock(), MagicMock()]}
        entity.image = MagicMock()

        dt = 0.25

        entity.animate(dt)

        self.assertEqual(entity.frame_index, 1)

if __name__ == '__main__':
    unittest.main()