from math import copysign

import pygame

from box import Box
from collision import handleBoxCollision, handleParticleCollision, detectTopCollision, handleTopCollision, \
    detectBottomCollision, handleBottomCollision, detectLeftCollision, handleLeftCollision, handleRightCollision, \
    detectRightCollision
from colours import *



class Particle:
    speed_limit = 3

    def __init__(self, initial_position, initial_velocity, initial_acceleration, radius, mass, collision_layer):
        self.position = pygame.Vector2(initial_position)
        self.velocity = pygame.Vector2(initial_velocity)
        self.acceleration = pygame.Vector2(initial_acceleration)
        self.radius = radius
        self.mass = mass

        self.left = self.position.x - self.radius
        self.right = self.position.x + self.radius
        self.top = self.position.y - self.radius
        self.bottom = self.position.y + self.radius

        self.collision_layer = collision_layer

        self.colour = RED

        self.collided_with_wall = {"top":False, "bottom": False, "left": False, "right": False}


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

        if not self.collided_with_wall["top"] and detectTopCollision(self, self.collision_layer[0]):
            handleTopCollision(self, self.collision_layer[0])
            self.collided_with_wall["top"] = True
        if not detectTopCollision(self, self.collision_layer[0]):
            self.collided_with_wall["top"] = False

        if not self.collided_with_wall["bottom"] and detectBottomCollision(self, self.collision_layer[0]):
            handleBottomCollision(self, self.collision_layer[0])
            self.collided_with_wall["bottom"] = True
        if not detectBottomCollision(self, self.collision_layer[0]):
            self.collided_with_wall["bottom"] = False

        if not self.collided_with_wall["left"] and detectLeftCollision(self, self.collision_layer[0]):
            handleLeftCollision(self, self.collision_layer[0])
            self.collided_with_wall["left"] = True
        if not detectLeftCollision(self, self.collision_layer[0]):
            self.collided_with_wall["left"] = False

        if not self.collided_with_wall["right"] and detectRightCollision(self, self.collision_layer[0]):
            handleRightCollision(self, self.collision_layer[0])
            self.collided_with_wall["right"] = True
        if not detectRightCollision(self, self.collision_layer[0]):
            self.collided_with_wall["right"] = False


    def draw(self, surf):
        pygame.draw.circle(surf, self.colour, self.position, self.radius)
