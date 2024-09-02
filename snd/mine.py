"""格子
"""

import pygame
import snd.color as color
from snd.draw import Draw


class Cell_Type():
    # 定义单元格类型类，用于表示扫雷游戏中的各种单元格状态
    Safe_Unexplored = 0     # 未挖 安全
    Mine = 1                # 地雷
    Mine_Unexplored = 1     # 未挖 地雷
    Flag = 2                # 标记
    Safe_Flag = 2           # 标记 安全
    Mine_Flag = 3           # 标记 地雷
    Explored = 4            # 已挖
    Safe_explored = 4       # 已挖 安全
    Mine_explored = 5       # 已挖 地雷
    Safe_Set = {Safe_Unexplored, Safe_Flag, Safe_explored}      # 安全的单元格集合
    Mine_Set = {Mine_Unexplored, Mine_Flag, Mine_explored}      # 地雷的单元格集合
    All = Safe_Set | Mine_Set                                       # 所有的单元格集合
    Unexplored_Set = {Safe_Unexplored, Mine_Unexplored}         # 未探索的单元格集合
    Explored_Set = {Safe_explored, Mine_explored}               # 已探索的单元格集合
    Flag_Set = {Safe_Flag, Mine_Flag}                           # 标记的单元格集合
    No_Flag = All - Flag_Set                                    # 未标记的单元格集合
    Reset_Button = 10086    # 重置


class Cell():
    """格子"""

    number: int = 0
    mouse: bool = False
    type = Cell_Type.Safe_Unexplored
    size: int = 0

    def __init__(self, x: int, y: int, game_surface: pygame.Surface, size: int = 25):
        """
        初始化棋子对象。

        x: 棋子的x坐标
        y: 棋子的y坐标
        game_surface: 棋子所在的pygame Surface对象
        size: 棋子的大小，默认为25
        """
        # 特殊情况处理：如果x和y都为-1，则表示这个棋子代表雷区之外的区域
        if x == -1 and y == -1:
            self.mouse = True
        # 初始化棋子的坐标、大小和相关属性
        self.x = x
        self.y = y
        self.size = size
        self.pos = (x, y)
        self.Rect_x = x * size
        self.Rect_y = y * size
        # 定义棋子在游戏界面中的矩形区域
        self.Rect = (x * size, y * size, size, size)
        self.Draw = Draw(size, game_surface)
        # 保存游戏界面的Surface对象
        self.game_surface = game_surface
        # 初始化棋子的绘制参数，包括颜色和图形等
        self.cell_list = [
            (255, 255, 255, 128),
            [(0, 0), (size, 0), (0, size)],
            (0, 0, 0, 64),
            [(size, size), (size, 0), (0, size)],
            (3, 3, size - 6, size - 6)
        ]

    def __str__(self) -> str:
        return f'Cell(x:{self.x},y:{self.y},mouse:{self.mouse},type:{self.type},number:{self.number})'

    def get_rect(self, topleft):
        """获取棋子的矩形区域"""
        self.rect = self.surface.get_rect(
            topleft=(topleft[0]+self.Rect_x, topleft[1]+self.Rect_y))

    def mouse_click(self, event: pygame.event.Event):
        """
        处理鼠标点击事件。

        根据不同的鼠标按钮和当前单元格状态，更改单元格的类型。
        支持左键点击和右键点击操作，用于标记和取消标记单元格。

        参数:
        event 包含事件信息

        返回:
        如果点击的单元格是隐藏的雷，则返回True，否则返回False。
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 左键点击且单元格为未探索状态，探雷
            if event.button == 1 and self.type in Cell_Type.Unexplored_Set:
                self.Draw.number = self.number
                self.type += Cell_Type.Explored
            # 左键点击已标记为旗子的单元格，无动作
            elif event.button == 1 and self.type in Cell_Type.Flag_Set:
                ...
            # 点击已探索的单元格，无动作
            elif self.type in Cell_Type.Explored_Set:
                ...
            # 右键点击标记为旗子的单元格，将其类型改为未探索
            elif event.button == 3 and self.type in Cell_Type.Flag_Set:
                self.type -= Cell_Type.Flag
            # 右键点击未探索的单元格，将其标记为旗子
            elif event.button == 3 and self.type in Cell_Type.Unexplored_Set:
                self.type += Cell_Type.Flag
            else:
                # 出现未知的鼠标点击情况，打印错误信息和点击按钮及单元格类型
                print('error')
                print(event.button)
                print(self.type)
        # 返回点击的单元格是否为探查过的雷
        return self.type == Cell_Type.Mine_explored

    def reflash(self):
        # 根据当前单元格的大小创建一个透明的Surface
        size = self.size
        self.surface = pygame.Surface((size, size), flags=pygame.SRCALPHA)
        self.Draw.surface = self.surface
        # 为Surface添加一个黑色边缘
        pygame.draw.rect(self.surface, (0, 0, 0, 64), (0, 0, size, size), 1)

        # 如果当前单元格未探索或被标记
        if self.type in Cell_Type.Unexplored_Set | Cell_Type.Flag_Set:
            # 绘制单元格本身
            self.Draw.draw_cell()
            # 如果鼠标在单元格上，绘制高亮效果
            if self.mouse:
                self.Draw.draw_highlight()
            # 如果单元格被标记，绘制旗帜
            if self.type in Cell_Type.Flag_Set:
                self.Draw.draw_cell()
                self.Draw.draw_flag()

        # 如果当前单元格是已探索类型
        if self.type in Cell_Type.Explored_Set:
            # 如果单元格周围有雷，绘制数字
            if self.number != 0:
                self.Draw.draw_number()

        # 如果当前单元格是重置按钮
        if self.type == Cell_Type.Reset_Button:
            self.Draw.draw_cell()
            self.Draw.draw_reset()
            # 如果鼠标在单元格上，绘制高亮效果
            if self.mouse:
                self.Draw.draw_highlight()

        # 将Surface内容绘制到游戏主界面上
        self.game_surface.blit(self.surface, (self.Rect_x, self.Rect_y))

    def set_Rect(self, x, y):
        self.Rect_x = x * self.size
        self.Rect_y = y * self.size
