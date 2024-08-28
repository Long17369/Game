"""游戏逻辑
"""

import pygame
import time
import snd.color as color
from snd.mine import Mine


class Game():
    """游戏逻辑
    """

    def __init__(self, game_size_x=0, game_size_y=0, mine=0):
        """初始化游戏
        """
        if game_size_x == 0 or game_size_y == 0:
            self.game_size_x = 10
            self.game_size_y = 10
        else:
            self.game_size_x = game_size_x
            self.game_size_y = game_size_y
        if mine == 0:
            self.mine = 10
        elif mine >= self.game_size_x*self.game_size_y/2:
            self.mine = self.game_size_x*self.game_size_y/2-1
        else:
            self.mine = mine
        self.end = False
        self.screen = pygame.display.set_mode(
            (self.game_size_x * 25 + 40, self.game_size_y * 25 + 100))
        self.screen.fill(color.Gray_X11)
        self.run = False
        self.no_pos = Mine(-1,-1, self.screen)
        self.mouse_motion_pos = self.no_pos
        self.game_surface_rect = (20, 80)
        self.game_surface = pygame.Surface(
            (self.game_size_x * 25, self.game_size_y * 25))
        self.button = [[Mine(x, y, self.game_surface)for y in range(
            self.game_size_y)] for x in range(self.game_size_x)]
        self.reflash()
        [i.get_rect(self.game_surface_rect) for j in self.button for i in j]

    def run_game(self):
        """开始一轮游戏
        """
        self.time = time.time()
        self.start_time = 0
        self.run = True
        ...

    def mouse_click(self, event):
        """鼠标点击事件
        """
        if self.game_surface.get_rect(topleft=self.game_surface_rect).collidepoint(event.pos):
            for i in self.button:
                for j in i:
                    if j.rect.collidepoint(event.pos):
                        j.mouse_click(event)

    def mouse_motion(self, event: pygame.event.Event):
        """鼠标移动事件
        """
        if self.game_surface.get_rect(topleft=self.game_surface_rect).collidepoint(event.pos):
            for i in self.button:
                for j in i:
                    if j.rect.collidepoint(event.pos):
                        self.mouse_motion_pos.mouse = False
                        j.mouse = True
                        self.mouse_motion_pos = j
        else:
            self.mouse_motion_pos.mouse = False
            self.mouse_motion_pos = self.no_pos
            self.mouse_motion_pos.mouse = True

    def update(self):
        """更新游戏时间
        """
        if time.time() - self.time >= 1:
            self.time += 1
            self.start_time += 1
        ...

    def reflash(self):
        """重绘游戏界面
        """

        self.game_surface.fill(color.Gray_X11)
        [i.reflash() for j in self.button for i in j]
        self.screen.blit(self.game_surface, self.game_surface_rect)