from math import copysign

import pygame

from box import Box
from collision import handleBoxCollision
from colours import *


class Particle:
    speed_limit = 3

    def __init__(self, initial_position, initial_velocity, initial_acceleration, radius, collision_layer):
        self.position = pygame.Vector2(initial_position)
        self.velocity = pygame.Vector2(initial_velocity)
        self.acceleration = pygame.Vector2(initial_acceleration)
        self.radius = radius

        self.left = self.position.x - self.radius
        self.right = self.position.x + self.radius
        self.top = self.position.y - self.radius
        self.bottom = self.position.y + self.radius

        self.collision_layer = collision_layer

    def get_next_frame(self, position, velocity, delta):
        vel = pygame.Vector2()
        pos = pygame.Vector2()

        vel.x = min(self.speed_limit, abs(velocity.x + self.acceleration.x * delta)) \
                * copysign(1, velocity.x + self.acceleration.x * delta)
        vel.y = min(self.speed_limit, abs(velocity.y + self.acceleration.y * delta)) \
                * copysign(1, velocity.y + self.acceleration.y * delta)

        pos.x = position.x + velocity.x * delta
        pos.y = position.y + velocity.y * delta

        return pos, vel

    def update(self, delta):
        self.position, self.velocity = self.get_next_frame(self.position, self.velocity, delta)

        self.left = self.position.x - self.radius
        self.right = self.position.x + self.radius
        self.top = self.position.y - self.radius
        self.bottom = self.position.y + self.radius

        for thing in self.collision_layer:
            if isinstance(thing, Box):
                handleBoxCollision(self, thing)

    def draw(self, surf):
        pygame.draw.circle(surf, RED, self.position, self.radius)
