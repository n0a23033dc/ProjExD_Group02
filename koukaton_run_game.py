import pygame
import random

#初期設定
pygame.init()

#画面サイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("チャリ走")

#色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

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

        #地面の衝突
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT #地面の位置に固定
            self.velocity = 0 #縦方向の速度をリセット
            self.jump_count = 2 #地面に着地したらジャンプ回数をリセット

        #上の壁を越えない
        if self.rect.top < 0:
            self.rect.top = 0 #上に固定
            self.velocity = 0 #縦方向の速度をリセット

    def jump(self):
        if self.jump_count > 0:  #ジャンプ可能な回数が残っている場合
            self.velocity = self.jump_strength #ジャンプの強さを適用
            self.jump_count -= 1 #ジャンプ回数を１回減少

#障害物クラス
class Obstacle(pygame.sprite.Sprite): #pygameのSpriteクラスを継承
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

# スプライトグループ
player = Player() #プレイヤーインスタンス生成
player_group = pygame.sprite.Group() #プレイヤー用グループを作成
player_group.add(player) #グループにプレイヤーを追加

obstacle_group = pygame.sprite.Group() #障害物用グループを作成

# ゲームループ
running = True #ゲームを実行中
score = 0 #スコアの初期化
spawn_timer = 0 #障害物生成のためのタイマー

while running:
    for event in pygame.event.get(): #イベント取得
        if event.type == pygame.QUIT: #ウィンドウが閉じられた場合
            running = False 
        if event.type == pygame.KEYDOWN: #キーが押された場合
            if event.key == pygame.K_SPACE: #スペースキーでジャンプ
                player.jump()

    # 背景を白で塗りつぶす
    screen.fill(WHITE)

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
    obstacle_group.update()

    # 衝突判定
    if pygame.sprite.spritecollide(player, obstacle_group, False, pygame.sprite.collide_mask):
        print(f"ゲームオーバー! スコア: {score}") #スコア表示
        running = False #ループ終了

    # スコア更新
    score += 1
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10)) #スコア表示

    # スプライト描画
    player_group.draw(screen) #プレイヤーを描画
    obstacle_group.draw(screen) #障害物を描画

    # 画面更新
    pygame.display.flip() #画面を更新
    clock.tick(FPS) #ゲーム速度をFPSに合わせる

pygame.quit()