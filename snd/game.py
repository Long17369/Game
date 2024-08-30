"""游戏逻辑
"""

import random
from typing import Tuple
import pygame
import time
import snd.color as color
from snd.mine import Cell, Cell_Type
import snd.constant as constant
Level = constant.Level

_log = False


def log(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if _log:
            with open('log.txt', 'a') as f:
                print(
                    f'{time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())}', file=f)
                print(f'{func.__name__}', file=f)
                for i in range(len(args)):
                    print(f'{i},{args[i]}', file=f)
                for i in kwargs:
                    print(f'{i}:{kwargs[i]}', file=f)
                print(f'result:{result}', file=f)
                print(
                    '--------------------------------------------------------------------------------', file=f)
        return result
    return wrapper


@log
def Log(*args, **kwargs):
    return


class Game():
    """游戏逻辑
    """

    end: bool = False
    run: bool = False

    def __init__(self, level: Level = Level()):
        """初始化游戏
        """
        self.level = level
        self.screen = pygame.display.set_mode(
            (self.level.x * 25 + 40, self.level.y * 25 + 100))
        self.screen.fill(color.Gray_X11)
        self.no_pos = Cell(-1, -1, self.screen)
        self.mouse_motion_pos = self.no_pos
        self.minefield_surface_rect = constant.MINEFIELD_SURFACE_RECT
        self.minefield_surface_border = pygame.Surface(
            (self.level.x * 25+2, self.level.y * 25+2), flags=pygame.SRCALPHA)
        self.minefield_surface = pygame.Surface(
            (self.level.x * 25, self.level.y * 25))
        self.minefield = [[Cell(x, y, self.minefield_surface)for y in range(
            self.level.y)] for x in range(self.level.x)]
        self.reflash()
        [i.get_rect(self.minefield_surface_rect)
         for j in self.minefield for i in j]

    def run_game(self):
        """开始一轮游戏
        """
        self.set_mine()
        self.time = time.time()
        self.Timer: int = 0
        self.run = True
        ...

    def mouse_click(self, event: pygame.event.Event):
        """鼠标点击事件
        """
        if self.minefield_surface.get_rect(topleft=self.minefield_surface_rect).collidepoint(event.pos):
            if (not self.run) and event.button == 1:
                self.run_game()
            self.end = self.click_cell(event, self.mouse_motion_pos)

    def restart(self,):
        """重置地雷位置
        """
        def reset(n: Cell):
            n.type = Cell_Type.Safe_Unexplored
            n.number = 0
        [reset(i)
         for j in self.minefield for i in j if i.type in Cell_Type.Mine_Set]
        print('restart')

    @log
    def click_cell(self, event, pos: Cell):
        if pos.mouse_click(event):
            return True
        if event.button == 1:
            if pos.number == 0:
                x = pos.pos[0]
                y = pos.pos[1]
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        if i < 0 or j < 0:
                            continue
                        try:
                            posTemp = self.minefield[i][j]
                            if posTemp.type in Cell_Type.Unexplored_Set:
                                if self.click_cell(event, posTemp):
                                    Log(f'Game Error{posTemp} {self.mouse_motion_pos.pos}')
                                    raise SystemError(
                                        f'Game Error{posTemp} {self.mouse_motion_pos.pos}')
                        except IndexError:
                            ...
        return False

    def mouse_motion(self, event: pygame.event.Event):
        """鼠标移动事件
        """
        if self.minefield_surface.get_rect(topleft=self.minefield_surface_rect).collidepoint(event.pos):
            for i in self.minefield:
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
            self.Timer += 1
        ...

    def reflash(self):
        """重绘游戏界面
        """
        self.screen.fill(color.Gray_X11)
        Rect = (0, 0, self.minefield_surface_border.get_width(),
                self.minefield_surface_border.get_height())
        rect = (i-1 for i in self.minefield_surface_rect)
        pygame.draw.rect(self.minefield_surface_border,
                         (0, 0, 0, 156), Rect, 1)
        self.minefield_surface.fill(color.Gray_X11)
        [i.reflash() for j in self.minefield for i in j]
        self.screen.blit(self.minefield_surface_border, tuple(rect))
        self.screen.blit(self.minefield_surface, self.minefield_surface_rect)

    def set_mine(self):
        """设置地雷
        """

        mine_count = 0
        while mine_count <= self.level.mine_count-1:
            x = random.randint(0, self.level.x-1)
            y = random.randint(0, self.level.y-1)
            if self.minefield[x][y].type not in Cell_Type.Mine_Set:
                if self.minefield[x][y] == self.mouse_motion_pos:
                    continue
                self.minefield[x][y].type += Cell_Type.Mine
                # print((x, y))
                mine_count += 1
                Log_List = [(x, y)]
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        if i < 0 or j < 0:
                            continue
                        try:
                            self.minefield[i][j].number += 1
                        except IndexError:
                            ...
                        else:
                            Log_List.append((i, j))
                Log(Log_List)
        Log('\n'+'\n'.join([''.join([str(i.number)
            if i.type in Cell_Type.Safe_Set else '*' for i in j])for j in self.minefield]))
