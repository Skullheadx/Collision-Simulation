import pygame
from math import copysign
from colours import *
from box import Box
from collision import handleBoxCollision


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

    def update(self, delta):
        self.velocity.x = min(self.speed_limit, abs(self.velocity.x + self.acceleration.x * delta))\
                          * copysign(1, self.velocity.x + self.acceleration.x * delta)
        self.velocity.y = min(self.speed_limit, abs(self.velocity.y + self.acceleration.y * delta))\
                          * copysign(1, self.velocity.y + self.acceleration.y * delta)

        self.position.x += self.velocity.x * delta
        self.position.y += self.velocity.y * delta

        self.left = self.position.x - self.radius
        self.right = self.position.x + self.radius
        self.top = self.position.y - self.radius
        self.bottom = self.position.y + self.radius

        for thing in self.collision_layer:
            if isinstance(thing, Box):
                handleBoxCollision(self, thing)

    def draw(self, surf):
        pygame.draw.circle(surf, RED, self.position, self.radius)
