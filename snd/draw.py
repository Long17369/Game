"""画图"""


import pygame
import snd.color as color


class Draw():

    number: int = 0

    def __init__(self, size: int = 25, surface: pygame.Surface = pygame.Surface((25, 25))):
        self.font = pygame.font.Font(None, size)
        self.surface = surface
        self.size = size
        self.cell_list = [
            (255, 255, 255, 128),
            [(0, 0), (size, 0), (0, size)],
            (0, 0, 0, 64),
            [(size, size), (size, 0), (0, size)],
            (3, 3, size - 6, size - 6)
        ]

    def draw_cell(self):
        """
        绘制格子

        此函数负责在图形界面上绘制一个细胞单元的形状和颜色。使用pygame库的绘制功能，
        通过self.cell_list存储的顶点信息来绘制阴影，并绘制格子本身。
        """
        # 获取绘制信息
        polygon = self.cell_list

        # 绘制阴影
        pygame.draw.polygon(self.surface, polygon[0], polygon[1])
        pygame.draw.polygon(self.surface, polygon[2], polygon[3])
        # 绘制格子
        pygame.draw.rect(self.surface, color.Silver, polygon[4])

    def draw_flag(self):
        """绘制旗帜"""
        size = self.size
        pygame.draw.polygon(self.surface, color.Red, [
                            (size/2, size/6), (size/2, size/2), (size/5, size/3)])
        pygame.draw.line(self.surface, color.Black,
                         (size/2, size/2), (size/2, size*0.7), int(size//25))
        pygame.draw.line(self.surface, color.Black, (size*0.25,
                         size*0.7), (size*0.75, size*0.7), int(size//25*2))

    def draw_highlight(self):
        """
        绘制高亮区域

        该方法用于在游戏界面中绘制一个半透明的白色高亮效果，用于突出显示某个区域。
        它通过创建一个带有SRCALPHA标志的Surface对象来实现半透明效果，然后在这个
        Surface对象上绘制一个白色的矩形，最后将这个Surface对象与游戏界面合并，达到
        高亮显示的效果。
        """
        size = self.size
        # 创建一个带有SRCALPHA标志的Surface对象，用于支持透明度设置
        a = pygame.Surface((size, size), flags=pygame.SRCALPHA)
        # 在Surface对象上绘制一个半透明的白色矩形
        pygame.draw.rect(a, (255, 255, 255, 128), (0, 0, size, size))
        # 将带有高亮效果的Surface对象绘制到游戏界面上
        self.surface.blit(a, (0, 0))

    def draw_number(self):
        """
        在游戏界面上绘制数字。
        首先使用字体对象渲染数字，然后计算数字的矩形位置，使其居中显示，
        最后将渲染好的数字绘制到Cell矩形区域上。
        """
        # 使用字体对象渲染数字，颜色为黑色
        number = self.font.render(str(self.number), True, color.Black)
        # 获取渲染后数字的矩形区域
        number_rect = number.get_rect()
        # 将数字矩形区域居中对齐到Cell矩形区域的中心
        number_rect.center = self.surface.get_rect().center
        # 将渲染好的数字绘制到Cell矩形区域上
        self.surface.blit(number, number_rect)

    def draw_reset(self):
        """
        绘制重置按钮。
        该方法用于在游戏界面上绘制一个“重置”按钮，当玩家点击该按钮时，游戏将会重置。
        """
        size = self.size
        # 创建一个带有SRCALPHA标志的Surface对象，用于支持透明度设置
        a = pygame.Surface((size, size), flags=pygame.SRCALPHA)
        # 在矩形上绘制一个小黄脸
        pygame.draw.circle(a, color.Gold, (size/2, size/2), size/3)
        # 添加边框
        pygame.draw.circle(a, color.Black, (size/2, size/2), size/3, 1)
        # 眼睛
        pygame.draw.circle(a, color.Black, (size*0.38, size/7*3), size/15)
        pygame.draw.circle(a, color.Black, (size*0.62, size/7*3), size/15)
        # 嘴巴
        mouth = pygame.Surface((size, size), flags=pygame.SRCALPHA)
        pygame.draw.circle(mouth, color.Black, (size/2, size*0.38), size/3, 1)
        pygame.draw.rect(mouth, (0,0,0,0), (0, 0, size, size/5*3))
        a.blit(mouth, (0,0))
        # 将带有重置按钮的Surface对象绘制到游戏界面上
        self.surface.blit(a, (0, 0))
