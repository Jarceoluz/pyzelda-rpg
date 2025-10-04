import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Add code directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'code'))

class TestFactories(unittest.TestCase):
    """Test factory classes."""

    @patch('factories.Player')
    def test_player_factory_create_player(self, mock_player):
        """Test PlayerFactory.create_player."""
        from factories import PlayerFactory

        mock_player_instance = MagicMock()
        mock_player.return_value = mock_player_instance

        pos = (100, 100)
        groups = [MagicMock()]
        obstacle_sprites = MagicMock()
        create_attack = MagicMock()
        destroy_attack = MagicMock()
        create_magic = MagicMock()
        config = {'health': 100}

        result = PlayerFactory.create_player(pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic, config)

        mock_player.assert_called_once_with(pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic)
        mock_player_instance.from_dict.assert_called_once_with(config)
        self.assertEqual(result, mock_player_instance)

    @patch('factories.Player')
    def test_player_factory_create_player_no_health(self, mock_player):
        """Test PlayerFactory.create_player without health in config."""
        from factories import PlayerFactory

        mock_player_instance = MagicMock()
        mock_player.return_value = mock_player_instance

        pos = (100, 100)
        groups = [MagicMock()]
        obstacle_sprites = MagicMock()
        create_attack = MagicMock()
        destroy_attack = MagicMock()
        create_magic = MagicMock()
        config = {}  # no health

        result = PlayerFactory.create_player(pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic, config)

        mock_player.assert_called_once_with(pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic)
        mock_player_instance.from_dict.assert_not_called()
        self.assertEqual(result, mock_player_instance)

    @patch('factories.PlayerFactory.create_player')
    def test_player_factory_load_player(self, mock_create_player):
        """Test PlayerFactory.load_player."""
        from factories import PlayerFactory

        mock_player = MagicMock()
        mock_create_player.return_value = mock_player
        data = {'health': 100}
        groups = [MagicMock()]
        obstacle_sprites = MagicMock()
        create_attack = MagicMock()
        destroy_attack = MagicMock()
        create_magic = MagicMock()

        result = PlayerFactory.load_player(data, groups, obstacle_sprites, create_attack, destroy_attack, create_magic)

        mock_create_player.assert_called_once_with((0, 0), groups, obstacle_sprites, create_attack, destroy_attack, create_magic)
        mock_player.from_dict.assert_called_once_with(data)
        self.assertEqual(result, mock_player)

    def test_enemy_factory(self):
        """Test EnemyFactory functionality."""
        from factories import EnemyFactory

        # Test enemy type mappings
        self.assertIn('squid', EnemyFactory.ENEMY_TYPES)
        self.assertIn('raccoon', EnemyFactory.ENEMY_TYPES)
        self.assertIn('spirit', EnemyFactory.ENEMY_TYPES)

        # Test boss type mappings
        self.assertIn('fire_guardian', EnemyFactory.BOSS_TYPES)
        self.assertIn('ice_queen', EnemyFactory.BOSS_TYPES)
        self.assertIn('shadow_lord', EnemyFactory.BOSS_TYPES)

        # Test create_enemy method exists
        self.assertTrue(hasattr(EnemyFactory, 'create_enemy'))

        # Test create_enemy raises for unknown type
        from unittest.mock import MagicMock
        pos = (100, 100)
        groups = [MagicMock()]
        obstacle_sprites = MagicMock()
        damage_player = MagicMock()
        trigger_death_particles = MagicMock()
        add_exp = MagicMock()
        trigger_exp_particles = MagicMock()
        pathfinding_grid = MagicMock()
        tile_size = 64
        quest_manager = MagicMock()

        with self.assertRaises(ValueError):
            EnemyFactory.create_enemy(
                'unknown', pos, groups, obstacle_sprites,
                damage_player, trigger_death_particles, add_exp, trigger_exp_particles,
                pathfinding_grid, tile_size, quest_manager
            )

    @patch('factories.Enemy')
    def test_enemy_factory_create_enemy(self, mock_enemy):
        """Test EnemyFactory.create_enemy for known types."""
        from factories import EnemyFactory

        mock_enemy_instance = MagicMock()
        mock_enemy.return_value = mock_enemy_instance

        pos = (100, 100)
        groups = [MagicMock()]
        obstacle_sprites = MagicMock()
        damage_player = MagicMock()
        trigger_death_particles = MagicMock()
        add_exp = MagicMock()
        trigger_exp_particles = MagicMock()
        pathfinding_grid = MagicMock()
        tile_size = 64
        quest_manager = MagicMock()

        # Test regular enemy
        result = EnemyFactory.create_enemy('squid', pos, groups, obstacle_sprites, damage_player,
                                          trigger_death_particles, add_exp, trigger_exp_particles,
                                          pathfinding_grid, tile_size, quest_manager)
        mock_enemy.assert_called_once_with('squid', pos, groups, obstacle_sprites, damage_player,
                                          trigger_death_particles, add_exp, trigger_exp_particles,
                                          pathfinding_grid, tile_size)
        self.assertEqual(result, mock_enemy_instance)

    def test_enemy_factory_create_boss(self):
        """Test EnemyFactory.create_enemy for boss types."""
        import bosses
        with patch.object(bosses, 'FireGuardianBoss') as mock_boss:
            from factories import EnemyFactory

            mock_boss_instance = MagicMock()
            mock_boss.return_value = mock_boss_instance

            pos = (100, 100)
            groups = [MagicMock()]
            obstacle_sprites = MagicMock()
            damage_player = MagicMock()
            trigger_death_particles = MagicMock()
            add_exp = MagicMock()
            trigger_exp_particles = MagicMock()
            pathfinding_grid = MagicMock()
            tile_size = 64
            quest_manager = MagicMock()

            # Test boss
            result = EnemyFactory.create_enemy('fire_guardian', pos, groups, obstacle_sprites, damage_player,
                                              trigger_death_particles, add_exp, trigger_exp_particles,
                                              pathfinding_grid, tile_size, quest_manager)
            mock_boss.assert_called_once_with('fire_guardian', pos, groups, obstacle_sprites, damage_player,
                                              trigger_death_particles, add_exp, trigger_exp_particles,
                                              pathfinding_grid, tile_size, quest_manager)
            self.assertEqual(result, mock_boss_instance)

    @patch('factories.Collectible')
    @patch('factories.Artifact')
    def test_item_factory_create_collectible(self, mock_artifact, mock_collectible):
        """Test ItemFactory.create_collectible."""
        from factories import ItemFactory

        mock_collectible_instance = MagicMock()
        mock_collectible.return_value = mock_collectible_instance
        mock_artifact_instance = MagicMock()
        mock_artifact.return_value = mock_artifact_instance

        pos = (100, 100)
        groups = [MagicMock()]
        effect = MagicMock()
        quest_manager = MagicMock()
        story_manager = MagicMock()

        # Test collectible
        result = ItemFactory.create_collectible('coin', pos, groups, effect, quest_manager, story_manager)
        mock_collectible.assert_called_once_with(pos, groups, 'coin', effect, quest_manager, story_manager)
        self.assertEqual(result, mock_collectible_instance)

        # Test artifact
        result = ItemFactory.create_collectible('artifact', pos, groups, effect, quest_manager, story_manager)
        mock_artifact.assert_called_once_with(pos, groups, 'artifact', quest_manager, story_manager)
        self.assertEqual(result, mock_artifact_instance)

    @patch('factories.EnemyFactory.create_enemy')
    def test_map_factory_create_entity_from_code(self, mock_create_enemy):
        """Test MapFactory.create_entity_from_code."""
        from factories import MapFactory

        mock_enemy = MagicMock()
        mock_create_enemy.return_value = mock_enemy

        pos = (100, 100)
        groups = [MagicMock()]
        obstacle_sprites = MagicMock()
        damage_player = MagicMock()
        trigger_death_particles = MagicMock()
        add_exp = MagicMock()
        trigger_exp_particles = MagicMock()
        pathfinding_grid = MagicMock()
        tile_size = 64
        quest_manager = MagicMock()

        # Test enemy code
        result = MapFactory.create_entity_from_code('390', pos, groups, obstacle_sprites, damage_player,
                                                   trigger_death_particles, add_exp, trigger_exp_particles,
                                                   pathfinding_grid, tile_size, quest_manager)
        mock_create_enemy.assert_called_once_with('bamboo', pos, groups, obstacle_sprites, damage_player,
                                                 trigger_death_particles, add_exp, trigger_exp_particles,
                                                 pathfinding_grid, tile_size, quest_manager)
        self.assertEqual(result, mock_enemy)

        # Test player code
        result = MapFactory.create_entity_from_code('394', pos, groups, obstacle_sprites, damage_player,
                                                   trigger_death_particles, add_exp, trigger_exp_particles,
                                                   pathfinding_grid, tile_size, quest_manager)
        self.assertIsNone(result)
        mock_create_enemy.assert_called_once()  # Still once

        # Test unknown code
        result = MapFactory.create_entity_from_code('999', pos, groups, obstacle_sprites, damage_player,
                                                   trigger_death_particles, add_exp, trigger_exp_particles,
                                                   pathfinding_grid, tile_size, quest_manager)
        self.assertIsNone(result)

    def test_map_factory(self):
        """Test MapFactory functionality."""
        from factories import MapFactory

        # Test enemy type mapping from codes
        self.assertEqual(MapFactory.get_enemy_type_from_code('390'), 'bamboo')
        self.assertEqual(MapFactory.get_enemy_type_from_code('391'), 'spirit')
        self.assertEqual(MapFactory.get_enemy_type_from_code('392'), 'raccoon')
        self.assertEqual(MapFactory.get_enemy_type_from_code('393'), 'squid')
        self.assertEqual(MapFactory.get_enemy_type_from_code('999'), 'squid')  # default

        # Test that the class has the create_entity_from_code method
        self.assertTrue(hasattr(MapFactory, 'create_entity_from_code'))

if __name__ == '__main__':
    unittest.main()