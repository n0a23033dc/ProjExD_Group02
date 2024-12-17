import pygame
import random

# 初期設定
pygame.init()

# 画面サイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("チャリ走")

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
DARK_RED = (139, 0, 0)
BROWN = (165, 42, 42)
PURPLE = (128, 0, 128)

# ゲーム速度
clock = pygame.time.Clock()
FPS = 60

# 星と惑星のリスト
stars = []
planets = []

# 惑星のサイズ定義
planet_sizes = {
    'sun': 50,
    'saturn': 40,
    'earth': 30,
    'comet': 20,
    'venus': 25,
    'jupiter': 45,
    'uranus': 35,
    'neptune': 35
}

# プレイヤークラス
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.jump_count = 2  # 2段ジャンプを許可

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

        # 地面の衝突
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0
            self.jump_count = 2  # 地面に着地したらジャンプ回数をリセット

        # 上の壁を越えない
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

    def jump(self):
        if self.jump_count > 0:  # ジャンプ可能な回数が残っている場合
            self.velocity = self.jump_strength
            self.jump_count -= 1

# 障害物クラス
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:  # 画面外に出たら削除
            self.kill()

def createStars():
    global stars, planets
    for _ in range(100):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        stars.append({'x': x, 'y': y})

    # 惑星を追加
    planet_types = list(planet_sizes.keys())
    while planet_types:
        planet_type = planet_types.pop()
        size = planet_sizes[planet_type]
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        planets.append({'x': x, 'y': y, 'size': size, 'type': planet_type})

def showStars():
    global stars
    speed = 1.5
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star['x'], star['y']), 2)
        star['x'] -= speed
        if star['x'] < 0:
            star['x'] = SCREEN_WIDTH

def showPlanets():
    global planets
    speed = 1
    for planet in planets:
        if planet['type'] == 'sun':
            pygame.draw.circle(screen, YELLOW, (planet['x'], planet['y']), planet['size'])
        elif planet['type'] == 'saturn':
            pygame.draw.circle(screen, ORANGE, (planet['x'], planet['y']), planet['size'])
            pygame.draw.ellipse(screen, YELLOW, (planet['x'] - planet['size'], planet['y'] - planet['size'] // 4, planet['size'] * 2, planet['size'] // 2), 2)
        elif planet['type'] == 'earth':
            pygame.draw.circle(screen, BLUE, (planet['x'], planet['y']), planet['size'])
            pygame.draw.circle(screen, GREEN, (planet['x'], planet['y']), planet['size'] - 5)
        elif planet['type'] == 'comet':
            pygame.draw.circle(screen, WHITE, (planet['x'], planet['y']), planet['size'])
            pygame.draw.line(screen, WHITE, (planet['x'], planet['y']), (planet['x'] - planet['size'] * 2, planet['y']), 2)
        elif planet['type'] == 'venus':
            pygame.draw.circle(screen, ORANGE, (planet['x'], planet['y']), planet['size'])
        elif planet['type'] == 'jupiter':
            pygame.draw.circle(screen, BROWN, (planet['x'], planet['y']), planet['size'])
        elif planet['type'] == 'uranus':
            pygame.draw.circle(screen, LIGHT_BLUE, (planet['x'], planet['y']), planet['size'])
        elif planet['type'] == 'neptune':
            pygame.draw.circle(screen, PURPLE, (planet['x'], planet['y']), planet['size'])
        planet['x'] -= speed
        if planet['x'] < 0:
            planet['x'] = SCREEN_WIDTH
            planet['y'] = random.randint(0, SCREEN_HEIGHT)  # 高さをランダムに変更

def showGround():
    screen.fill(LIGHT_BLUE)  # 空を水色に塗りつぶす
    pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
    sun_size = 50  # 太陽のサイズを固定
    pygame.draw.circle(screen, YELLOW, (SCREEN_WIDTH - 50, 50), int(sun_size))  # 右上に太陽を描画

def showAtmosphere():
    # グラデーションを描画
    for y in range(SCREEN_HEIGHT):
        color = (
            DARK_BLUE[0] + (LIGHT_BLUE[0] - DARK_BLUE[0]) * y // SCREEN_HEIGHT,
            DARK_BLUE[1] + (LIGHT_BLUE[1] - DARK_BLUE[1]) * y // SCREEN_HEIGHT,
            DARK_BLUE[2] + (LIGHT_BLUE[2] - DARK_BLUE[2]) * y // SCREEN_HEIGHT
        )
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))
    pygame.draw.circle(screen, YELLOW, (SCREEN_WIDTH - 50, 50), 50)  # 右上に太陽を描画

# スプライトグループ
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

obstacle_group = pygame.sprite.Group()

# ゲームループ
running = True
score = 0
spawn_timer = 0

createStars()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # スコアに応じて背景を切り替える
    if score < 1000:
        # 地上を表示
        showGround()
        player.gravity = 0.5
    elif score < 2000:
        # 大気圏を表示
        showAtmosphere()
        player.gravity = 0.4
    elif score < 3000:
        # 星のみを表示
        screen.fill(BLACK)
        showStars()
        player.gravity = 0.3
    elif 3000<=score:   
        # 星と惑星を表示
        screen.fill(BLACK)
        showStars()
        showPlanets()
        player.gravity = 0.3

    # プレイヤー更新
    player_group.update()

    # 障害物生成
    spawn_timer += 1
    if spawn_timer > 90:  # 一定時間ごとに障害物を生成
        height = random.randint(20, 100)
        obstacle = Obstacle(SCREEN_WIDTH, SCREEN_HEIGHT - height, 30, height)
        obstacle_group.add(obstacle)
        spawn_timer = 0

    # 障害物更新
    obstacle_group.update()

    # 衝突判定
    if pygame.sprite.spritecollide(player, obstacle_group, False):
        print(f"ゲームオーバー! スコア: {score}")
        running = False

    # スコア更新
    score += 1
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # スプライト描画
    player_group.draw(screen)
    obstacle_group.draw(screen)

    # 画面更新
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()