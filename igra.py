import pygame
from pygame.locals import *
ARTI = 0
FPS = 24
WIN_WIDTH = 501
WIN_HEIGHT = 501
WHITE = (255, 255, 255)
GREEN = (95, 232, 177)
RED = (214, 74, 49)
BACKGOUNDCOLOR = (0, 0, 0)
player = [0, 0, 0]  # 1
enemy = [0, 0, 0]  # 2
who = 1


def drawenv(sc):
    global who
    for i in range(6):
        pygame.draw.line(sc, WHITE, [0, 100*i], [500, 100*i])
        pygame.draw.line(sc, WHITE, [100*i, 0], [100*i, 500])
    for i in range(3):
        pygame.draw.rect(
            sc, GREEN, (player[i]*100 + 45, 140 + 100*i, 30, 10))
        pygame.draw.rect(
            sc, RED, (140 + 100*i, 450 - enemy[i]*100, 10, 30))
    if(who == 1):
        turncolor = (0, 200, 0)  # player
    else:
        turncolor = (150, 0, 0)  # enemy
    pygame.draw.rect(sc, turncolor, (1, 401, 99, 99))


def playermoves():
    mov = [1, 1, 1]
    for i in range(3):
        player_y = i + 1
        player_x = player[i]
        enemycords = []
        enemy_xs = []
        for j in range(3):
            enemy_y = 4 - enemy[j]
            enemy_x = j + 1
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


def enemymoves():
    mov = [1, 1, 1]
    for i in range(3):
        enemy_y = 4 - enemy[i]
        enemy_x = i + 1
        playercords = []
        player_ys = []
        for j in range(3):
            player_y = j + 1
            player_x = player[j]
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


def ai(possiblemoves: list) -> int:  # выбирает вариант с наибольшей дальностью хода
    a = max(possiblemoves)
    for i in range(len(possiblemoves)):
        if possiblemoves[i] == a:
            return i


def turn():
    global who
    global player
    global enemy
    global before
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_ESCAPE):
                pygame.quit()
            if(event.key == pygame.K_r):
                player = [0, 0, 0]
                enemy = [0, 0, 0]
            if(event.key == pygame.K_c and sum(player) + sum(enemy) == 0):
                who *= -1
            before = sum(player) + sum(enemy)
            if(who == 1):
                mov = playermoves()
                if(sum(mov) == 0):
                    who *= -1
                if event.key == pygame.K_KP7 or event.key == pygame.K_KP8 or event.key == pygame.K_KP9:
                    player[0] += (1 * mov[0])
                elif event.key == pygame.K_KP4 or event.key == pygame.K_KP5 or event.key == pygame.K_KP6:
                    player[1] += (1 * mov[1])
                elif event.key == pygame.K_KP1 or event.key == pygame.K_KP2 or event.key == pygame.K_KP3:
                    player[2] += (1 * mov[2])
            else:
                mov = enemymoves()
                if(sum(mov) == 0):
                    who *= -1
                global ARTI
                if(ARTI == 1):
                    ind = ai(mov)
                    enemy[ind] += (1 * mov[ind])
                else:
                    if event.key == pygame.K_KP1 or event.key == pygame.K_KP4 or event.key == pygame.K_KP7:
                        enemy[0] += (1 * mov[0])
                    elif event.key == pygame.K_KP2 or event.key == pygame.K_KP5 or event.key == pygame.K_KP8:
                        enemy[1] += (1 * mov[1])
                    elif event.key == pygame.K_KP3 or event.key == pygame.K_KP6 or event.key == pygame.K_KP9:
                        enemy[2] += (1 * mov[2])
            after = sum(player) + sum(enemy)
            if(after != before):
                who *= -1


def checkwin():
    global player
    global enemy
    wincolor = (0, 0, 0)
    win = 0
    if(sum(player) == 12):
        wincolor = (0, 200, 0)
        win = 1
    if(sum(enemy) == 12):
        wincolor = (150, 0, 0)
        win = 1
    if(win != 0):
        sc.fill(wincolor)
        pygame.display.update()
        pygame.time.delay(1000)
        player = [0, 0, 0]
        enemy = [0, 0, 0]


if __name__ == "__main__":
    clock = pygame.time.Clock()
    sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(
        "Game")
    '''
        Escape - выход
        R - сброс
        C - выбор, кто ходит первый (только если ни один ход не был сделан)
        Numpad 7,4,1 - ход зеленой фишкой (верхней/средней/нижней)
        Numpad 1,2,3 - ход красной фишкой (левой/средней/правой)
        '''
    while(True):
        checkwin()
        turn()
        sc.fill(BACKGOUNDCOLOR)
        BACKGOUNDCOLOR = tuple([int(i*0.9) for i in BACKGOUNDCOLOR])
        drawenv(sc)
        pygame.display.update()
        clock.tick(FPS)
