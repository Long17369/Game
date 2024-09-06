"""游戏逻辑
"""

import tkinter as tk
from tkinter import messagebox
import random
from typing import Dict, Tuple
import pygame
import time
import snd.color as color
from snd.mine import Cell, Cell_Type
import snd.constant as constant
from snd.others import log, Log, Level


class Game():
    """游戏逻辑"""

    end: bool = False  # 游戏结束标志
    run: bool = False  # 游戏运行标志
    Flag: Dict[Tuple[int, int], bool] = {}  # 存储旗帜标记的字典

    def __init__(self, level: Level = Level(), size: int = 25):
        """
        初始化游戏

        参数:
        - level: 游戏难度等级，默认为默认等级
        """
        self.level = level  # 设置游戏难度等级
        self.size = size  # 设置游戏大小
        self.screen_size = (self.level.x * size + size * 1.6,
                            self.level.y * size + size * 4)  # 根据难度等级设置游戏窗口大小
        self.screen = pygame.display.set_mode(
            self.screen_size)  # 设置游戏窗口大小
        self.screen.fill(color.Gray_X11)  # 用灰色填充游戏窗口
        self.no_pos = Cell(-1, -1, self.screen,size)  # 创建一个无效位置的单元格对象
        self.mouse_motion_pos = self.no_pos  # 初始化鼠标移动位置为无效位置

        self.minefield_surface_rect = (
            constant.MINEFIELD_SURFACE_RECT[0]*size, constant.MINEFIELD_SURFACE_RECT[1]*size)  # 设置雷区表面的矩形区域
        self.minefield_surface_border = pygame.Surface(
            (self.level.x * size + 2, self.level.y * size + 2), flags=pygame.SRCALPHA)  # 创建雷区边框表面
        self.minefield_surface = pygame.Surface(
            (self.level.x * size, self.level.y * size))  # 创建雷区表面
        self.minefield = [[Cell(x, y, self.minefield_surface,size) for y in range(
            self.level.y)] for x in range(self.level.x)]  # 初始化雷区，创建所有单元格对象
        # 重置按钮
        self.reset_button = Cell(-10086,-10086, self.screen,size)
        self.reset_button.type = Cell_Type.Reset_Button
        self.reset_button.Rect_x = self.screen_size[0] / 2 - size / 2
        self.reset_button.Rect_y = self.minefield_surface_rect[1] / 2 - size / 2
        self.reset_button.rect = pygame.Rect(
            self.reset_button.Rect_x, self.reset_button.Rect_y, size, size)
        self.reflash()  # 刷新游戏界面
        [i.get_rect(self.minefield_surface_rect)
         for j in self.minefield for i in j]  # 为每个单元格设置矩形区域

    def run_game(self):
        """开始一轮游戏"""
        self.set_mine()  # 设置地雷
        self.time = time.time()  # 记录游戏开始时间
        self.Timer: int = 0  # 初始化计时器
        self.run = True  # 设置游戏运行状态为True
        ...

    def mouse_click(self, event: pygame.event.Event):
        """鼠标点击事件"""
        # 检查鼠标点击是否在雷区表面内
        if self.minefield_surface.get_rect(topleft=self.minefield_surface_rect).collidepoint(event.pos):
            pos = self.mouse_motion_pos
            # 如果游戏未运行且点击了左键，则开始游戏
            if (not self.run) and event.button == 1:
                self.run_game()
            # 点击单元格并检查是否触雷
            if self.click_cell(event, pos):
                self.end = True
                # 显示游戏结束提示框
                a = tk.Tk()
                a.withdraw()
                messagebox.showinfo('Game Over', 'Game Over')
                a.quit()
            # 右键点击事件，处理旗帜标记
            if event.button == 3:
                if pos.type in Cell_Type.Flag_Set:
                    self.Flag[pos.pos] = True
                elif pos.type in Cell_Type.No_Flag and pos.pos in self.Flag:
                    self.Flag.pop(pos.pos)
            # 检查游戏状态
            self.check()
        else:
            # 如果鼠标点击位置不在雷区表面内，则检查是否点击了重置按钮
            if self.reset_button.rect.collidepoint(event.pos) and event.button == 1:
                # 重置游戏
                self.restart()
                # 刷新游戏界面
                self.reflash()

    @log  # 日志装饰器，用于记录函数调用
    def check(self):
        # 检查未探索或标记的单元格数量是否等于地雷数量
        if len([j for i in self.minefield for j in i if j.type in Cell_Type.Unexplored_Set | Cell_Type.Flag_Set]) == self.level.mine_count:
            # 设置游戏结束标志
            self.end = True
            # 创建一个Tkinter窗口实例
            a = tk.Tk()
            # 隐藏主窗口
            a.withdraw()
            # 显示信息框，提示玩家胜利，并显示游戏时间
            messagebox.showinfo(
                'Win', f'Win\nTime:{self.Timer+time.time()-self.time}\nSize:{self.level.x}x{self.level.y}\nMine:{self.level.mine_count}')
            # 退出Tkinter应用程序
            a.quit()

    @log  # 日志装饰器，用于记录函数调用
    def restart(self,):
        """重置地雷位置
        """
        def reset(n: Cell):
            """重置单个单元格的状态
            参数:
                n (Cell): 需要重置的单元格
            """
            n.type = Cell_Type.Safe_Unexplored  # 将单元格类型设置为未探索的安全区域
            n.number = 0  # 将单元格的数字设置为0

        # 遍历整个地雷区域，对所有类型为地雷的单元格进行重置
        [reset(i) for j in self.minefield for i in j ]

        # 设置游戏运行状态为False
        self.run = False

        # print('restart')  # 打印重置完成的信息

    @log  # 日志装饰器，用于记录函数调用
    def click_cell(self, event, pos: Cell):
        """
        处理单元格点击事件的函数。

        参数:
        - event: 鼠标事件对象。
        - pos: 被点击的单元格对象。

        返回:
        - bool: 如果踩雷，返回True；否则返回False。
        """
        # 如果单元格的mouse_click方法成功处理了事件，返回True
        if pos.mouse_click(event):
            return True

        # 如果点击事件是左键点击
        if event.button == 1:
            # 如果被点击的单元格的数字为0
            if pos.number == 0:
                self.traversal(event, pos, 0)  # 遍历周围的单元格
            else:
                # 检查周围标记数量
                flag_count = 0
                for i in range(pos.pos[0]-1, pos.pos[0]+2):
                    if i < 0:  # 如果x坐标小于0，跳过
                        continue
                    for j in range(pos.pos[1]-1, pos.pos[1]+2):
                        if j < 0:  # 如果y坐标小于0，跳过
                            continue
                        try:
                            if self.Flag[(i, j)]:
                                flag_count += 1
                        except KeyError:
                            pass  # 捕获键错误，跳过
                # 如果周围标记数量等于数字，则
                if flag_count == pos.number:
                    self.traversal(event, pos, 1)
                ...
        return False  # 如果未踩雷，返回False

    @log  # 日志装饰器，用于记录函数调用
    def traversal(self,event: pygame.event.Event, pos: Cell, mode: int):
        """
        遍历周围的单元格，并对每个单元格进行处理。

        参数:
        - pos: 被点击的单元格对象。
        """
        # 遍历周围的单元格
        x = pos.pos[0]  # 获取单元格的x坐标
        y = pos.pos[1]  # 获取单元格的y坐标
        # 遍历被点击单元格周围的8个单元格
        for i in range(x-1, x+2):
            if i < 0:  # 如果x坐标小于0，跳过
                continue
            for j in range(y-1, y+2):
                if j < 0:  # 如果y坐标小于0，跳过
                    continue
                try:
                    posTemp = self.minefield[i][j]  # 获取临时单元格对象
                    # 如果临时单元格的类型是未探索的
                    if posTemp.type in Cell_Type.Unexplored_Set:
                        if mode == 0:
                            # 递归调用click_cell处理临时单元格的点击事件
                            if self.click_cell(event, posTemp):
                                # 记录游戏错误日志
                                Log(f'Game Error{posTemp} {self.mouse_motion_pos.pos}')
                                # 抛出系统错误
                                raise SystemError(
                                    f'Game Error{posTemp} {self.mouse_motion_pos.pos}')
                        elif mode == 1:
                            posTemp.mouse_click(event)  # 处理临时单元格的点击事件
                except IndexError:
                    pass  # 捕获索引错误，跳过

    def mouse_motion(self, event: pygame.event.Event):
        """鼠标移动事件
        处理鼠标在游戏区域内的移动事件
        """
        # 检查鼠标位置是否在雷区表面矩形内
        if self.minefield_surface.get_rect(topleft=self.minefield_surface_rect).collidepoint(event.pos):
            # 遍历雷区中的每个方块
            for i in self.minefield:
                for j in i:
                    # 检查鼠标是否在当前方块的矩形内
                    if j.rect.collidepoint(event.pos):
                        # 设置前一个鼠标悬停方块的mouse属性为False
                        self.mouse_motion_pos.mouse = False
                        # 设置当前方块的mouse属性为True
                        j.mouse = True
                        # 更新鼠标悬停位置为当前方块
                        self.mouse_motion_pos = j
        elif self.reset_button.rect.collidepoint(event.pos):
            self.mouse_motion_pos.mouse = False
            self.reset_button.mouse = True
            self.mouse_motion_pos = self.reset_button
        else:
            # 如果鼠标不在雷区表面矩形内，则设置前一个鼠标悬停方块的mouse属性为False
            self.mouse_motion_pos.mouse = False
            # 更新鼠标悬停位置为no_pos（一个默认的空位置）
            self.mouse_motion_pos = self.no_pos
            # 设置no_pos的mouse属性为True
            self.mouse_motion_pos.mouse = True

    def update(self):
        """
        更新游戏时间
        """
        # 获取当前时间戳
        current_time = time.time()

        # 检查当前时间与上一次更新时间的差值是否大于或等于1秒
        if current_time - self.time >= 1:
            # 如果大于或等于1秒，则将self.time增加1秒
            self.time += 1

            # 同时将计时器self.Timer增加1
            self.Timer += 1

        # 其他代码...

    def reflash(self):
        """重绘游戏界面
        """
        # 使用灰色填充屏幕
        self.screen.fill(color.Gray_X11)

        # 定义一个矩形区域，用于绘制边界
        Rect = (0, 0, self.minefield_surface_border.get_width(),
                self.minefield_surface_border.get_height())

        # 生成一个新的矩形区域，用于绘制地雷区域
        rect = (i-1 for i in self.minefield_surface_rect)

        # 使用黑色绘制地雷区域的边界
        pygame.draw.rect(self.minefield_surface_border,
                         (0, 0, 0, 156), Rect, 1)

        # 使用灰色填充地雷区域
        self.minefield_surface.fill(color.Gray_X11)

        # 刷新地雷区域中的每个元素
        [i.reflash() for j in self.minefield for i in j]

        # 将地雷区域边界绘制到屏幕上
        self.screen.blit(self.minefield_surface_border, tuple(rect))

        # 将地雷区域绘制到屏幕上
        self.screen.blit(self.minefield_surface, self.minefield_surface_rect)

        # 绘制重置按钮
        self.reset_button.reflash()

    def set_mine(self):
        """设置地雷
        """
        # 初始化地雷计数器
        mine_count = 0

        # 循环直到地雷数量达到设定值
        while mine_count <= self.level.mine_count-1:
            # 随机生成x坐标
            x = random.randint(0, self.level.x-1)
            # 随机生成y坐标
            y = random.randint(0, self.level.y-1)

            # 检查该位置是否已经是地雷
            if self.minefield[x][y].type not in Cell_Type.Mine_Set:
                # 如果该位置是鼠标悬停位置，则跳过
                if self.minefield[x][y] == self.mouse_motion_pos:
                    continue

                # 设置该位置为地雷
                self.minefield[x][y].type += Cell_Type.Mine

                # 地雷计数器加1
                mine_count += 1

                # 初始化日志列表，记录地雷位置
                Log_List = [(x, y)]

                # 遍历地雷周围的格子
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        # 跳过越界的格子
                        if i < 0 or j < 0:
                            continue

                        try:
                            # 增加周围格子的数字标记
                            self.minefield[i][j].number += 1
                        except IndexError:
                            # 捕获越界错误
                            pass
                        else:
                            # 记录周围格子的位置
                            Log_List.append((i, j))

                # 记录日志
                Log(Log_List)

        # 记录整个雷区的数字和地雷分布
        Log(*[''.join([str(i.number) if i.type in Cell_Type.Safe_Set else '*' for i in j])
            for j in self.minefield])
