import pygame
import random
import math


class Particle:
    """Individual particle for visual effects"""

    def __init__(self, x, y, velocity, color, lifetime, size=2, fade=True):
        self.x = x
        self.y = y
        self.velocity = velocity  # (vx, vy)
        self.color = color
        self.original_lifetime = lifetime
        self.lifetime = lifetime
        self.size = size
        self.fade = fade

    @property
    def is_dead(self):
        """Check if particle has expired"""
        return self.lifetime <= 0

    def update(self, dt):
        """Update particle position and lifetime"""
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.lifetime -= dt

        # Shrink as lifetime decreases
        if self.fade:
            self.size = max(0.1, self.size * (self.lifetime / self.original_lifetime))

    def draw(self, surface):
        """Draw particle on surface"""
        # Fade out as lifetime decreases
        alpha = (
            int(255 * (self.lifetime / self.original_lifetime)) if self.fade else 255
        )

        if isinstance(self.color, tuple) and len(self.color) == 3:
            color_with_alpha = (*self.color, alpha)
        else:
            # If color already has alpha, adjust it
            color_with_alpha = (*self.color[:3], min(self.color[3], alpha))

        # Draw as a circle with anti-aliasing if size permits
        if self.size >= 1:
            pygame.draw.circle(
                surface, color_with_alpha, (int(self.x), int(self.y)), int(self.size)
            )
        else:
            # For very small particles, just draw a pixel
            surface.set_at((int(self.x), int(self.y)), color_with_alpha)


class ParticleSystem:
    """System for managing particles for visual effects"""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.particles = []

    def add_particle(self, x, y, velocity, color, lifetime, size=2, fade=True):
        """Add a single particle to the system"""
        self.particles.append(Particle(x, y, velocity, color, lifetime, size, fade))

    def add_explosion(
        self, x, y, count=20, color=(255, 255, 255), size_range=(1, 3), speed=2.0
    ):
        """Add an explosion effect at the given position"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed_val = random.uniform(0.5, speed)
            velocity = (math.cos(angle) * speed_val, math.sin(angle) * speed_val)
            size = random.uniform(size_range[0], size_range[1])
            lifetime = random.uniform(20, 60)

            # Vary color slightly
            r = min(255, max(0, color[0] + random.randint(-20, 20)))
            g = min(255, max(0, color[1] + random.randint(-20, 20)))
            b = min(255, max(0, color[2] + random.randint(-20, 20)))

            self.add_particle(x, y, velocity, (r, g, b, 255), lifetime, size)

    def update(self, dt):
        """Update all particles in the system"""
        # Update all particles first
        for particle in self.particles:
            particle.update(dt * 0.05)  # Scale down dt to make animations smoother

        # Filter out expired particles using is_dead property
        self.particles = [p for p in self.particles if not p.is_dead]

    def draw(self, surface):
        """Draw all particles on the given surface"""
        for particle in self.particles:
            particle.draw(surface)


class AnimationManager:
    """Manager for game animations"""

    def __init__(self):
        self.animations = {}

    def add_animation(
        self,
        name,
        start_value,
        end_value,
        duration,
        delay=0,
        loop=False,
        ease_func=None,
    ):
        """Add an animation to the manager"""
        self.animations[name] = {
            "start": start_value,
            "end": end_value,
            "duration": duration,
            "elapsed": -delay,  # Negative elapsed time handles delay
            "loop": loop,
            "completed": False,
            "ease_func": ease_func or self._linear_ease,
        }

    def update(self, dt):
        """Update all animations"""
        for name, anim in self.animations.items():
            if anim["completed"] and not anim["loop"]:
                continue

            anim["elapsed"] += dt

            # Handle delay
            if anim["elapsed"] < 0:
                continue

            if anim["elapsed"] >= anim["duration"]:
                if anim["loop"]:
                    anim["elapsed"] = anim["elapsed"] % anim["duration"]
                else:
                    anim["elapsed"] = anim["duration"]
                    anim["completed"] = True

    def get_value(self, name, default_value=None):
        """
        Get the current value of an animation

        Args:
            name: The name of the animation
            default_value: The value to return if the animation doesn't exist

        Returns:
            The current animation value, or the default value if animation not found
        """
        if name not in self.animations:
            return default_value

        anim = self.animations[name]
        if anim["elapsed"] < 0:
            return anim["start"]

        progress = min(1.0, anim["elapsed"] / anim["duration"])
        eased_progress = anim["ease_func"](progress)

        # Linear interpolation between start and end values
        return anim["start"] + (anim["end"] - anim["start"]) * eased_progress

    def _linear_ease(self, t):
        """Linear easing function"""
        return t

    def _ease_in_out(self, t):
        """Smooth ease-in, ease-out function"""
        return -0.5 * (math.cos(math.pi * t) - 1)
