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

    def reward_calculation(self, orig_x, orig_y):
        checkpoint = self.board.checkpoints[self.checkpoint]
        distance1 = 0
        distance2 = 0
        if checkpoint[2] == 0 or checkpoint[2] == 2:
            distance1 = abs(orig_x - checkpoint[0])
            distance2 = abs(self.board.player[0] - checkpoint[0])
        elif checkpoint[2] == 1 or checkpoint[2] == 3:
            distance1 = abs(orig_y - checkpoint[1])
            distance2 = abs(self.board.player[1] - checkpoint[1])
        else:
            distance1 = abs(orig_x - checkpoint[0]) + abs(orig_y - checkpoint[1])
            distance2 = abs(self.board.player[0] - checkpoint[0]) + abs(self.board.player[1] - checkpoint[1])
        reward = (distance1 - distance2)/((1 + distance1) * (1 + distance2))
        if reward < 0:
            reward -= 0.1
        return reward

    def move(self, action):
        reward = 0
        [orig_x, orig_y] = [self.board.player[0], self.board.player[1]]
        if action == 1:
            self.board.player[0] += self.board.playerSpeed
        elif action == 2:
            self.board.player[1] -= self.board.playerSpeed
        elif action == 3:
            self.board.player[0] -= self.board.playerSpeed
        elif action == 4:
            self.board.player[1] += self.board.playerSpeed
        else:
            reward -= 0.5
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

        for wall in self.board.walls:
            overlap = self.intersectionPW(self.board.player, wall)
            if overlap > 0:
                self.board.player[0] = orig_x
                self.board.player[1] = orig_y
                reward -= 50
        reached_goal = self.intersectionPG(self.board.player, self.board.goal)
        if reached_goal == self.board.player[2]*self.board.player[3]:
            return True, 5
        for idx, ball in enumerate(self.board.balls):
            if self.intersectionPB(self.board.player, ball) > 0:
                return True, -2
        self.checkpoint = 0
        for idx, checkpoint in enumerate(self.board.checkpoints):
            original_crossed = self.checkpoint_crossed(checkpoint, orig_x + self.board.player[2]/2, orig_y + self.board.player[3]/2)
            new_crossed = self.checkpoint_crossed(checkpoint, self.board.player[0] + self.board.player[2]/2, self.board.player[1] + self.board.player[3]/2)
            if (not original_crossed) and new_crossed:
                reward += checkpoint[3]
            elif original_crossed and (not new_crossed):
                reward -= checkpoint[3]
            if new_crossed:
                self.checkpoint = idx + 1
        reward += self.reward_calculation(orig_x, orig_y)

        return False, reward
