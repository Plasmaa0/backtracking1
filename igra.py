import pygame


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
    """
    Game
    Q - выход
    R - сброс
    C - выбор, кто ходит первый (только если ни один ход не был сделан)
    Numpad 7,4,1 - ход зеленой фишкой (верхней/средней/нижней)
    Numpad 1,2,3 - ход красной фишкой (левой/средней/правой)
    """

    def __init__(self, artion: bool, width: int, height: int, playerstartpos: list, enemystartpos: list, isplayerturn: int):
        self.arti = artion
        self.BACKGOUNDCOLOR = (0, 0, 0)
        self.board = Board(playerstartpos, enemystartpos, isplayerturn)
        self.sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption(
            "Game")
        while(True):
            self.checkwin()
            self.playturn()
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
            turncolor = (0, 200, 0)  # player
        else:
            turncolor = (150, 0, 0)  # enemy
        pygame.draw.rect(self.sc, turncolor, (1, 401, 99, 99))
    # <!-- eslint-disable-next-line - ->  #убрать комментирование если бесит, что vscode выдает ошибки в обозначениях клавиш типа "pygame.K_ESCAPE", "pygame.K_c"

    def playturn(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_q):
                    pygame.quit()
                if(event.key == pygame.K_r):
                    self.reset(None)
                if(event.key == pygame.K_c and sum(self.board.player) + sum(self.board.enemy) == 0):
                    self.board.isplayerturn = not self.board.isplayerturn
                before = sum(self.board.player) + sum(self.board.enemy)
                if(self.board.isplayerturn):
                    mov = self.board.playermoves()
                    if(sum(mov) == 0):
                        self.board.isplayerturn = False
                    if event.key == pygame.K_KP7 or event.key == pygame.K_KP8 or event.key == pygame.K_KP9:
                        self.board.player[0] += (1 * mov[0])
                    elif event.key == pygame.K_KP4 or event.key == pygame.K_KP5 or event.key == pygame.K_KP6:
                        self.board.player[1] += (1 * mov[1])
                    elif event.key == pygame.K_KP1 or event.key == pygame.K_KP2 or event.key == pygame.K_KP3:
                        self.board.player[2] += (1 * mov[2])
                else:
                    mov = self.board.enemymoves()
                    if(sum(mov) == 0):
                        self.board.isplayerturn = True
                    if(self.arti):
                        ind = self.ai(mov)
                        self.board.enemy[ind] += (1 * mov[ind])
                    else:
                        if event.key == pygame.K_KP1 or event.key == pygame.K_KP4 or event.key == pygame.K_KP7:
                            self.board.enemy[0] += (1 * mov[0])
                        elif event.key == pygame.K_KP2 or event.key == pygame.K_KP5 or event.key == pygame.K_KP8:
                            self.board.enemy[1] += (1 * mov[1])
                        elif event.key == pygame.K_KP3 or event.key == pygame.K_KP6 or event.key == pygame.K_KP9:
                            self.board.enemy[2] += (1 * mov[2])
                if(sum(self.board.player) + sum(self.board.enemy) != before):
                    self.board.isplayerturn = not self.board.isplayerturn

    def reset(self, playerwins):
        if(playerwins != None):
            if(playerwins):
                self.sc.fill((0, 200, 0))
            else:
                self.sc.fill((150, 0, 0))
            pygame.display.update()
            pygame.time.delay(1000)
        self.board.player = [0, 0, 0]
        self.board.enemy = [0, 0, 0]

    def checkwin(self):
        if(sum(self.board.player) == 12):
            self.reset(True)
        elif(sum(self.board.enemy) == 12):
            self.reset(False)

    def ai(self, possiblemoves: list) -> int:  # выбирает вариант с наибольшей дальностью хода
        a = max(possiblemoves)
        for i in range(len(possiblemoves)):
            if possiblemoves[i] == a:
                return i


if __name__ == "__main__":
    ARTI = False
    WIN_WIDTH = 501
    WIN_HEIGHT = 501
    WHITE = (255, 255, 255)
    GREEN = (95, 232, 177)
    RED = (214, 74, 49)

    startplayer = [0, 0, 0]  # 1
    startenemy = [0, 0, 0]  # -1
    isplayerturn = True
    Game(ARTI, WIN_WIDTH, WIN_HEIGHT,
         startplayer, startenemy, isplayerturn)
