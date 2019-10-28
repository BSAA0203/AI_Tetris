import pygame as pg
import random, time, sys

WHITE       = (255, 255, 255)
BLACK       = (  0,   0,   0)
GRAY        =(177,177,177) # 맵 안의 선 색상

#블록 색상들
RED         = (155,   0,   0)
GREEN       = (  0, 155,   0)
BLUE        = (  0,   0, 155)
YELLOW      = (155, 155,   0)

#블록 색상에 그라데이션 효과를 주기 위한 색상들
LIGHTRED    = (175,  20,  20)
LIGHTGREEN  = ( 20, 175,  20)
LIGHTBLUE   = ( 20,  20, 175)
LIGHTYELLOW = (175, 175,  20)

SIZE = [800,640] # 게임 사이즈
WIDTH = SIZE[0] # 사이즈 가로 길이
HEIGHT = SIZE[1] # 사이즈 세로 길이

BOXSIZE = 30 # 블록 사이즈
BOXWIDTH = 5 # 블록의 가로 길이
BOXHEIGHT = 5 # 블록의 세로 길이

BOARDWIDTH = 10 # 맵 가로 길이
BOARDHEIGHT = 20 # 맵 세로 길이

BLANK = '.'

#컬러의 튜플화를 통한 랜덤 색상 지정 구현
COLORS =(BLUE, GREEN, RED, YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)

XMARGIN = (WIDTH - BOARDWIDTH * BOXSIZE) / 2
YMARGIN = (HEIGHT -BOARDHEIGHT * BOXSIZE) - 5

#블록들의 각기 다른 모양 디자인
S = [               ['.....',
                     '.....',
                     '..0O.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z= [                ['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I = [               ['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O = [               ['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J = [               ['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L = [               ['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T= [                ['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

#블록들의 딕셔너리화를 통해 마찬가지로 랜덤 선택에 도움을 준다
PIECES = {'S': S,
          'Z': Z,
          'J': J,
          'L': L,
          'I': I,
          'O': O,
          'T': T}

def end(sc): # 게임 오버 화면
    check = True
    while check:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                check = False
                sys.exit()

        GAME.fill(BLACK) # 배경색을 검은색으로
        endFont = pg.font.SysFont('times new roman', 72) # 게임 엔드 폰트
        reFont = pg.font.SysFont('monaco', 70) # 게임 재시작 폰트

        #게임 엔드 관련 텍스트 렌더링 및 배치
        GOsurf = endFont.render("Game Over", True, RED)
        GAME.blit(GOsurf, ( (WIDTH/ 2) - 150 , (HEIGHT / 2) - 50) )
        Ssurf = endFont.render("Score  :  {0}".format(sc), True, RED)
        GAME.blit(Ssurf, ( (WIDTH / 2) - 130 , (HEIGHT / 2) + 50) )

        #게임 재시작 관련 버튼 그리고 텍스트 디자인
        pg.draw.rect(GAME, WHITE, pg.Rect((WIDTH / 2) - 60, (HEIGHT / 2) + 150, 120, 50))
        text = reFont.render("RE?", True, BLACK)
        GAME.blit(text, ( (WIDTH / 2)-45 , (HEIGHT / 2)+155 ) )

        #마우스 커서 이벤트 구현
        cur = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if ((WIDTH / 2) - 60) + 120 > cur[0] > (WIDTH/ 2) - 60 and ((HEIGHT / 2) + 150) + 50 > cur[1] > (HEIGHT / 2) + 150:
            if (click[0] == 1):
                run()
        pg.display.flip()

def main():
    global FPS, GAME

    pg.init()
    GAME = pg.display.set_mode(SIZE)
    pg.display.set_caption('Tetris')
    FPS = pg.time.Clock()

    check = True
    while check:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                check = False
                sys.exit()

        GAME.fill(BLACK)
        TFont = pg.font.SysFont('Stencil', 100)
        GOsurf = TFont.render("Tetris", True, GREEN)
        GAME.blit(GOsurf, ((WIDTH / 2) - 150, (HEIGHT / 2) - 50))

        global MFont
        MFont = pg.font.SysFont('monaco', 50)

        pg.draw.rect(GAME, WHITE, pg.Rect((WIDTH / 2) - 60, (HEIGHT / 2) + 150, 120, 50)) # 버튼 디자인
        text = MFont.render("START", True, BLACK) # 버튼 글자
        GAME.blit(text, ((WIDTH / 2) - 55, (HEIGHT / 2) + 160))

        cur = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if ((WIDTH / 2) - 60) + 120 > cur[0] > (WIDTH / 2) - 60 and ((HEIGHT / 2) + 150) + 50 > cur[1] > (HEIGHT / 2) + 150:
            if (click[0] == 1):
                run()
                check = False
        pg.display.flip()

def run():
    board = getBlankBoard()

    score = 0
    level, fallsp = ingamesp(score)

    lastFallTime = time.time()

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    check = True
    while check:
        if fallingPiece == None:
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time()

            if not CHpiece(board, fallingPiece):
                end(score)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                check = False
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT and CHpiece(board, fallingPiece, X=-1):
                    fallingPiece['x'] -= 1
                elif event.key == pg.K_RIGHT and CHpiece(board, fallingPiece, X=1):
                    fallingPiece['x'] += 1
                elif event.key == pg.K_DOWN and CHpiece(board, fallingPiece, Y=1):
                        fallingPiece['y'] += 1
                elif event.key == pg.K_SPACE:
                    for i in range(BOARDHEIGHT):
                        if not CHpiece(board, fallingPiece, Y=i):
                            break
                    fallingPiece['y'] += i - 1
                elif event.key == pg.K_UP:
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not CHpiece(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                elif event.key == pg.K_r:
                    run()

        if time.time() - lastFallTime > fallsp:
            if not CHpiece(board, fallingPiece, Y=1):
                addToBoard(board, fallingPiece)
                score += remove(board)
                level, fallsp = ingamesp(score)
                fallingPiece = None
            else:
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        GAME.fill(BLACK)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pg.display.flip()
        FPS.tick(30)

def CHpiece(board, piece, X=0, Y=0):
    for x in range(BOXWIDTH):
        for y in range(BOXHEIGHT):
            ispiece = y + piece['y'] + Y
            if ispiece < 0 or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + X, y + piece['y'] + Y):
                return False
            if board[x + piece['x'] + X][y + piece['y'] + Y] != BLANK:
                return False
    return True

def getBlankBoard():
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board

def ingamesp(score):
    level = int(score/3) + 1
    if level < 6:
        fallsp = 0.6 -(level*0.1)+0.1
    else:
        fallsp = 0.1

    return level, fallsp

def getNewPiece():
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(BOXWIDTH / 2),
                'y': -2,
                'color': random.randint(0, len(COLORS)-1)}
    return newPiece

def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

def drawStatus(score, level):
    scoreSurf = MFont.render('Score: %s' % score, True, WHITE)
    GAME.blit(scoreSurf, (WIDTH - 150, 20))

    levelSurf = MFont.render('Level: %s' % level, True, WHITE)
    GAME.blit(levelSurf, (WIDTH - 150, 60))

def addToBoard(board, piece):
    for x in range(BOXWIDTH):
        for y in range(BOXHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']

def remove(board):
    removeline = 0
    y = BOARDHEIGHT - 1
    while y >= 0:
        if isCompleteLine(board, y):
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            removeline += 1
        else:
            y -= 1
    return removeline

def isCompleteLine(board, y):
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True

def drawBoard(board):
    pg.draw.rect(GAME, BLUE, (XMARGIN - 3, YMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])

def drawBox(boxx, boxy, color, pixelx=None, pixely=None):

    for i in range(BOARDWIDTH):
        pg.draw.line(GAME, GRAY, ((XMARGIN+10)+(i*BOXSIZE-10), YMARGIN-3), ((XMARGIN+10)+(i*BOXSIZE-10) , YMARGIN+600),2)
    for j in range(BOARDHEIGHT):
        pg.draw.line(GAME, GRAY, (XMARGIN + 10, (YMARGIN+3)+(j*BOXSIZE)), (XMARGIN + 300, (YMARGIN+3)+(j*BOXSIZE)),2)

    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = Pixel(boxx, boxy)
    pg.draw.rect(GAME, COLORS[color], (pixelx , pixely , BOXSIZE - 1, BOXSIZE - 1))
    pg.draw.rect(GAME, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 10, BOXSIZE - 10))

def drawNextPiece(piece):
    MFont = pg.font.SysFont('monaco', 50)
    nextSurf = MFont.render('Next:', True, WHITE)
    GAME.blit(nextSurf, (WIDTH - 120, 100))

    drawPiece(piece, pixelx=WIDTH-150, pixely=130)

def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = Pixel(piece['x'], piece['y'])

    for x in range(BOXWIDTH):
        for y in range(BOXHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def Pixel(boxx, boxy):
    return (XMARGIN + (boxx * BOXSIZE)), (YMARGIN + (boxy * BOXSIZE))

main()