"""启动页面
"""

import pygame
import snd.color as color
import snd.constant as constant
from snd.game import Game

pygame.init()
pygame.display.set_caption(constant.SCREEN_TITLE)

running = True

clock = pygame.time.Clock()
screen = pygame.display.set_mode(constant.SCREEN_SIZE)
screen.fill(color.White)

game = Game(20,20)
game_run = True

while running:
    if game_run == False:
        game = Game()
        game_run = True
        screen = game.screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            game.mouse_motion(event)
            game.reflash()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print('按下鼠标左键')
            elif event.button == 3:
                print('按下鼠标右键')
            game.mouse_click(event)
            game.reflash()
    if game.end:
        game_run = False
    if game.run:
        game.update()
    pygame.display.update()
    clock.tick(constant.FPS)
    

pygame.quit()