from envs.Board import Board
import sys
import pygame

if __name__ == '__main__':
    b = Board()
    action = 0
    thr = 0
    mx = 5
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
                thr = 4
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and action == 1:
                    action = 0
                if event.key == pygame.K_UP and action == 2:
                    action = 0
                if event.key == pygame.K_LEFT and action == 3:
                    action = 0
                if event.key == pygame.K_DOWN and action == 4:
                    action = 0
            elif event.type == pygame.QUIT:
                b.close()
                sys.exit()
        if thr == 0:
            if b.player.move(0) != 0:
                b.close()
                break
        else:
            if b.player.move(action) != 0:
                b.close()
                break
        thr = (thr + mx - 1) % mx
        # time.sleep(0.1)
