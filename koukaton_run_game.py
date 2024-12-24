import pygame
import random
import time
import os

#初期設定
pygame.init()

#画面サイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("走れ！こうかとん！")

#色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
DARK_RED = (139, 0, 0)
BROWN = (165, 42, 42)
PURPLE = (128, 0, 128)

#ゲーム速度
clock = pygame.time.Clock()
FPS = 60
#ビル画像の読み込み
building_image = pygame.image.load("ex5/fig/3254オフィスビル.png").convert_alpha() #画像を読み込む
building_image = pygame.transform.scale(building_image, (500, 1000))  #サイズを調整

#プレイヤークラス
class Player(pygame.sprite.Sprite): #pygameのSpriteクラスを継承
    def __init__(self):
        super().__init__() #親クラスの初期化
        self.image = pygame.Surface((50, 30)) #プレイヤーのサイズ
        self.image.fill(BLUE) #プレイヤーの色
        self.rect = self.image.get_rect() #位置とサイズ情報
        self.rect.center = (100, SCREEN_HEIGHT // 2) #初期位置を画面左中央に設定
        self.velocity = 0 #縦方向の速度
        self.gravity = 0.5 #重力
        self.jump_strength = -10 #ジャンプの強さ
        self.jump_count = 2  #2段ジャンプを許可

    def update(self):
        self.velocity += self.gravity #重力で速度を増加
        self.rect.y += self.velocity #速度分だけY座標を更新
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

# プレイヤークラス1
class Player1(pygame.sprite.Sprite):
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

        #地面の衝突
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0
            self.jump_count = self.default_jump_count  # 着地時にジャンプ回数をリセット
            self.jump_count = 5  # 地面に着地したらジャンプ回数をリセット

        #上の壁を越えない
        if self.rect.top < 0:
            self.rect.top = 0 #上に固定
            self.velocity = 0 #縦方向の速度をリセット

        # ジャンプブーストの時間切れ判定
        if time.time() > self.boost_end_time:
            self.default_jump_count = 2  # ジャンプ回数を元に戻す

    def jump(self):
        if self.jump_count > 0:  #ジャンプ可能な回数が残っている場合
            self.velocity = self.jump_strength #ジャンプの強さを適用
            self.jump_count -= 1 #ジャンプ回数を１回減少

#障害物クラス
class Obstacle(pygame.sprite.Sprite): #pygameのSpriteクラスを継承
        if self.jump_count > 0:
            self.velocity = self.jump_strength
            self.jump_count -= 1

# 障害物クラス
class Obstacle(pygame.sprite.Sprite):
    def activate_boost(self, duration=10):
        self.default_jump_count = 6  # ジャンプ回数を6回に増加
        self.jump_count = 6  # 即時反映
        self.boost_end_time = time.time() + duration  # 終了時間を設定

    def activate_flight(self, duration=10):
        self.flight_end_time = time.time() + duration  # 飛行モードの終了時間

# 障害物クラス1
class Obstacle1(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__() #親クラスの初期化
        self.image = pygame.transform.scale(building_image, (width, height)) #ビル画像のサイズ調整
        self.rect = self.image.get_rect() #画像の位置情報を取得
        self.rect.x = x #障害物のX座標を設定
        self.rect.y = y #障害物のY座標を設定
        self.speed = 5 #障害物の移動速度

    def update(self):
        self.rect.x -= self.speed #左方向に移動
        if self.rect.right < 0:  # 画面外に出たら削除
            self.kill() #障害物を削除


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

# ゲームオーバー画面表示関数
def gameover(screen, score):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(150)  # 半透明度を設定
    screen.blit(overlay, (0, 0))

    # フォントとテキスト設定
    font = pygame.font.Font(None, 80)
    text1 = font.render("Game Over", True, (255, 255, 255))
    text2 = font.render(f"Score: {score}", True, (255, 255, 255))

    # テキストの配置
    text_rect1 = text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    text_rect2 = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))

    # 画面にテキストを描画
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)

    pygame.display.update()
    pygame.time.wait(5000)  # 5秒間待機

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
player = Player() #プレイヤーインスタンス生成
player_group = pygame.sprite.Group() #プレイヤー用グループを作成
player_group.add(player) #グループにプレイヤーを追加

obstacle_group = pygame.sprite.Group() #障害物用グループを作成

# ゲームループ
running = True #ゲームを実行中
score = 0 #スコアの初期化
spawn_timer = 0 #障害物生成のためのタイマー

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
score_timer = 0
last_item1_score = 0
last_item2_score = 0
createStars()

while running:
    for event in pygame.event.get(): #イベント取得
        if event.type == pygame.QUIT: #ウィンドウが閉じられた場合
            running = False 
        if event.type == pygame.KEYDOWN: #キーが押された場合
            if event.key == pygame.K_SPACE: #スペースキーでジャンプ
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

    # プレイヤーが障害物の上に乗れるようにする
    for obstacle in obstacle_group:
        if player.rect.colliderect(obstacle.rect): #衝突判定
            if player.rect.bottom <= obstacle.rect.top + 10:  #上側からの接触
                player.rect.bottom = obstacle.rect.top #プレイヤーを障害物の上に固定
                player.velocity = 0 #縦方向の速度をリセット
                player.jump_count = 2  # 障害物の上でジャンプ回数をリセット

    # 障害物生成
    spawn_timer += 1
    if spawn_timer > random.randint(20, 60):  # 一定時間ごとに障害物を生成
        height = random.randint(50, 170) #障害物の高さをランダムに設定
        obstacle = Obstacle(SCREEN_WIDTH, SCREEN_HEIGHT - height, 100, height)
        obstacle_group.add(obstacle) #障害物をグループに追加
        spawn_timer = 0 #タイマーをリセット
   
    # 障害物更新
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
        gameover(screen, score)
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
    score_timer += 1
    if score_timer >= 10:  # 10フレームごとにスコアを更新
        score += 1
        score_timer = 0
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10)) #スコア表示

    # スプライト描画
    player_group.draw(screen) #プレイヤーを描画
    obstacle_group.draw(screen) #障害物を描画
    item1_group.draw(screen)
    item2_group.draw(screen)

    # 画面更新
    pygame.display.flip() #画面を更新
    clock.tick(FPS) #ゲーム速度をFPSに合わせる


pygame.quit()
