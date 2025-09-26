import pygame
from glogic import Player
import glogic

# 初始化 Pygame
pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Python Game")

# 创建角色
user1 = Player.createplayer()

barrier = glogic.barrier.create_barrier()

# 字体对象
font = pygame.font.SysFont("Arial", 30)

clock = pygame.time.Clock()

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充背景颜色（RGB）
    screen.fill((0, 128, 255))

    # 渲染玩家名字
    name_text = font.render(f"Name: {user1.name}", True, (255, 255, 255))
    atk_text = font.render(f"ATK: {user1.atk}", True, (255, 255, 255))
    hp_text = font.render(f"HP: {user1.hp}", True, (255, 255, 255))
    
    user1.move()
    
    pygame.draw.rect(screen, (255, 255, 0), (user1.player_x, user1.player_y, user1.player_width, user1.player_height))

    pygame.draw.rect(screen, (128,255,128), (barrier.x,barrier.y,barrier.length,barrier.length))
    
    user1.iscollapse(barrier)
    
    # 把文字贴到屏幕上 (x, y 位置)
    
    screen.blit(name_text, (50, 50))
    screen.blit(atk_text, (50, 100))
    screen.blit(hp_text, (50, 150))
    clock.tick(60)
    # 更新显示内容
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
