import pyxel
import math
import pygame
import os

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 120
BASE_RADIUS = 6.5
HIGHSCORE_FILE = "highscore.txt"


class Fruit:
    def __init__(self):
        # evolution[0][0]は画像のx座標、evolution[0][1]は画像のy座標、evolution[0][2]はfruitのscaleの値、evolution[0][3]はスコア
        self.evolution = [
            [0, 0, 1, 10],
            [16, 0, 1.2, 10],
            [32, 0, 1.5, 10],
            [0, 16, 2, 50],
            [16, 16, 2.5, 50],
            [0, 32, 3, 100],
            [16, 32, 3, 100],
            [0, 48, 3.2, 200],
            [16, 48, 3.4, 200],
            [0, 64, 4, 500],
        ]
        # 0 = 50% 1 = 25% 2 = 12.5% 3 = 6.25% 4 = 3.125%
        self.number = pyxel.rndi(0, 100)
        if self.number < 50:
            self.number = 0
        elif self.number < 75:
            self.number = 1
        elif self.number < 87.5:
            self.number = 2
        elif self.number < 93.75:
            self.number = 3
        else:
            self.number = 4
        self.x = 50
        self.y = 6
        self.vy = 0
        self.r = BASE_RADIUS * self.evolution[self.number][2]
        self.fall = False
        self.gravity = 1.2

    def update(self):
        if self.fall:
            self.vy *= self.gravity
            self.y += self.vy
            if self.y > SCREEN_HEIGHT - (
                BASE_RADIUS * (self.evolution[self.number][2] + 1)
            ):
                self.y = SCREEN_HEIGHT - BASE_RADIUS * (
                    self.evolution[self.number][2] + 1
                )

        else:
            if pyxel.btn(pyxel.KEY_LEFT):
                self.x -= pyxel.rndi(1, 3)
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.x += pyxel.rndi(1, 3)
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.vy += 0.1
                self.fall = True

            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                if self.x < pyxel.mouse_x:
                    self.x += pyxel.rndi(1, 3)
                elif self.x > pyxel.mouse_x:
                    self.x -= pyxel.rndi(1, 3)

        if self.x < BASE_RADIUS * (self.evolution[self.number][2] - 1):
            self.x = BASE_RADIUS * (self.evolution[self.number][2] - 1)
        if self.x + BASE_RADIUS * (self.evolution[self.number][2] + 1) > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - BASE_RADIUS * (self.evolution[self.number][2] + 1)

    def draw(self):
        pyxel.blt(
            self.x,
            self.y,
            0,
            self.evolution[self.number][0],
            self.evolution[self.number][1],
            BASE_RADIUS * 2,
            BASE_RADIUS * 2,
            0,
            0,
            self.evolution[self.number][2],
        )


class Sound:
    def __init__(self):
        # 魔王魂様からお借りしました
        self.sound_1 = pygame.mixer.Sound("sounds/maou_bgm_piano40.mp3")
        self.sound_1.set_volume(0.8)

        self.sound_2 = pygame.mixer.Sound("sounds/慶應義塾塾歌.mp3")
        self.sound_3 = pygame.mixer.Sound("sounds/若き血.mp3")

        # OtoLogic様からお借りしました
        self.union = pygame.mixer.Sound("sounds/union.mp3")

        # ポケットサウンド様からお借りしました
        self.gameover = pygame.mixer.Sound("sounds/gameover.mp3")
        self.gameover.set_volume(0.8)

    def play_1(self):
        self.sound_1.play(loops=-1)

    def play_2(self):
        self.sound_2.play(loops=-1)

    def play_3(self):
        self.sound_3.play(loops=-1)

    def play_union(self):
        self.union.play()

    def play_gameover(self):
        self.gameover.play()

    def stop_bgm(self):
        pygame.mixer.stop()


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="SFC Suica")
        pyxel.load("suica.pyxres")
        pyxel.mouse(True)
        pygame.mixer.init()
        self.highscore = self.load_highscore()
        self.reset_game()
        self.next_fruit = pyxel.rndi(0, 100)
        if self.next_fruit < 50:
            self.next_fruit = 0
        elif self.next_fruit < 75:
            self.next_fruit = 1
        elif self.next_fruit < 87.5:
            self.next_fruit = 2
        elif self.next_fruit < 93.75:
            self.next_fruit = 3
        else:
            self.next_fruit = 4
        pyxel.run(self.update, self.draw)

    def load_highscore(self):
        if not os.path.exists(HIGHSCORE_FILE):
            return 0
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())

    def save_highscore(self):
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(self.highscore))

    def reset_game(self):
        self.score = 0
        self.game_over = False
        self.fruits = [Fruit()]
        self.sound = Sound()
        self.flag = 0
        self.sound.stop_bgm()
        self.sound.play_1()

    def create_fruit(self):
        fruit = Fruit()
        fruit.number = self.next_fruit
        fruit.r = BASE_RADIUS * fruit.evolution[fruit.number][2]
        self.next_fruit = pyxel.rndi(0, 100)
        if self.next_fruit < 50:
            self.next_fruit = 0
        elif self.next_fruit < 75:
            self.next_fruit = 1
        elif self.next_fruit < 87.5:
            self.next_fruit = 2
        elif self.next_fruit < 93.75:
            self.next_fruit = 3
        else:
            self.next_fruit = 4
        return fruit

    def update(self):
        """デバッグ用
        if pyxel.btnp(pyxel.KEY_E):
            self.next_fruit = 9
        """

        if self.game_over:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game()
            return

        if not any(not fruit.fall for fruit in self.fruits):
            self.fruits.append(self.create_fruit())

        for fruit in self.fruits:
            fruit.update()
            if fruit.y < 0:
                self.game_over = True
                self.sound.stop_bgm()
                self.sound.play_gameover()

                if self.score > self.highscore:
                    self.highscore = self.score
                    self.save_highscore()

            if fruit.number >= 7 and self.flag == 0:
                self.flag = 1
            if fruit.number == 9 and self.flag == 2:
                self.flag = 3

        if self.flag == 1:
            self.sound.stop_bgm()
            self.sound.play_2()
            self.flag = 2
        elif self.flag == 3:
            self.sound.stop_bgm()
            self.sound.play_3()
            self.flag = 4

        # フルーツ同士の反発・進化処理
        i = 0
        while i < len(self.fruits):
            f1 = self.fruits[i]
            j = i + 1
            while j < len(self.fruits):
                f2 = self.fruits[j]
                dx = f1.x - f2.x
                dy = f1.y - f2.y
                dist = math.sqrt(dx**2 + dy**2)
                if dist < f1.r + f2.r and f1.fall == True and f2.fall == True:
                    # 反発処理
                    if f1.number == f2.number and f1.number < len(f1.evolution) - 1:
                        # フルーツを進化させ、一つに合体
                        f1.number += 1
                        f1.r = BASE_RADIUS * f1.evolution[f1.number][2]
                        f1.x = (f1.x + f2.x) / 2
                        self.score += f1.evolution[f1.number][3]
                        self.sound.play_union()

                        del self.fruits[j]
                        continue

                    elif f1.number == f2.number and f1.number == len(f1.evolution) - 1:
                        # 最終進化段階の場合、両方のフルーツを削除
                        del self.fruits[j]
                        del self.fruits[i]
                        self.score += f1.evolution[f1.number][3]
                        i -= 1
                        break
                    else:
                        overlap = (f1.r + f2.r) - dist
                        if dist != 0:
                            nx = dx / dist
                            ny = dy / dist
                            f1.x += nx * overlap / 2
                            f1.y += ny * overlap / 2
                            f2.x -= nx * overlap / 2
                            f2.y -= ny * overlap / 2
                            f1.vy *= 0.9
                            f2.vy *= 0.9

                j += 1
            i += 1

    def draw(self):
        pyxel.cls(0)
        if self.game_over:
            pyxel.text(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 30, "GAME OVER", 8)
            pyxel.text(
                SCREEN_WIDTH // 2 - 30,
                SCREEN_HEIGHT // 2 - 10,
                f"HIGHSCORE: {self.highscore}",
                6,
            )
            pyxel.text(
                SCREEN_WIDTH // 2 - 20,
                SCREEN_HEIGHT // 2,
                f"SCORE: {self.score}",
                7,
            )
            pyxel.text(
                SCREEN_WIDTH // 2 - 42,
                SCREEN_HEIGHT // 2 + 20,
                "PRESS SPACE TO RESTART",
                7,
            )

        else:

            for fruit in self.fruits:
                fruit.draw()

            pyxel.text(0, 2, f"SCORE: {self.score}", 7)
            pyxel.text(SCREEN_WIDTH - 17, 2, "NEXT:", 7)
            pyxel.rect(SCREEN_WIDTH - 17, 8, 15, 15, 1)
            pyxel.blt(
                SCREEN_WIDTH - 16,
                9,
                0,
                Fruit().evolution[self.next_fruit][0],
                Fruit().evolution[self.next_fruit][1],
                BASE_RADIUS * 2,
                BASE_RADIUS * 2,
                0,
                0,
            )


App()
