import time


class Engine:
    def __init__(self, board):
        self.board = board
        self.checkpoint = 0
        # 0 - stat 1 - right 2 - up 3 - left 4 - down

    def intersectionRect(self, r1, r2):
        lx = max(r1[0], r2[0])
        rx = min(r1[0]+r1[2], r2[0]+r2[2])
        ly = max(r1[1], r2[1])
        ry = min(r1[1]+r1[3], r2[1]+r2[3])
        if (lx < rx) and (ly < ry):
            return (rx - lx) * (ry - ly)
        else:
            return 0

    def intersectionBW(self, ball, wall):
        if ball[3] == 1 and self.intersectionRect([ball[0]-ball[2], ball[1]-ball[2], 2*ball[2], 2*ball[2]], wall) > 0:
            return max(0, (ball[0]+ball[2])-(wall[0]))
        elif ball[3] == 2 and self.intersectionRect([ball[0]-ball[2], ball[1]-ball[2], 2*ball[2], 2*ball[2]], wall) > 0:
            return max(0, (wall[1]+wall[3])-(ball[1]-ball[2]))
        elif ball[3] == 3 and self.intersectionRect([ball[0]-ball[2], ball[1]-ball[2], 2*ball[2], 2*ball[2]], wall) > 0:
            return max(0, (wall[0]+wall[2])-(ball[0]-ball[2]))
        elif ball[3] == 4 and self.intersectionRect([ball[0]-ball[2], ball[1]-ball[2], 2*ball[2], 2*ball[2]], wall) > 0:
            return max(0, (ball[1]+ball[2])-(wall[1]))
        return 0

    def intersectionPW(self, player, wall):
        return self.intersectionRect(player, wall)

    def intersectionPB(self, player, ball):
        return self.intersectionRect(player, [ball[0]-ball[2], ball[1]-ball[2], 2*ball[2], 2*ball[2]])

    def intersectionPG(self, player, goal):
        return self.intersectionRect(player, goal)

    def checkpoint_crossed(self, checkpoint, x, y):
        if checkpoint[2] == 0 or checkpoint[2] == 4:
            return x >= checkpoint[0]
        elif checkpoint[2] == 1 or checkpoint[2] == 5:
            return y < checkpoint[1]
        elif checkpoint[2] == 2 or checkpoint[2] == 6:
            return x < checkpoint[0]
        else:
            return y >= checkpoint[1]

    def reward_calculation(self, x, y, prev_x, prev_y, chk_index):
        checkpoint = self.board.checkpoints[chk_index]
        # distance_sq = (x-checkpoint[0])* (x-checkpoint[0]) + (y-checkpoint[1])* (y-checkpoint[1])
        if checkpoint[2] == 0 or checkpoint[2] == 2:
            distance_sq = abs(x-checkpoint[0])
        elif checkpoint[2] == 1 or checkpoint[2] == 3:
            distance_sq = abs(y-checkpoint[1])
        else:
            distance_sq = abs(x-checkpoint[0]) + abs(y-checkpoint[1])
        total_distance = abs(prev_x-checkpoint[0]) + abs(prev_y-checkpoint[1])
        reward = checkpoint[3] * (total_distance-distance_sq) / total_distance
        return reward

    def move(self):
        reward = 0
        for ball in self.board.balls:
            if ball[3] == 1:
                ball[0] += self.board.ballSpeed
                for wall in self.board.walls:
                    overlap = self.intersectionBW(ball, wall)
                    if overlap > 0:
                        ball[0] -= 2*overlap
                        ball[3] = 3
                        break
            elif ball[3] == 2:
                ball[1] -= self.board.ballSpeed
                for wall in self.board.walls:
                    overlap = self.intersectionBW(ball, wall)
                    if overlap > 0:
                        ball[1] += 2*overlap
                        ball[3] = 4
                        break
            elif ball[3] == 3:
                ball[0] -= self.board.ballSpeed
                for wall in self.board.walls:
                    overlap = self.intersectionBW(ball, wall)
                    if overlap > 0:
                        ball[0] += 2*overlap
                        ball[3] = 1
                        break
            elif ball[3] == 4:
                ball[1] += self.board.ballSpeed
                for wall in self.board.walls:
                    overlap = self.intersectionBW(ball, wall)
                    if overlap > 0:
                        ball[1] -= 2*overlap
                        ball[3] = 2
                        break

        # self.checkpoint = 0
        # for idx, checkpoint in enumerate(self.board.checkpoints):
        #     original_crossed = self.checkpoint_crossed(checkpoint, orig_x + self.board.player[2]/2, orig_y + self.board.player[3]/2)
        #     new_crossed = self.checkpoint_crossed(checkpoint, self.board.player[0] + self.board.player[2]/2, self.board.player[1] + self.board.player[3]/2)
        #     if (not original_crossed) and new_crossed:
        #         reward += checkpoint[3]
        #     elif original_crossed and (not new_crossed):
        #         reward -= 2*checkpoint[3]
        #     if new_crossed:
        #         self.checkpoint = idx + 1
        # reward += self.reward_calculation(orig_x, orig_y)

        return False, reward

    def check_collisions(self, orig_x, orig_y, new_x, new_y, size_x, size_y):
        for wall in self.board.walls:
            overlap = self.intersectionPW([new_x, new_y, size_x, size_y], wall)
            if overlap > 0:
                return False, False, True, [orig_x, orig_y]

        if self.intersectionPG([new_x, new_y, size_x, size_y], self.board.goal) == size_x * size_y:
            return True, False, False, [new_x, new_y]

        for idx, ball in enumerate(self.board.balls):
            if self.intersectionPB([min(new_x, orig_x), min(new_y, orig_y), size_x + abs(new_x-orig_x), size_y + abs(new_y-orig_y)], ball) > 0:
                return False, True, False, [orig_x, orig_y]

        return False, False, False, [new_x, new_y]

    def calculate_fitness(self, player):
        chk_index = 0
        player.fitness = 0
        if player.goal_reached:
            player.fitness += self.board.goal[4]
        for idx, checkpoint in enumerate(self.board.checkpoints):
            crossed = self.checkpoint_crossed(checkpoint, player.pos[0]+player.size[0]/2, player.pos[1]+player.size[1]/2)
            if crossed:
                chk_index = idx+1
                player.fitness += checkpoint[3]
        if chk_index == 0:
            prev_x = self.board.pos_size[0][0]
            prev_y = self.board.pos_size[0][1]
        else:
            prev_x = self.board.checkpoints[chk_index - 1][0]
            prev_y = self.board.checkpoints[chk_index - 1][1]
        while chk_index < len(self.board.checkpoints) and self.board.checkpoints[chk_index][2] < 4:
            chk_index += 1
        if chk_index < len(self.board.checkpoints):
            player.fitness += self.reward_calculation(player.pos[0], player.pos[1], prev_x, prev_y, chk_index)

    def get_checkpoint(self, player):
        chk_index = 0
        for idx, checkpoint in enumerate(self.board.checkpoints):
            crossed = self.checkpoint_crossed(checkpoint, player.pos[0] + player.size[0],
                                              player.pos[1] + player.size[1])
            if crossed:
                chk_index = idx+1
        return chk_index

