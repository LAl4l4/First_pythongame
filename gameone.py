import pygame
from glogic import Player
import glogic

# 初始化 Pygame
pygame.init()


WIDTH, HEIGHT = 800, 600
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
screen = pygame.display.set_mode((800, 600))
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

rowlen = 16
collen = 12
TileSize = 100
gMap = glogic.Map.getMap(rowlen,collen,TileSize)


# 字体对象
font = pygame.font.SysFont("Arial", 30)

clock = pygame.time.Clock()

def draw_map(screen, map_obj, textures, player):
    for row in range(map_obj.rowlen):
        for col in range(map_obj.collen):
            texture_index = map_obj.map[row][col]
            texture = textures[texture_index]

            world_x = row * map_obj.TileSize
            world_y = col * map_obj.TileSize
            screen_x = world_x - player.player_x + CENTER_X
            screen_y = world_y - player.player_y + CENTER_Y

            if -map_obj.TileSize < screen_x < WIDTH and -map_obj.TileSize < screen_y < HEIGHT:
                screen.blit(texture, (screen_x, screen_y))

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充背景颜色（RGB）
    screen.fill((0, 128, 255))
    
    #背景部分
    draw_map(screen,gMap,textures,user1)

    # 渲染玩家名字
    name_text = font.render(f"{user1.name}", True, (255, 255, 255))
    atk_text = font.render(f"ATK: {user1.atk}", True, (255, 255, 255))
    hp_text = font.render(f"HP: {user1.hp}", True, (255, 255, 255))
    
    
    # player部分
    user1.move(bars)
    
    pygame.draw.rect(screen, (255, 255, 0), (CENTER_X, CENTER_Y, user1.player_width, user1.player_height))

    
    #barrier部分
    for bar in bars:
        bx, by = bar.BarGetCoodi(user1) 
        if -BarLength < bx < WIDTH and -BarLength < by < HEIGHT:
            pygame.draw.rect(screen, (128,255,128), (bx,by,bar.length,bar.length))
            

    

    
    # 把文字贴到屏幕上 (x, y 位置)
    
    screen.blit(name_text, (50, 50))
    screen.blit(atk_text, (50, 100))
    screen.blit(hp_text, (50, 150))
    clock.tick(59)
    # 更新显示内容
    pygame.display.flip()
    
    



# 退出 Pygame
pygame.quit()
