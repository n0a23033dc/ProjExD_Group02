import pygame
import random
import time
import os

# 初期設定
pygame.init()

# 画面サイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("走れ！こうかとん！")

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
        # 画像を読み込み、サイズを調整
        self.image = pygame.transform.flip(pygame.transform.rotozoom(pygame.image.load("fig/5.png"), 0, 1), True, False)
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.default_jump_count = 2  # 通常ジャンプ回数
        self.jump_count = self.default_jump_count
        self.boost_end_time = 0  # ジャンプ増加の終了時間
        self.flight_end_time = 0  # 飛行モードの終了時間

    def update(self):
        # 飛行モード中
        keys = pygame.key.get_pressed()
        if time.time() < self.flight_end_time and keys[pygame.K_a]:
            self.velocity = 0  # 重力無効化
            self.rect.y = 40  # スコア表示の高さ付近（画面上部40pxに固定）
        else:
            # 通常状態
            self.velocity += self.gravity
            self.rect.y += self.velocity

        # 地面の衝突
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0
            self.jump_count = self.default_jump_count  # 着地時にジャンプ回数をリセット
            self.jump_count = 5  # 地面に着地したらジャンプ回数をリセット

        # 上の壁を越えない
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

        # ジャンプブーストの時間切れ判定
        if time.time() > self.boost_end_time:
            self.default_jump_count = 2  # ジャンプ回数を元に戻す

    def jump(self):
        if self.jump_count > 0:
            self.velocity = self.jump_strength
            self.jump_count -= 1

    def activate_boost(self, duration=10):
        self.default_jump_count = 6  # ジャンプ回数を6回に増加
        self.jump_count = 6  # 即時反映
        self.boost_end_time = time.time() + duration  # 終了時間を設定

    def activate_flight(self, duration=10):
        self.flight_end_time = time.time() + duration  # 飛行モードの終了時間

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
        if self.rect.right < 0:
            self.kill()

# アイテム1クラス
class Item1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("ex5/fig/item.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

# アイテム2クラス（飛行モード用）
class Item2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("ex5/fig/item2.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

# スプライトグループ
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

obstacle_group = pygame.sprite.Group()
item1_group = pygame.sprite.Group()
item2_group = pygame.sprite.Group()

# 日本語フォントの読み込み
font_path = "NotoSansJP-VariableFont_wght.ttf"

# スタート画面を表示する関数
def show_start_screen(screen):
    screen.fill(WHITE)
    if not os.path.exists(font_path):
        title_font = pygame.font.Font(None, 74)
        instruction_font = pygame.font.Font(None, 50)
    else:
        title_font = pygame.font.Font(font_path, 74)
        instruction_font = pygame.font.Font(font_path, 50)
    
    title_text = title_font.render("走れ！こうかとん", True, BLACK)
    instruction_text = instruction_font.render("エンターキーを押してね", True, BLACK)
    
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    
    screen.blit(title_text, title_rect)
    screen.blit(instruction_text, instruction_rect)

    crying_kk_img = pygame.transform.rotozoom(pygame.image.load("fig/5.png"), 0, 0.9)
    crying_kk_img_flipped = pygame.transform.flip(crying_kk_img, True, False)  # 左右反転

    left_crying_kk_rct = crying_kk_img_flipped.get_rect()
    right_crying_kk_rct = crying_kk_img.get_rect()
    left_crying_kk_rct.center = (title_rect.left - 50, title_rect.centery)
    right_crying_kk_rct.center = (title_rect.right + 50, title_rect.centery)
    screen.blit(crying_kk_img_flipped, left_crying_kk_rct)
    screen.blit(crying_kk_img, right_crying_kk_rct)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# メインゲームループの前にスタート画面を表示
show_start_screen(screen)

# ゲームループ
running = True
score = 0
spawn_timer = 0
last_item1_score = 0
last_item2_score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # 背景
    screen.fill(WHITE)

    # プレイヤー更新
    player_group.update()

    # 障害物生成
    spawn_timer += 1
    if spawn_timer > 90:
        height = random.randint(20, 100)
        obstacle = Obstacle(SCREEN_WIDTH, SCREEN_HEIGHT - height, 30, height)
        obstacle_group.add(obstacle)
        spawn_timer = 0

    # アイテム1生成（スコアが1000の時だけ）
    if score % 1500 == 0 and last_item1_score < score:
        item = Item1(SCREEN_WIDTH, 200)
        item1_group.add(item)
        last_item1_score = score

    # アイテム2生成（スコアが3000の時だけ）
    if score % 3500 == 0 and last_item2_score < score:
        item = Item2(SCREEN_WIDTH, 200)
        item2_group.add(item)
        last_item2_score = score

    # 障害物・アイテム更新
    obstacle_group.update()
    item1_group.update()
    item2_group.update()

    # 衝突判定
    if pygame.sprite.spritecollide(player, obstacle_group, False):
        print(f"ゲームオーバー! スコア: {score}")
        running = False

    # アイテム1取得判定
    if pygame.sprite.spritecollide(player, item1_group, True):
        player.activate_boost(10)
        print("アイテム1取得！10秒間6回ジャンプ可能！")

    # アイテム2取得判定
    if pygame.sprite.spritecollide(player, item2_group, True):
        player.activate_flight(10)
        print("アイテム2取得！10秒間飛行モード有効！")

    # スコア更新
    score += 1
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # 描画
    player_group.draw(screen)
    obstacle_group.draw(screen)
    item1_group.draw(screen)
    item2_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
