import numpy as np
from pygame import Vector2
from math import sqrt
from itertools import combinations


def handleBoxCollision(particle, box):  # Discrete Collision Detection
    if particle.left <= box.left or particle.right >= box.right:
        particle.velocity.x *= -1
    if particle.bottom >= box.bottom or particle.top <= box.top:
        particle.velocity.y *= -1


def handleParticleCollision(particle1, particle2):  # https://www.vobarian.com/collisions/2dcollisions2.pdf
    if particle1.position.distance_to(particle2.position) <= particle1.radius + particle2.radius and \
            particle1 != particle2:

        v1 = np.array(particle1.velocity)
        v2 = np.array(particle2.velocity)
        x1 = np.array(particle1.position)
        x2 = np.array(particle2.position)
        m1 = particle1.mass
        m2 = particle2.mass

        v1 = v1 - (2 * m2 / (m1 + m2)) * np.dot(v1 - v2, x1 - x2) / np.linalg.norm(x1 - x2) ** 2 * (x1 - x2)
        v2 = v2 - (2 * m1 / (m1 + m2)) * np.dot(v2 - v1, x2 - x1) / np.linalg.norm(x2 - x1) ** 2 * (x2 - x1)

        particle1.velocity = Vector2(list(v1))
        particle2.velocity = Vector2(list(v2))

        # v1 - (2 * m2 / (m1 + m2)) * np.dot(v1 - v2, x1 - x2) / np.linalg.norm(x1 - x2) ** 2 * (x1 - x2)
        # particle1.velocity = particle1.velocity - (2 * particle2.mass) / (particle1.mass + particle2.mass) * (particle1.velocity - particle2.velocity).dot(particle1.position - particle2.position) / ((particle1.position - particle2.position).normalize() * (particle1.position - particle2.position).normalize()) * (particle1.position - particle2.position)
        # particle2.velocity = particle2.velocity - (2 * particle1.mass) / (particle1.mass + particle2.mass) * (particle2.velocity - particle1.velocity).dot(particle2.position - particle1.position) / ((particle2.position - particle1.position).normalize() * (particle2.position - particle1.position).normalize()) * (particle2.position - particle1.position)

        # n = particle2.position - particle1.position
        # un = n / n.magnitude()
        # ut = Vector2(-un.y, un.x)
        #
        # v1 = particle1.velocity
        # v2 = particle2.velocity
        #
        # v1n = un.dot(v1)
        # v1t = ut.dot(v1)
        # v2n = un.dot(v2)
        # v2t = ut.dot(v2)
        #
        # v1t_prime = v1t
        # v2t_prime = v2t
        #
        # v1n_prime = (v1n * (particle1.mass - particle2.mass) + 2 * particle2.mass * v2n) / (
        #         particle1.mass + particle2.mass)
        # v2n_prime = (v2n * (particle2.mass - particle1.mass) + 2 * particle1.mass * v1n) / (
        #         particle1.mass + particle2.mass)
        #
        # v1_prime = v1n_prime * un + v1t_prime * ut
        # v2_prime = v2n_prime * un + v2t_prime * ut
        #
        # particle1.velocity = v1_prime
        # particle2.velocity = v2_prime


def sweepAndPrune(particle_list):
    particles = particle_list.copy()

    particles.sort(key=lambda x: x.position.x)
    x_checks = []
    active = [particles[0]]
    for particle in particles:
        if particle == active[0]:
            continue

        start_x = active[-1].position.x - active[-1].radius
        end_x = active[-1].position.x + active[-1].radius
        if (start_x <= particle.position.x - particle.radius <= end_x or
                start_x <= particle.position.x <= end_x or
                start_x <= particle.position.x + particle.radius <= end_x):
            active.append(particle)
        if len(active) > 1:
            x_checks.extend(tuple(combinations(active, 2)))
        active = [particle]

    particles.sort(key=lambda x: x.position.y)
    y_checks = []
    active = [particles[0]]
    for particle in particles:
        if particle == active[0]:
            continue
        start_y = active[-1].position.y - active[-1].radius
        end_y = active[-1].position.y + active[-1].radius
        if (start_y <= particle.position.y - particle.radius <= end_y or
                start_y <= particle.position.y <= end_y or
                start_y <= particle.position.y + particle.radius <= end_y):
            active.append(particle)
        if len(active) > 1:
            y_checks.extend(tuple(combinations(active, 2)))
        active = [particle]

    return remove_duplicates(x_checks, y_checks)


def intersection(arr1, arr2):
    return [value for value in arr1 if value in set(arr2)]


def remove_duplicates(arr1, arr2):
    return list(set(arr1 + arr2))
