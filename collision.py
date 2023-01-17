from linear_interpolation import LinearInterpolation
import pygame


def handleBoxCollision(particle, box):  # Continuous Collision Detection
    if particle.left <= box.left or particle.right >= box.right:
        particle.velocity.x *= -1
    if particle.bottom >= box.bottom or particle.top <= box.top:
        particle.velocity.y *= -1

    next_frame, _ = particle.get_next_frame(particle.position, particle.velocity, 1)
    x = LinearInterpolation(particle.position.x, next_frame.x)
    y = LinearInterpolation(particle.position.y, next_frame.y)
    t_c = (box.bottom + particle.radius - next_frame.y) / (particle.position.y - next_frame.y)

    point_of_collision = pygame.Vector2((x.evaluate(t_c), y.evaluate(t_c)))

    print((x.evaluate(t_c), y.evaluate(t_c)),particle.position, next_frame, t_c)

    # particle.position -= next_frame - point_of_collision



