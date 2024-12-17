import pygame as pg
import random

# 初期設定
pg.init()

# 画面サイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("チャリ走")

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# ゲーム速度
clock = pg.time.Clock()
FPS = 60

# プレイヤークラス
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50, 30))
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
class Obstacle(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pg.Surface((width, height))
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
player_group = pg.sprite.Group()
player_group.add(player)

obstacle_group = pg.sprite.Group()

#日本語フォントの読み込み
font_path = "NotoSansJP-VariableFont_wght.ttf"

# スタート画面を表示する関数
def show_start_screen(screen):
    screen.fill(WHITE)
    title_font = pg.font.Font(font_path, 74)
    instruction_font = pg.font.Font(font_path, 50)
    
    title_text = title_font.render("走れ！こうかとん", True, BLACK)
    instruction_text = instruction_font.render("エンターキーを押してね", True, BLACK)
    
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    
    screen.blit(title_text, title_rect)
    screen.blit(instruction_text, instruction_rect)

    crying_kk_img = pg.transform.rotozoom(pg.image.load("fig/5.png"), 0, 0.9)
    crying_kk_img_flipped = pg.transform.flip(crying_kk_img, True, False)  # 左右反転

    left_crying_kk_rct = crying_kk_img_flipped.get_rect()
    right_crying_kk_rct = crying_kk_img.get_rect()
    left_crying_kk_rct.center = (title_rect.left - 50, title_rect.centery)
    right_crying_kk_rct.center = (title_rect.right + 50, title_rect.centery)
    screen.blit(crying_kk_img_flipped, left_crying_kk_rct)
    screen.blit(crying_kk_img, right_crying_kk_rct)

    pg.display.flip()

    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    waiting = False

# メインゲームループの前にスタート画面を表示
show_start_screen(screen)

# ゲームループ
running = True
score = 0
spawn_timer = 0

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
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
    if pg.sprite.spritecollide(player, obstacle_group, False):
        print(f"ゲームオーバー! スコア: {score}")
        running = False

    # スコア更新
    score += 1
    font = pg.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # スプライト描画
    player_group.draw(screen)
    obstacle_group.draw(screen)

    # 画面更新
    pg.display.flip()
    clock.tick(FPS)

pg.quit()