import os, pygame
from glogic import Player
import glogic
import window

# 初始化 Pygame
pygame.init()


WIDTH, HEIGHT = glogic.WIDTH, glogic.HEIGHT
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.SCALED | pygame.DOUBLEBUF,
    vsync =1
    )
pygame.display.set_caption("Ionic fluorescence")

base_path = os.path.dirname(os.path.abspath(__file__))  # 当前脚本所在目录
bg_img_path = os.path.join(base_path, "Materials", "map_background.png")



#地图纹理
texture_img = pygame.image.load(bg_img_path).convert()
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
playername = "Cosmos"
playeratk = 10
playerhp = 100
playerwidth = 150
playerheight = 150
user1 = Player.createplayer(playername, playeratk, playerhp, playerwidth, playerheight)
pl_img_path = os.path.join(base_path, "Materials", "player_transcript.png")
PlayerImg = pygame.image.load(pl_img_path).convert_alpha()
PlayerImg = pygame.transform.scale(PlayerImg, (user1.player_width, user1.player_height))
PlayerImgRight = pygame.transform.flip(PlayerImg, True, False)


# create barrier
BarLength = 80
bar_img_path = os.path.join(base_path, "Materials", "obstaclestone.png")
barimg = pygame.image.load(bar_img_path).convert_alpha()
barimg = pygame.transform.scale(barimg, (BarLength*2, BarLength*2))
bars = [glogic.barrier.create_barrier(BarLength, user1, barimg) for _ in range(5)]

# create enemy
EnemyHP = 100
EnemyATK = 5
EnemySpeed = 5
EnemyRadius = 100
EnemyAtkRadius = 150
en_img_path = os.path.join(base_path, "Materials", "diren1.png")
EnemyImg = pygame.image.load(en_img_path).convert_alpha()
EnemyImg = pygame.transform.scale(EnemyImg, (EnemyRadius*2, EnemyRadius*2))
Enemies = [glogic.Enemy.getEnemy(
    EnemyATK, EnemyHP, EnemySpeed, EnemyRadius, EnemyAtkRadius, EnemyImg
    ) for _ in range(3)]

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
totalObj = [gMap, user1, *bars, *Enemies]
movable_objects = [
    [user1, []],  
    *[(enemy, [user1]) for enemy in Enemies]
]
drawable_objects = [ #后画的会覆盖先画的，所以地图要最先画
    *[(gMap, [screen, textures, user1])],
    *[(bar, [screen, user1]) for bar in bars],
    *[(enemy, [screen, user1]) for enemy in Enemies],
    [user1, [screen, PlayerImg, PlayerImgRight]]
] 

# 创建游戏世界对象
GameWorld = glogic.GameWorld(
    totalObj, drawable_objects, 
    movable_objects, screen,
    user1
    )

window = window.interfaceManager(screen, base_path, GameWorld)

# 游戏主循环
running = True
while running:
    
    Events = pygame.event.get()
    #如果退出了就把游戏关了
    for event in Events:
        if event.type == pygame.QUIT:
            running = False

    # 填充背景颜色（RGB）
    screen.fill((0, 128, 255))

    # 渲染玩家名字
    name_text = font.render(f"{user1.name}", True, (255, 255, 255))
    atk_text = font.render(f"ATK: {user1.atk}", True, (255, 255, 255))
    hp_text = font.render(f"HP: {user1.hp}", True, (255, 255, 255))
    
    
    window.LoadEvents(Events)
    window.updateWindow()
    window.drawWindow()
    if running == True:
        running = window.quitHandle()
    
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

