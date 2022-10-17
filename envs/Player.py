class Player:
    def __init__(self, x, y, board):
        self.board = board
        self.x = x
        self.y = y
        # 0 - stat 1 - right 2 - up 3 - left 4 - down

    def move(self, action):
        [orig_x, orig_y] = [self.x, self.y]
        if action == 1:
            self.y += 1
        elif action == 2:
            self.x -= 1
        elif action == 3:
            self.y -= 1
        elif action == 4:
            self.x += 1
        original_balls = [x.copy() for x in self.board.balls]
        for ball in self.board.balls:
            if ball[2] == 1:
                ball[1] += 1
                if self.board.grid[ball[0]][ball[1]] == 1:
                    ball[1] -= 2
                    ball[2] = 3
            elif ball[2] == 2:
                ball[0] -= 1
                if self.board.grid[ball[0]][ball[1]] == 1:
                    ball[0] += 2
                    ball[2] = 4
            elif ball[2] == 3:
                ball[1] -= 1
                if self.board.grid[ball[0]][ball[1]] == 1:
                    ball[1] += 2
                    ball[2] = 1
            elif ball[2] == 4:
                ball[0] += 1
                if self.board.grid[ball[0]][ball[1]] == 1:
                    ball[0] -= 2
                    ball[2] = 2

        if self.board.grid[self.x][self.y] == 1:
            self.x = orig_x
            self.y = orig_y
        elif self.board.grid[self.x][self.y] == 3:
            return 1
        else:
            for idx, ball in enumerate(self.board.balls):
                if (self.x == ball[0] and self.y == ball[1]) or (orig_x == ball[0] and orig_y == ball[1] and self.x == original_balls[idx][0] and self.y == original_balls[idx][1]):
                    return -1
        for ball in original_balls:
            self.board.grid[ball[0]][ball[1]] = 0
        self.board.grid[orig_x][orig_y] = 0
        for ball in self.board.balls:
            self.board.grid[ball[0]][ball[1]] = ball[2]+3
        self.board.grid[self.x][self.y] = 2
        return 0
