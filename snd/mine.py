"""格子
"""

import pygame
import snd.color as color


class Mine():
    """格子
    """

    def __init__(self, x: int, y: int, game_surface: pygame.Surface, size=25):
        if x == -1 and y == -1:
            self.x = -1
            self.y = -1
            self.mouse = True
            return
        self.x = x
        self.y = y
        self.size = size
        self.pos = (x, y)
        self.Rect_x = x*size
        self.Rect_y = y*size
        self.Rect = (x*size, y*size, size, size)
        self.mouse = False
        self.game_surface = game_surface

    def get_rect(self, topleft):
        self.rect = self.surface.get_rect(
            topleft=(topleft[0]+self.Rect_x, topleft[1]+self.Rect_y))

    def mouse_click(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print(self.pos)
        ...
    def reflash(self):
        x = self.x
        y = self.y
        size = self.size
        self.surface = pygame.Surface((size, size), flags=pygame.SRCALPHA)
        pygame.draw.polygon(self.surface, (255, 255, 255, 128), [
                            (0, 0), (size, 0), (0, size)])
        pygame.draw.polygon(self.surface, (0, 0, 0, 64), [
                            (size, size), (size, 0), (0, size)])
        self.game_surface.blit(self.surface, (self.Rect_x,self.Rect_y))
        pygame.draw.rect(self.game_surface, color.Silver,
                         (x*size+3, y*size+3, size-6, size-6))
        if self.mouse:
            a = pygame.Surface((size, size), flags=pygame.SRCALPHA)
            pygame.draw.rect(a, (255,255,255,128), (0, 0, size, size))
            self.game_surface.blit(a, (self.Rect_x,self.Rect_y))
