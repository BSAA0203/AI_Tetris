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

SIZE = [800,640] # 게임 디스플레이 사이즈
WIDTH = SIZE[0] # 디스플레이 가로 길이
HEIGHT = SIZE[1] # 디스플레이 세로 길이

BOXSIZE = 30 # 블록 사이즈
BOXWIDTH = 5 # 블록의 가로 길이
BOXHEIGHT = 5 # 블록의 세로 길이

BOARDWIDTH = 10 # 게임 맵 가로 길이
BOARDHEIGHT = 20 # 게임 맵 세로 길이

BLANK = '.' # 렌더링 전 시스템상으로 해당 내용 코딩

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

#블록들의 딕셔너리화를 통해 마찬가지로 랜덤 선택 구현
PIECES = {'S': S,
          'Z': Z,
          'J': J,
          'L': L,
          'I': I,
          'O': O,
          'T': T}

# 폰트 배치 X,Y 좌표 전역 변수
x = WIDTH / 2
y = HEIGHT / 2

def end(score): # 게임 오버 화면
    check = True
    while check:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                check = False
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r: # R키가 눌렸을 경우 게임 재시작
                    Play_game()

        GAME.fill(BLACK) # 게임 배경색을 검은색으로
        endFont = pg.font.SysFont('times new roman', 72) # 게임 엔드 폰트
        reFont = pg.font.SysFont('monaco', 70) # 게임 재시작 폰트

        #게임 엔드 관련 텍스트 렌더링 및 배치
        text = endFont.render("Game Over", True, RED)
        GAME.blit(text, ( x - 150 , y - 50) )
        text = endFont.render("Score  :  {0}".format(score), True, RED)
        GAME.blit(text, ( x - 130 , y + 50) )

        #게임 재시작 관련 텍스트 렌더링 및 배치
        text = reFont.render("Press R to restart", True, WHITE)
        GAME.blit(text, ( x - 180 , y + 180 ) )

        pg.display.update()

def main():
    global FPS, GAME
    global MFont

    pg.init() # Pygame 라이브러리 초기화
    GAME = pg.display.set_mode(SIZE) # 게임 디스플레이 옵션
    pg.display.set_caption('Tetris') # 디스플레이 타이틀 생성
    FPS = pg.time.Clock() # 게임 프레임 옵션

    check = True
    while check:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                check = False
                sys.exit()

            elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_1: # 1번이 눌렸을 경우 직접 플레이로
                        Play_game()
                    elif event.key ==  pg.K_2: # 2번이 눌렸을 경우 AI 플레이로
                        Auto_game()

        GAME.fill(BLACK)
        TFont = pg.font.SysFont('Snap ITC', 100) # 게임 화면 타이틀 폰트
        GOsurf = TFont.render("Tetris", True, GREEN) # 타이틀 렌더링
        GAME.blit(GOsurf, (x - 150, y - 150))

        MFont = pg.font.SysFont('monaco', 50) # 게임 화면 텍스트 폰트
        text = MFont.render("1. Play tetris", True, WHITE) # 텍스트 렌더링
        text2 = MFont.render("2. Watch Ai play tetris", True, WHITE)
        GAME.blit(text, (x - 120, y + 120))
        GAME.blit(text2, (x - 120, y + 200))

        pg.display.update()

def Play_game():
    board = getBlankBoard() # 게임 맵에 해당하는 보드 생성
    score = 0 # 게임 스코어 초기화
    level, fallsp = ingamesp(score) # 게임 레벨과 블록 떨어지는 속도 값 초기화
    lastFallTime = time.time()
    fallingPiece = getNewPiece() # 떨어지는 블록 생성
    nextPiece = getNewPiece() # 다음 블록 생성

    check = True
    while check:
        if fallingPiece == None: # 떨어지는 블록이 없을 경우
            fallingPiece = nextPiece # 다음 블록으로 교체
            nextPiece = getNewPiece() # 새로운 블록을 받는다
            lastFallTime = time.time()

            if not CHpiece(board, fallingPiece): # 맵 안에 블록이 다 찰 경우
                end(score) # 게임 오버로 변경

        for event in pg.event.get():
            if event.type == pg.QUIT:
                check = False
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT and CHpiece(board, fallingPiece, X=-1): # 왼쪽 방향키가 눌렸을 때
                    fallingPiece['x'] -= 1 # 떨어지는 블록 왼쪽으로 이동
                elif event.key == pg.K_RIGHT and CHpiece(board, fallingPiece, X=1): # 오른쪽 방향키가 눌렸을 때
                    fallingPiece['x'] += 1 # 떨어지는 블록 오른쪽 이동
                elif event.key == pg.K_DOWN and CHpiece(board, fallingPiece, Y=1): # 밑 방향키가 눌렸을 때
                        fallingPiece['y'] += 1 # 떨어지는 블록 밑으로 이동
                elif event.key == pg.K_SPACE: # 스페이스 키가 눌렸을 때
                    for i in range(BOARDHEIGHT):
                        if not CHpiece(board, fallingPiece, Y=i):
                            break
                    fallingPiece['y'] += i - 1 # 블록을 제일 밑으로 떨어트린다
                elif event.key == pg.K_UP: # 윗 방향키가 눌렸을 때
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']]) # 블록의 모양 변화
                    if not CHpiece(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                elif event.key == pg.K_r: # R키가 눌렸을 때
                    Play_game() # 게임 재시작

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
        drawBoard(board) # 보드를 화면에 렌더링
        drawStatus(score, level) # 스코어와 레벨 텍스트 렌더링
        drawNextPiece(nextPiece) # 다음 블록 렌더링
        if fallingPiece != None:
            drawPiece(fallingPiece) # 떨어지는 블록 렌더링

        pg.display.flip() # 디스플레이 업데이트
        FPS.tick(30) # 30 프레임으로 진행

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
        board.append([BLANK] * BOARDHEIGHT) # 정해둔 맵 가로,세로 사이즈 만큼 보드 배열 구성
    return board

def ingamesp(score):
    level = int(score/3) + 1 # 스코어 3배수 마다 레벨 증가
    if level < 6: # 레벨 6전까진 떨어지는 속도 감소
        fallsp = 0.6 -(level*0.1)+0.1
    else: # 6 이후론 일정 속도로 유지
        fallsp = 0.2

    return level, fallsp

def getNewPiece():
    shape = random.choice(list(PIECES.keys())) # 랜덤함수로 새로운 블록 지정
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                # X,Y 좌표를 화면 한 가운데로 지정
                'x': int(BOARDWIDTH / 2) - int(BOXWIDTH / 2),
                'y': -2,
                'color': random.randint(0, len(COLORS)-1)} # 색상 역시 랜덤 지정
    return newPiece

def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT # 보드 안에 블록이 있을 경우

def drawStatus(score, level):
    scoreSurf = MFont.render('Score: %s' % score, True, WHITE) # 화면에 스코어 텍스트 렌더링
    GAME.blit(scoreSurf, (WIDTH - 150, 20))

    levelSurf = MFont.render('Level: %s' % level, True, WHITE) # 화면에 레벨 텍스트 렌더링
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

def Auto_game():
    pass

main() # 시작은 메인함수부터