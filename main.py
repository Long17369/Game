"""启动页面
"""

import pygame
import snd.color as color
import snd.constant as constant

pygame.init()

running = True

screen = pygame.display.set_mode(constant.SCREEN_SIZE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(color.White)
    pygame.display.update()

pygame.quit()