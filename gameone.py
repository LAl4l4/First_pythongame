import pygame
from glogic import Player
import glogic

# 初始化 Pygame
pygame.init()


WIDTH, HEIGHT = glogic.WIDTH, glogic.HEIGHT
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.SCALED | pygame.DOUBLEBUF,vsync =1)
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

# create barrier
BarLength = 80
bars = [glogic.barrier.create_barrier(BarLength) for _ in range(5)]

# create enemy
EnemyHP = 100
EnemyATK = 20
EnemySpeed = 5
EnemyRadius = 100
Enemies = [glogic.Enemy.getEnemy(EnemyATK, EnemyHP, EnemySpeed,EnemyRadius) for _ in range(3)]

# create map
TileSize = 100
rowlen = 2*WIDTH // TileSize
collen = 2*HEIGHT // TileSize
gMap = glogic.Map.getMap(rowlen,collen,TileSize)


# 字体对象
font = pygame.font.SysFont("Arial", 30)
# 控制游戏帧率的时钟对象
clock = pygame.time.Clock()

# 装入totalObj Movable Drawable Attackable
# 把每个元素和它的参数打包成元组整体装入列表
totalObj = [user1, gMap, *bars, *Enemies]
movable_objects = [
    [user1, [bars]],  
    *[(enemy, [user1]) for enemy in Enemies]
]
IsRepackageDrawable = [False]#把这个存为可变类型，这样glogic里改了就能反映到这里
drawable_objects = [
    *[(gMap, [screen, textures, user1])],
    *[(bar, [screen, user1]) for bar in bars],
    *[(enemy, [screen, user1]) for enemy in Enemies]
] 
attackable_objects = [
    *[(bar, [user1]) for bar in bars],
    *[(enemy, [user1]) for enemy in Enemies]
]
canAttack_objects = [
    [user1, [screen]]
]

# 创建游戏世界对象
GameWorld = glogic.GameWorld(
    totalObj, drawable_objects, 
    movable_objects, attackable_objects,
    canAttack_objects)

# 游戏主循环
running = True
while running:
    #如果退出了就把游戏关了
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充背景颜色（RGB）
    screen.fill((0, 128, 255))

    # 渲染玩家名字
    name_text = font.render(f"{user1.name}", True, (255, 255, 255))
    atk_text = font.render(f"ATK: {user1.atk}", True, (255, 255, 255))
    hp_text = font.render(f"HP: {user1.hp}", True, (255, 255, 255))
    
    # game world update    
    GameWorld.updateMove()
    GameWorld.updateDraw()
    GameWorld.updateCanAttack()
    GameWorld.updateAttack()
    GameWorld.updateRemoveObjects()
            
    # player部分
    pygame.draw.rect(screen, (255, 255, 0), (user1.Drawx, user1.Drawy, user1.player_width, user1.player_height))
    

    
    # 把文字贴到屏幕上 (x, y 位置)    
    screen.blit(name_text, (50, 50))
    screen.blit(atk_text, (50, 100))
    screen.blit(hp_text, (50, 150))
    # 控制帧率
    clock.tick(60)
    # 更新显示内容
    pygame.display.flip()
    
    
# 退出 Pygame
pygame.quit()

def drawfont():
    pass
