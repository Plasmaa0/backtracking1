"""
Game
Q - выход
R - сброс на исходные позиции
C - выбор, кто ходит первый (только если ни один ход не был сделан)
Numpad 7,4,1 - ход зеленой фишкой (верхней/средней/нижней)
Numpad 1,2,3 - ход красной фишкой (левой/средней/правой)
Параметр ARTI (в __main__) включает/выключает игру компьютера за красные фишки
Если игра компьютера включена, то после хода человека, чтобы увидеть ход компьютера, нажмите любую клавишу
По умолчанию начинет зелёный, если хотите чтобы компьютер сделал первый ход, нажмите C
Комментариев к коду нет, штука адская, сам разбираюсь.
"""

import pygame
import math
import random


class Board():
    """
    Board, Positions of players, Check if someone win, get available moves for both players
    """

    def __init__(self, playerpos: list, enemypos: list, turn: int):
        self.player = playerpos
        self.enemy = enemypos
        self.isplayerturn = turn

    def getplayerpos_x(self, indexofplayer: int):
        player_x = self.player[indexofplayer]
        return player_x

    def getplayerpos_y(self, indexofplayer: int):
        player_y = indexofplayer + 1
        return player_y

    def getenemypos_x(self, indexofenemy: int):
        enemy_x = indexofenemy + 1
        return enemy_x

    def getenemypos_y(self, indexofenemy: int):
        enemy_y = 4 - self.enemy[indexofenemy]
        return enemy_y

    def playermoves(self):
        mov = [1, 1, 1]
        for i in range(3):
            player_y = self.getplayerpos_y(i)
            player_x = self.getplayerpos_x(i)
            enemycords = []
            enemy_xs = []
            for j in range(3):
                enemy_y = self.getenemypos_y(j)
                enemy_x = self.getenemypos_x(j)
                enemycords.append((enemy_x, enemy_y))
                if(player_y == enemy_y):
                    enemy_xs.append(enemy_x)
            for en in enemycords:
                enemy_x = en[0]
                enemy_y = en[1]
                if(player_x + 1 == enemy_x and player_y == enemy_y):
                    if(player_x + 2 in enemy_xs):
                        mov[i] = 0
                        break
                    else:
                        mov[i] = 2
                        break
                if(player_x > 3):
                    mov[i] = 0
                    break
        return mov

    def enemymoves(self):
        mov = [1, 1, 1]
        for i in range(3):
            enemy_y = self.getenemypos_y(i)
            enemy_x = self.getenemypos_x(i)
            playercords = []
            player_ys = []
            for j in range(3):
                player_y = self.getplayerpos_y(j)
                player_x = self.getplayerpos_x(j)
                playercords.append((player_x, player_y))
                if(player_x == enemy_x):
                    player_ys.append(player_y)
            for pl in playercords:
                player_y = pl[1]
                player_x = pl[0]
                if(player_y == enemy_y - 1 and player_x == enemy_x):
                    if(enemy_y - 2 in player_ys):
                        mov[i] = 0
                        break
                    else:
                        mov[i] = 2
                        break
                if(enemy_y == 0):
                    mov[i] = 0
                    break
        return mov


class Game():
    def __init__(self, artion: bool, width: int, height: int, playerstartpos: list, enemystartpos: list, isplayerturn: int):
        self.arti = artion
        self.BACKGOUNDCOLOR = (18, 22, 22)
        self.board = Board(playerstartpos, enemystartpos, isplayerturn)
        self.sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.icon = pygame.Surface((10, 10))
        for i in range(10):
            for j in range(10):
                self.icon.set_at((i, j), (random.randint(
                    0, 255), random.randint(0, 255), random.randint(0, 255)))
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(
            "Game")
        playing = True
        while(playing):
            self.checkwin()
            playing = self.playturn()
            self.sc.fill(self.BACKGOUNDCOLOR)
            self.drawenv()
            pygame.display.update()

    def drawenv(self):
        for i in range(6):
            pygame.draw.line(self.sc, WHITE, [0, 100*i], [500, 100*i])
            pygame.draw.line(self.sc, WHITE, [100*i, 0], [100*i, 500])
        for i in range(3):
            pygame.draw.rect(
                self.sc, GREEN, (self.board.player[i]*100 + 45, 140 + 100*i, 30, 10))
            pygame.draw.rect(
                self.sc, RED, (140 + 100*i, 450 - self.board.enemy[i]*100, 10, 30))
        if(self.board.isplayerturn):
            turncolor = GREEN  # player
        else:
            turncolor = RED  # enemy
        pygame.draw.rect(self.sc, turncolor, (1, 401, 99, 99))
    # <!-- eslint-disable-next-line - ->  #убрать комментирование если бесит, что vscode выдает ошибки в обозначениях клавиш типа "pygame.K_ESCAPE", "pygame.K_c"

    def playturn(self):
        before = sum(self.board.player) + sum(self.board.enemy)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif(event.type == pygame.KEYDOWN):
                if(event.key in [pygame.K_q, pygame.K_ESCAPE]):
                    pygame.quit()
                elif(event.key == pygame.K_r):
                    self.reset(None)
                    return True
                elif(event.key == pygame.K_c and sum(self.board.player) + sum(self.board.enemy) == 0):
                    self.board.isplayerturn = not self.board.isplayerturn
                    return True
                elif(self.board.isplayerturn):
                    mov = self.board.playermoves()
                    if(sum(mov) == 0):
                        self.board.isplayerturn = False
                    elif event.key in [pygame.K_KP7, pygame.K_KP8, pygame.K_KP9, pygame.K_1]:
                        self.board.player[0] += (1 * mov[0])
                    elif event.key in [pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_2]:
                        self.board.player[1] += (1 * mov[1])
                    elif event.key in [pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_3]:
                        self.board.player[2] += (1 * mov[2])
                elif(not self.arti):
                    mov = self.board.enemymoves()
                    if(sum(mov) == 0):
                        self.board.isplayerturn = True
                    if event.key in [pygame.K_KP1, pygame.K_KP4, pygame.K_KP7, pygame.K_1]:
                        self.board.enemy[0] += (1 * mov[0])
                    elif event.key in [pygame.K_KP2, pygame.K_KP5, pygame.K_KP8, pygame.K_2]:
                        self.board.enemy[1] += (1 * mov[1])
                    elif event.key in [pygame.K_KP3, pygame.K_KP6, pygame.K_KP9, pygame.K_3]:
                        self.board.enemy[2] += (1 * mov[2])
                else:
                    mov = self.board.enemymoves()
                    if(sum(mov) == 0):
                        self.board.isplayerturn = True
                    else:
                        ind = self.ai()
                        if(ind != -1):
                            self.board.enemy[ind] += (1 * mov[ind])
                        else:
                            for i in range(len(mov)):
                                # костыль тк если комп-у остался один ход до победы то в рекурсии он упрется в то, что у него нет ходов
                                if(mov[i] != 0):
                                    self.board.enemy[i] += (1 * mov[i])
        if(sum(self.board.player) + sum(self.board.enemy) != before):
            self.board.isplayerturn = not self.board.isplayerturn
        return True

    def reset(self, playerwins):
        if(playerwins != None):
            if(playerwins):
                self.sc.fill(GREEN)
            else:
                self.sc.fill(RED)
            pygame.time.delay(1000)
            pygame.display.update()
            pygame.time.delay(1000)
        self.board.isplayerturn = True
        self.board.player = [0, 0, 0]
        self.board.enemy = [0, 0, 0]

    def checkwin(self):
        if(sum(self.board.player) == 12):
            self.reset(True)
        elif(sum(self.board.enemy) == 12):
            self.reset(False)

    def ai(self) -> int:  # https://youtu.be/trKjYdBASyQ
        scores = [10, -10, 0]

        def minimax(board: Board, depth, ismaximizing):
            def win(board: Board):
                if sum(board.player) == 12:
                    return 1
                elif sum(board.enemy) == 12:
                    return 0
                else:
                    return 2

            result = win(board)
            if(result != 0):
                return scores[result]
            if(ismaximizing):
                bestscore = -math.inf
                moves = board.enemymoves()
                for i in range(3):
                    if(moves[i] != 0):
                        board.enemy[i] += (1 * moves[i])
                        score = minimax(board, depth + 1, False)/depth
                        board.enemy[i] -= (1 * moves[i])
                        bestscore = max(score, bestscore)
                return bestscore
            else:
                bestscore = -math.inf
                moves = board.playermoves()
                for i in range(3):
                    if(moves[i] != 0):
                        board.enemy[i] += (1 * moves[i])
                        score = minimax(board, depth + 1, True)/depth
                        board.enemy[i] -= (1 * moves[i])
                        bestscore = min(score, bestscore)
                return bestscore

        bestscore = -math.inf
        moves = self.board.enemymoves()
        move = -1
        for i in range(3):
            if(moves[i] != 0):
                self.board.enemy[i] += (1 * moves[i])
                score = minimax(self.board, 1, False)
                self.board.enemy[i] -= (1 * moves[i])
                if(score > bestscore):
                    bestscore = score
                    move = i
        return move


if __name__ == "__main__":
    ARTI = True  # int(input()) == 1
    WIN_WIDTH = 501
    WIN_HEIGHT = 501
    WHITE = (68, 43, 72)
    GREEN = (101, 240, 42)  # (95, 232, 177)
    RED = (184, 24, 0)  # (214, 74, 49)

    startplayer = [0, 0, 0]
    startenemy = [0, 0, 0]
    isplayerturn = True
    Game(ARTI, WIN_WIDTH, WIN_HEIGHT,
         startplayer, startenemy, isplayerturn)
