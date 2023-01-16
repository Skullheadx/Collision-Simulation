from colours import *
import pygame


pygame.init()


class Display:
    WIDTH, HEIGHT = 640, 640
    DIMENSIONS = pygame.Vector2(WIDTH, HEIGHT)
    CENTER = pygame.Vector2(WIDTH / 2, HEIGHT / 2)

    FPS = 60

    def __init__(self, window_name="Pygame"):
        self.is_running = False
        pygame.display.set_caption(window_name)

    def show(self):
        screen = pygame.display.set_mode(self.DIMENSIONS)

        clock = pygame.time.Clock()
        delta = 0
        self.is_running = True
        while self.is_running:
            self.update(delta)
            self.draw(screen)
            pygame.display.flip()
            delta = clock.tick(self.FPS)
        pygame.quit()

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def draw(self, surf):
        surf.fill(WHITE)
