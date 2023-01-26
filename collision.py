from itertools import combinations

from pygame import Vector2


def detectTopCollision(particle, box):
    if particle.top <= box.top:
        return True
    return False


def detectBottomCollision(particle, box):
    if particle.bottom >= box.bottom:
        return True
    return False


def detectLeftCollision(particle, box):
    if particle.left <= box.left:
        return True
    return False


def detectRightCollision(particle, box):
    if particle.right >= box.right:
        return True
    return False


def handleTopCollision(particle, box):
    particle.velocity.y *= -1
    # particle.position.y = box.top + particle.radius
    return True


def handleBottomCollision(particle, box):
    particle.velocity.y *= -1
    # particle.position.y = box.bottom - particle.radius
    return True


def handleLeftCollision(particle, box):
    particle.velocity.x *= -1
    # particle.position.x = box.left + particle.radius
    return True


def handleRightCollision(particle, box):
    particle.velocity.x *= -1
    # particle.position.x = box.right - particle.radius
    return True


def handleBoxCollision(particle, box):
    if detectTopCollision(particle, box) or detectBottomCollision(particle, box):
        particle.velocity.y *= -1
        return True
    elif detectLeftCollision(particle, box) or detectRightCollision(particle, box):
        particle.velocity.x *= -1
        return True
    return False


def detectParticleCollision(particle1, particle2):
    if particle1.position.distance_to(particle2.position) <= particle1.radius + particle2.radius and \
            particle1 != particle2:
        return True
    return False


def handleParticleCollision(particle1, particle2):  # https://www.vobarian.com/collisions/2dcollisions2.pdf
    if detectParticleCollision(particle1, particle2):
        n = particle2.position - particle1.position
        un = n / n.magnitude()
        ut = Vector2(-un.y, un.x)

        v1 = particle1.velocity
        v2 = particle2.velocity

        v1n = un.dot(v1)
        v1t = ut.dot(v1)
        v2n = un.dot(v2)
        v2t = ut.dot(v2)

        v1t_prime = v1t
        v2t_prime = v2t

        v1n_prime = (v1n * (particle1.mass - particle2.mass) + 2 * particle2.mass * v2n) / (
                particle1.mass + particle2.mass)
        v2n_prime = (v2n * (particle2.mass - particle1.mass) + 2 * particle1.mass * v1n) / (
                particle1.mass + particle2.mass)

        v1_prime = v1n_prime * un + v1t_prime * ut
        v2_prime = v2n_prime * un + v2t_prime * ut

        particle1.velocity = v1_prime
        particle2.velocity = v2_prime
        return True
    return False


def sweepAndPrune(particle_list):  # broad phase collision detection
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


def spacePartitioning(particle_list, width, height):  # broad phase collision detection

    n = 25

    grid = [[[] for _ in range(n)] for _ in range(n)]

    for particle in particle_list:
        x1 = int(particle.left // (width / n))
        x2 = int(particle.right // (width / n))
        y1 = int(particle.top // (height / n))
        y2 = int(particle.bottom // (height / n))
        if x1 < 0:
            x1 = 0
        if x2 < 0:
            x2 = 0
        if y1 < 0:
            y1 = 0
        if y2 < 0:
            y2 = 0
        if x1 >= n:
            x1 = n - 1
        if x2 >= n:
            x2 = n - 1
        if y1 >= n:
            y1 = n - 1
        if y2 >= n:
            y2 = n - 1

        grid[y1][x1].append(particle)
        grid[y1][x2].append(particle)
        grid[y2][x1].append(particle)
        grid[y2][x2].append(particle)

    checks = []
    for i in range(n):
        for j in range(n):
            checks.extend(tuple(combinations(grid[i][j], 2)))

    return list(set(checks))
