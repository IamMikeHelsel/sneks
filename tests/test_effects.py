import unittest
import pygame
from ui.effects import Particle, ParticleSystem, AnimationManager


class TestParticle(unittest.TestCase):
    def test_particle_initialization(self):
        particle = Particle(100, 200, (1, 1), (255, 0, 0), 2.0, 3, True)
        self.assertEqual(particle.x, 100)
        self.assertEqual(particle.y, 200)
        self.assertEqual(particle.velocity, (1, 1))
        self.assertEqual(particle.color, (255, 0, 0))
        self.assertEqual(particle.lifetime, 2.0)
        self.assertEqual(particle.size, 3)
        self.assertTrue(particle.fade)
        self.assertFalse(particle.is_dead)

    def test_particle_update(self):
        particle = Particle(100, 200, (1, 2), (255, 0, 0), 2.0)
        particle.update(0.5)
        self.assertEqual(particle.x, 100.5)
        self.assertEqual(particle.y, 201.0)
        self.assertEqual(particle.lifetime, 1.5)
        self.assertFalse(particle.is_dead)

        particle.update(2.0)
        self.assertTrue(particle.is_dead)


class TestParticleSystem(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_particle_system_initialization(self):
        ps = ParticleSystem(800, 600)
        self.assertEqual(len(ps.particles), 0)
        self.assertEqual(ps.screen_width, 800)
        self.assertEqual(ps.screen_height, 600)

    def test_add_particle(self):
        ps = ParticleSystem(800, 600)
        ps.add_particle(100, 200, (1, 1), (255, 0, 0), 2.0)
        self.assertEqual(len(ps.particles), 1)

    def test_add_explosion(self):
        ps = ParticleSystem(800, 600)
        ps.add_explosion(400, 300, count=10)
        self.assertEqual(len(ps.particles), 10)

    def test_update_removes_dead_particles(self):
        ps = ParticleSystem(800, 600)
        ps.add_particle(100, 200, (1, 1), (255, 0, 0), 0.1)
        self.assertEqual(len(ps.particles), 1)
        ps.update(0.2)
        self.assertEqual(len(ps.particles), 0)


class TestAnimationManager(unittest.TestCase):
    def test_animation_manager_initialization(self):
        am = AnimationManager()
        self.assertEqual(len(am.animations), 0)

    def test_add_animation(self):
        am = AnimationManager()
        am.add_animation("test", 0, 100, 1.0)
        self.assertIn("test", am.animations)

    def test_get_value(self):
        am = AnimationManager()
        am.add_animation("test", 0, 100, 1.0)
        # Initially should be at start value
        self.assertEqual(am.get_value("test"), 0)

        # After updating partially through
        am.update(0.5)
        self.assertAlmostEqual(am.get_value("test"), 50, delta=1)

        # After completion
        am.update(0.5)
        self.assertEqual(am.get_value("test"), 100)

        # Default value if animation doesn't exist
        self.assertEqual(am.get_value("nonexistent", 42), 42)

    def test_ease_functions(self):
        am = AnimationManager()
        self.assertEqual(am._linear_ease(0.5), 0.5)
        self.assertLess(am._ease_in_out(0.25), 0.25)  # Early values are slower
        self.assertGreater(am._ease_in_out(0.75), 0.75)  # Later values are faster
