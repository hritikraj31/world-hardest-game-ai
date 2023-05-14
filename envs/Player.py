from envs.Genes import Genes
import pygame


class Player:

    def __init__(self, pos, size, gene_length):
        self.pos = [pos[0], pos[1]]
        self.vel = [0, 0]
        self.acc = [0, 0]
        self.size = [size[0], size[1]]
        self.genes = Genes(gene_length)
        self.dead = False
        self.win = False
        self.fitness = 0
        self.is_best = False
        self.goal_reached = False

    def move(self):
        if self.dead:
            return
        if self.win:
            return
        if self.genes.index < len(self.genes.directions):
            self.acc[0] = self.genes.directions[self.genes.index][0]
            self.acc[1] = self.genes.directions[self.genes.index][1]
            self.genes.index += 1
        else:
            self.dead = True

        self.vel[0] = 3*self.acc[0]
        self.vel[1] = 3*self.acc[1]

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def draw(self, surf):
        if not self.dead:
            pygame.gfxdraw.box(surf, (self.pos[0], self.pos[1], self.size[0], self.size[1]), (50, 255, 50) if self.is_best else (0, 0, 255))
            border = 3
            border_color = (50, 50, 50)
            pygame.gfxdraw.box(surf, (self.pos[0], self.pos[1], self.size[0], border), border_color)
            pygame.gfxdraw.box(surf, (self.pos[0], self.pos[1], border, self.size[1]), border_color)
            pygame.gfxdraw.box(surf, (self.pos[0]+self.size[0] - border, self.pos[1], border, self.size[1]), border_color)
            pygame.gfxdraw.box(surf, (self.pos[0], self.pos[1]+self.size[1] - border, self.size[0], border), border_color)

    def clone(self, pos, size, GL):
        player = Player(pos, size, GL)
        player.genes = self.genes.clone(GL)
        return player

    def mutate(self):
        self.genes.mutate()
