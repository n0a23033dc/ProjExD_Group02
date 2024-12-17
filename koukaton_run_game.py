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

# ゲーム速度
clock = pygame.time.Clock()
FPS = 60

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

# スプライトグループ
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

obstacle_group = pygame.sprite.Group()

# ゲームループ
running = True
score = 0
spawn_timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # 背景を白で塗りつぶす
    screen.fill(WHITE)

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
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # スプライト描画
    player_group.draw(screen)
    obstacle_group.draw(screen)

    # 画面更新
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()