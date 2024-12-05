import pygame
import random
import sys
import json
import os
from pygame.locals import *

# 初始化 Pygame
pygame.init()

# 游戏配置
class GameConfig:
    # 窗口设置
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    GRID_SIZE = 20
    FPS = 10  # 降低速度，使游戏更容易控制
    
    # 颜色定义
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = GameConfig.RED
        self.randomize_position()

    def randomize_position(self):
        # 确保食物生成在网格上
        max_x = (GameConfig.WINDOW_WIDTH - GameConfig.GRID_SIZE) // GameConfig.GRID_SIZE
        max_y = (GameConfig.WINDOW_HEIGHT - GameConfig.GRID_SIZE) // GameConfig.GRID_SIZE
        self.position = (
            random.randint(0, max_x) * GameConfig.GRID_SIZE,
            random.randint(0, max_y) * GameConfig.GRID_SIZE
        )

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0], self.position[1],
            GameConfig.GRID_SIZE - 2, GameConfig.GRID_SIZE - 2
        )
        pygame.draw.rect(surface, self.color, rect)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        # 初始化蛇的位置在屏幕中心
        center_x = (GameConfig.WINDOW_WIDTH // GameConfig.GRID_SIZE // 2) * GameConfig.GRID_SIZE
        center_y = (GameConfig.WINDOW_HEIGHT // GameConfig.GRID_SIZE // 2) * GameConfig.GRID_SIZE
        self.positions = [(center_x, center_y)]
        self.length = 1
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.score = 0
        self.color = GameConfig.GREEN
    
    def get_head_position(self):
        return self.positions[0]
    
    def move(self):
        current = self.get_head_position()
        x, y = self.direction
        new_position = (
            current[0] + x * GameConfig.GRID_SIZE,
            current[1] + y * GameConfig.GRID_SIZE
        )
        
        # 检查是否撞墙
        if (new_position[0] < 0 or 
            new_position[0] >= GameConfig.WINDOW_WIDTH or
            new_position[1] < 0 or 
            new_position[1] >= GameConfig.WINDOW_HEIGHT):
            return False
        
        # 检查是否撞到自己
        if new_position in self.positions[2:]:
            return False
        
        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def draw(self, surface):
        for position in self.positions:
            rect = pygame.Rect(
                position[0], position[1],
                GameConfig.GRID_SIZE - 2, GameConfig.GRID_SIZE - 2
            )
            pygame.draw.rect(surface, self.color, rect)

class ScoreBoard:
    def __init__(self):
        self.scores_file = "high_scores.json"
        self.high_scores = self.load_scores()
    
    def load_scores(self):
        if os.path.exists(self.scores_file):
            try:
                with open(self.scores_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_scores(self):
        with open(self.scores_file, 'w') as f:
            json.dump(self.high_scores, f)
    
    def add_score(self, score):
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:5]  # 只保留前5个最高分
        self.save_scores()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (GameConfig.WINDOW_WIDTH, GameConfig.WINDOW_HEIGHT)
        )
        pygame.display.set_caption('贪吃蛇')
        
        # 尝试加载中文字体
        try:
            self.font = pygame.font.Font("simhei.ttf", 36)
        except:
            try:
                self.font = pygame.font.SysFont("microsoftyaheimicrosoftyaheiui", 36)
            except:
                self.font = pygame.font.Font(None, 36)
        
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score_board = ScoreBoard()
        
        self.game_over = False
        self.showing_scores = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                if event.key == K_SPACE:
                    if self.showing_scores:
                        self.showing_scores = False
                    elif self.game_over:
                        self.reset_game()
                if event.key == K_TAB and self.game_over:
                    self.showing_scores = True
                
                if not self.game_over and not self.showing_scores:
                    if event.key == K_UP and self.snake.direction != (0, 1):
                        self.snake.direction = (0, -1)
                    elif event.key == K_DOWN and self.snake.direction != (0, -1):
                        self.snake.direction = (0, 1)
                    elif event.key == K_LEFT and self.snake.direction != (1, 0):
                        self.snake.direction = (-1, 0)
                    elif event.key == K_RIGHT and self.snake.direction != (-1, 0):
                        self.snake.direction = (1, 0)
        return True
    
    def reset_game(self):
        if self.snake.score > 0:
            self.score_board.add_score(self.snake.score)
        self.snake.reset()
        self.food.randomize_position()
        self.game_over = False
    
    def update(self):
        if not self.game_over and not self.showing_scores:
            if not self.snake.move():
                self.game_over = True
                return
            
            # 检查是否吃到食物
            if self.snake.get_head_position() == self.food.position:
                self.snake.length += 1
                self.snake.score += 1
                self.food.randomize_position()
                # 确保食物不会出现在蛇身上
                while self.food.position in self.snake.positions:
                    self.food.randomize_position()
    
    def draw_high_scores(self):
        self.screen.fill(GameConfig.BLACK)
        title = self.font.render("排行榜", True, GameConfig.WHITE)
        title_rect = title.get_rect(center=(GameConfig.WINDOW_WIDTH/2, 50))
        self.screen.blit(title, title_rect)
        
        for i, score in enumerate(self.score_board.high_scores):
            text = self.font.render(f"第{i+1}名: {score}", True, GameConfig.WHITE)
            rect = text.get_rect(center=(GameConfig.WINDOW_WIDTH/2, 150 + i*50))
            self.screen.blit(text, rect)
        
        instruction = self.font.render("按空格键返回", True, GameConfig.WHITE)
        inst_rect = instruction.get_rect(center=(GameConfig.WINDOW_WIDTH/2, GameConfig.WINDOW_HEIGHT-50))
        self.screen.blit(instruction, inst_rect)
    
    def draw(self):
        if self.showing_scores:
            self.draw_high_scores()
        else:
            self.screen.fill(GameConfig.BLACK)
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            
            score_text = self.font.render(f'分数: {self.snake.score}', True, GameConfig.WHITE)
            self.screen.blit(score_text, (10, 10))
            
            if self.game_over:
                game_over_text = self.font.render('游戏结束!', True, GameConfig.WHITE)
                text_rect = game_over_text.get_rect(center=(GameConfig.WINDOW_WIDTH/2, GameConfig.WINDOW_HEIGHT/2 - 30))
                self.screen.blit(game_over_text, text_rect)
                
                instruction_text = self.font.render('按空格键重新开始，按TAB键查看排行榜', True, GameConfig.WHITE)
                inst_rect = instruction_text.get_rect(center=(GameConfig.WINDOW_WIDTH/2, GameConfig.WINDOW_HEIGHT/2 + 30))
                self.screen.blit(instruction_text, inst_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(GameConfig.FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run() 