import pygame
from glogic import Player
import glogic

# 初始化 Pygame
pygame.init()


WIDTH, HEIGHT = glogic.WIDTH, glogic.HEIGHT
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Game")

#地图纹理
texture_img = pygame.image.load("pygameone/map_background.png").convert()
tile_width = texture_img.get_width() // 3 - 1
tile_height = texture_img.get_height() // 4 - 1

textures = []
for row in range(3):
    for col in range(4):
        rect = pygame.Rect(row * tile_width, col * tile_height, tile_width, tile_height)
        tile = texture_img.subsurface(rect).copy()
        tile = pygame.transform.scale(tile, (100, 100)) 
        textures.append(tile)

# 创建角色
user1 = Player.createplayer()

BarLength = 80
bars = [glogic.barrier.create_barrier(BarLength) for _ in range(5)]

TileSize = 100
rowlen = 2*WIDTH // TileSize
collen = 2*HEIGHT // TileSize

gMap = glogic.Map.getMap(rowlen,collen,TileSize)


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
    
    #背景部分
    glogic.Map.draw_map(screen,gMap,textures,user1)

    # 渲染玩家名字
    name_text = font.render(f"{user1.name}", True, (255, 255, 255))
    atk_text = font.render(f"ATK: {user1.atk}", True, (255, 255, 255))
    hp_text = font.render(f"HP: {user1.hp}", True, (255, 255, 255))
    
    
    # player部分
    user1.move(bars)
    
    pygame.draw.rect(screen, (255, 255, 0), (user1.Drawx, user1.Drawy, user1.player_width, user1.player_height))

    
    #barrier部分
    for bar in bars:
        bx, by = bar.BarGetCoodi(user1) 
        if -BarLength < bx < WIDTH and -BarLength < by < HEIGHT:
            pygame.draw.rect(screen, (128,255,128), (bx,by,bar.length,bar.length))
            
    user1.attack(bars,screen)
    

    
    # 把文字贴到屏幕上 (x, y 位置)
    
    screen.blit(name_text, (50, 50))
    screen.blit(atk_text, (50, 100))
    screen.blit(hp_text, (50, 150))
    clock.tick(59)
    # 更新显示内容
    pygame.display.flip()
    
    



# 退出 Pygame
pygame.quit()
