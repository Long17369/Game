"""启动页面
"""

import pygame
import snd.color as color
import snd.constant as constant
from snd.game import Game

# 初始化pygame
pygame.init()
# 设置窗口标题
pygame.display.set_caption(constant.SCREEN_TITLE)

# 设置游戏运行标志
running = True

# 创建时钟对象，用于控制帧率
clock = pygame.time.Clock()

# 创建游戏对象，初始难度为初级
game = Game(constant.LEVEL.BEGINNER)
# 设置游戏运行标志
game_run = True

# 主循环
while running:
    # 处理事件
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            # 如果检测到关闭窗口事件，设置running为False，退出主循环
            running = False
        elif event.type == pygame.MOUSEMOTION:
            # 处理鼠标移动事件
            game.mouse_motion(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 处理鼠标按键按下事件
            game.mouse_click(event)
    
    # 如果游戏结束，重新初始化游戏对象
    if game.end:
        pygame.event.clear()
        game = Game(constant.LEVEL.BEGINNER)
        screen = game.screen
    
    # 如果游戏正在运行，更新游戏状态
    if game.run:
        game.update()
    
    # 更新屏幕显示
    game.reflash()
    pygame.display.update()
    # 控制帧率
    clock.tick(constant.FPS)

# 退出pygame
pygame.quit()