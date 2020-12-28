# -*- coding: cp1251 -*-
import math
import pygame
import threading
import queue
"""
Комментариев к коду нет, штука адская, сам разбираюсь.
Параметр ARTI(в __main__) включает/выключает игру компьютера за красные фишки

upd: кажется minimax начал что-то считать, в нижнем правом квадрате выводится прогноз алгоритма:
    зеленый - выигрыш
    желтый - пока неизвестно(возможно только на первых ходах, тк глубина рекурсивного просчета ограничена)
    красный - проигрыш
!! если вылетает, попробуйте уменьшить число с которым сравнивается depth - это глубина просчёта ходов(искать "@DEPTH")

в планах разобраться с альфа-бета отсечением
"""


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
    def __init__(self, artion: bool, arti2on: bool, width: int, height: int, playerstartpos: list, enemystartpos: list, isplayerturn: int):
        self.number = 0
        self.arti = artion
        self.arti2 = arti2on
        self.BACKGOUNDCOLOR = (18, 22, 22)
        self.board = Board(playerstartpos, enemystartpos, isplayerturn)
        self.sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.articolor = self.BACKGOUNDCOLOR
        self.arti2color = self.BACKGOUNDCOLOR
        pygame.display.set_caption("Game")
        while(True):
            self.checkwin()
            self.playturn()
            self.sc.fill(self.BACKGOUNDCOLOR)
            self.drawenv()
            pygame.display.update()
            pygame.time.delay(100)

    def drawenv(self):
        for i in range(6):
            pygame.draw.line(self.sc, WHITE, [0, 100*i], [500, 100*i])
            pygame.draw.line(self.sc, WHITE, [100*i, 0], [100*i, 500])
        for i in range(3):
            pygame.draw.rect(
                self.sc, GREEN, (self.board.player[i]*100 + 45, 140 + 100*i, 30, 10))
            pygame.draw.rect(
                self.sc, RED, (140 + 100*i, 440 - self.board.enemy[i]*100, 10, 30))
            if(self.arti):
                if(self.board.enemy[i] == 4):
                    color = self.BACKGOUNDCOLOR
                else:
                    color = self.articolor
                pygame.draw.rect(
                    self.sc, color, (401, 401, 99, 99))
            if(self.arti2):
                if(self.board.player[i] == 4):
                    color = self.BACKGOUNDCOLOR
                else:
                    color = self.arti2color
                pygame.draw.rect(
                    self.sc, color, (1, 1, 99, 99))
        if(self.board.isplayerturn):
            turncolor = GREEN  # player
        else:
            turncolor = RED  # enemy
        pygame.draw.rect(self.sc, turncolor, (1, 401, 99, 99))

    def playturn(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_q):
                    pygame.quit()
                    print("Closing. Press any key.")
                    input()
                    exit(0)
                if(event.key == pygame.K_r):
                    self.reset(None)
                if(event.key == pygame.K_c and sum(self.board.player) + sum(self.board.enemy) == 0):
                    self.board.isplayerturn = not self.board.isplayerturn
                before = sum(self.board.player) + sum(self.board.enemy)
                if(self.board.isplayerturn):
                    mov = self.board.playermoves()
                    if(sum(mov) == 0):
                        self.board.isplayerturn = False
                        self.number += 1
                    if(self.arti2):
                        ind = self.ai(True)
                        if(ind != -1):
                            self.board.player[ind] += (1 * mov[ind])
                        else:
                            for i in range(len(mov)):
                                # костыль тк если комп-у остался один ход до победы то в рекурсии он упрется в то, что у него нет ходов
                                if(mov[i] != 0):
                                    self.board.player[i] += (1 * mov[i])
                    else:
                        if event.key in [pygame.K_KP7, pygame.K_KP8, pygame.K_KP9, pygame.K_1]:
                            self.board.player[0] += (1 * mov[0])
                        elif event.key in [pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_2]:
                            self.board.player[1] += (1 * mov[1])
                        elif event.key in [pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_3]:
                            self.board.player[2] += (1 * mov[2])
                else:
                    mov = self.board.enemymoves()
                    if(sum(mov) == 0):
                        self.board.isplayerturn = True
                        self.number += 1
                    if(self.arti):
                        ind = self.ai()
                        if(ind != -1):
                            self.board.enemy[ind] += (1 * mov[ind])
                        else:
                            for i in range(len(mov)):
                                # костыль тк если комп-у остался один ход до победы то в рекурсии он упрется в то, что у него нет ходов
                                if(mov[i] != 0):
                                    self.board.enemy[i] += (1 * mov[i])
                    else:
                        if event.key in [pygame.K_KP1, pygame.K_KP4, pygame.K_KP7, pygame.K_1]:
                            self.board.enemy[0] += (1 * mov[0])
                        elif event.key in [pygame.K_KP2, pygame.K_KP5, pygame.K_KP8, pygame.K_2]:
                            self.board.enemy[1] += (1 * mov[1])
                        elif event.key in [pygame.K_KP3, pygame.K_KP6, pygame.K_KP9, pygame.K_3]:
                            self.board.enemy[2] += (1 * mov[2])
                if(sum(self.board.player) + sum(self.board.enemy) != before):
                    self.number += 1
                    self.board.isplayerturn = not self.board.isplayerturn

    def reset(self, playerwins):
        if(playerwins != None):
            if(playerwins):
                self.sc.fill(GREEN)
                print("Green won")
            else:
                self.sc.fill(RED)
                print("Red won")
            pygame.time.delay(1000)
            pygame.display.update()
            pygame.time.delay(1000)
        self.number = 0
        self.articolor = self.BACKGOUNDCOLOR
        self.arti2olor = self.BACKGOUNDCOLOR
        self.board.player = [0, 0, 0]
        self.board.enemy = [0, 0, 0]

    def checkwin(self):
        if(sum(self.board.player) == 12):
            self.reset(True)
        elif(sum(self.board.enemy) == 12):
            self.reset(False)

    def win(self, board: Board):
        if(not self.board.isplayerturn):
            if sum(board.player) == 12:
                return False
            elif sum(board.enemy) == 12:
                return True
            else:
                return None
        else:
            if sum(board.player) == 12:
                return True
            elif sum(board.enemy) == 12:
                return False
            else:
                return None
    # @njit(fastmath=True)

    def minimax(self, brd: Board, depth, ismaximizing, alpha, beta):
        result = self.win(brd)
        # if(depth > 11):  # @DEPTH
        #     return 0
        if(result != None):
            if(result):
                return 1
            else:
                return -1
        if(ismaximizing):
            bestscore = -math.inf
            moves = brd.enemymoves()
            for i in range(3):
                if(moves[i] != 0):
                    brd.enemy[i] += (1 * moves[i])
                    score = self.minimax(brd, depth + 1, False, alpha, beta)
                    brd.enemy[i] -= (1 * moves[i])
                    bestscore = max(score, bestscore)
                    alpha = max(alpha, bestscore)
                    if(beta <= alpha):
                        break
            return bestscore
        else:
            bestscore = math.inf
            moves = brd.playermoves()
            for i in range(3):
                if(moves[i] != 0):
                    brd.player[i] += (1 * moves[i])
                    score = self.minimax(brd, depth + 1, True, alpha, beta)
                    brd.player[i] -= (1 * moves[i])
                    bestscore = min(score, bestscore)
                    beta = min(beta, bestscore)
                    if(beta <= alpha):
                        break
            return bestscore

    def scoretocolor(self, score, isenemy: bool):
        if(isenemy):
            if(score == 1):
                return (0, 100, 0)
            elif(score == 0 and self.articolor != (0, 100, 0)):
                return (200, 200, 0)
            elif (score == -1 and self.articolor != (0, 100, 0) or self.articolor != (200, 200, 0)):
                return (100, 0, 0)
            else:
                return (100, 0, 0)
        else:
            if(score == 1):
                return (0, 100, 0)
            elif(score == 0 and self.arti2color != (0, 100, 0)):
                return (200, 200, 0)
            elif (score == -1 and self.arti2color != (0, 100, 0) or self.arti2color != (200, 200, 0)):
                return (100, 0, 0)
            else:
                return (100, 0, 0)

    def ai(self, pl=False) -> int:  # https://youtu.be/trKjYdBASyQ
        que = queue.Queue()
        threads = []
        if(pl):
            bestscore = -math.inf
            moves = self.board.playermoves()
            move = int()
            print("Green:")
            for i in range(3):
                if(moves[i] != 0):
                    self.board.player[i] += (1 * moves[i])
                    # score = self.minimax(
                    #     self.board, 0, False, -math.inf, math.inf)
                    thr = threading.Thread(target=lambda que, *args: que.put((self.minimax(
                        *args), i)), args=(que, self.board, 0, False, -math.inf, math.inf))
                    threads.append(thr)
                    thr.start()
                    thr.join()
                    self.board.player[i] -= (1 * moves[i])
            while(not que.empty()):
                score, i = que.get()
                print(i, " score: ", score)
                self.arti2color = self.scoretocolor(score, False)
                if(score > bestscore):
                    bestscore = score
                    move = i
            print("\n", end='')
            return move
        else:
            bestscore = -math.inf
            moves = self.board.enemymoves()
            move = int()
            print("Red:")
            for i in range(3):
                if(moves[i] != 0):
                    self.board.enemy[i] += (1 * moves[i])
                    # score = self.minimax(
                    #     self.board, 0, True, -math.inf, math.inf)
                    thr = threading.Thread(target=lambda que, *args: que.put((self.minimax(
                        *args), i)), args=(que, self.board, 0, True, -math.inf, math.inf))
                    threads.append(thr)
                    thr.start()
                    thr.join()
                    self.board.enemy[i] -= (1 * moves[i])
            while(not que.empty()):
                score, i = que.get()
                print(i, " score: ", score)
                self.articolor = self.scoretocolor(score, True)
                if(score > bestscore):
                    bestscore = score
                    move = i
            print("\n", end='')
            return move


if __name__ == "__main__":
    print('Game:\nQ - exit\nR - reset\nC - choose who plays first\nNumpad 7, 4, 1 - green turn(upper/middle/lower)\nNumpad 1, 2, 3 - red turn(left/middle/right)\nColor of lower left square shows who\'s turn now \ncolor of lower right square shows chance of red to win(if ai enabled for red)\ncolor of upper left square shows chance of green to win (if ai enabled for green)\nPress any key to see computer\'s turn\nGreen plays first as default. To change it press \'C\' \nSet ai for red and green(1 - yes, 0 - no)\n')
    print("ai play for red(1/0): ")
    ARTI = int(input()) == 1
    print("ai play for green(1/0): ")
    ARTI2 = int(input()) == 1
    WIN_WIDTH = 501
    WIN_HEIGHT = 501
    WHITE = (68, 43, 72)
    GREEN = (101, 240, 42)  # (95, 232, 177)
    RED = (184, 24, 0)  # (214, 74, 49)
    startplayer = [0, 0, 0]
    startenemy = [0, 0, 0]
    isplayerturn = True
    Game(ARTI, ARTI2, WIN_WIDTH, WIN_HEIGHT,
         startplayer, startenemy, isplayerturn)
