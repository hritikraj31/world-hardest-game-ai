from envs.Board import Board
import sys
import pygame

if __name__ == '__main__':
    b = Board()
    action = 0
    thr = 1
    print("Game Running ...")
    while True:
        b.draw()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    action = 1
                elif event.key == pygame.K_UP:
                    action = 2
                elif event.key == pygame.K_LEFT:
                    action = 3
                elif event.key == pygame.K_DOWN:
                    action = 4
                thr = 0
            elif event.type == pygame.KEYUP:
                action = 0
            elif event.type == pygame.QUIT:
                b.close()
                sys.exit()
        if thr > 0:
            thr -= 1
            if b.player.move(0) != 0:
                b.close()
                break
        else:
            thr = 1
            if b.player.move(action) != 0:
                b.close()
                break
        # time.sleep(0.1)
