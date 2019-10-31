import pygame as pg
import random, time, sys

WHITE       = (255, 255, 255) # 텍스트 폰트 색상
BLACK       = (  0,   0,   0) #배경색
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

BOARDWIDTH = 10 # 게임 보드 가로 길이
BOARDHEIGHT = 20 # 게임 보드 세로 길이

BLANK = '.' # 빈 공간 생성

#컬러의 튜플화를 통한 랜덤 색상 지정 구현
COLORS =(BLUE, GREEN, RED, YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)

XMARGIN = int((WIDTH - BOARDWIDTH * BOXSIZE) / 2) # 디스플레이에서 보드까지 떨어진 X 값
YMARGIN = HEIGHT -(BOARDHEIGHT * BOXSIZE) - 5 # 디스플레이에서 보드까지 떨어진 Y 값

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
                    Run(GAME, FPS, MainFont)

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

def Run(g,f,m):
    global GAME, FPS, MainFont
    GAME=g
    FPS=f
    MainFont=m

    board = getBlankBoard() # 게임 맵에 해당하는 보드 생성
    score = 0 # 게임 스코어 초기화
    level, fallsp = ingamesp(score) # 게임 레벨과 블록 떨어지는 속도 값 초기화
    lastFallTime = time.time() # 1초 간격으로 블록이 떨어지는 효과를 위한 시간 체킹
    fallingPiece = getNewPiece() # 떨어지는 블록 생성
    nextPiece = getNewPiece() # 다음 블록 생성

    check = True
    while check:
        if fallingPiece == None: # 떨어지는 블록이 없을 경우
            fallingPiece = nextPiece # 다음 블록으로 교체
            nextPiece = getNewPiece() # 새로운 블록을 받는다
            lastFallTime = time.time()

            if not CHpiece(board, fallingPiece): # 블록이 게임 보드 보다 높게 쌓였을 경우 게임 오버
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
                            break # 떨어지려는 구간이 더 이상 없을 경우 스페이스 기능 block
                    fallingPiece['y'] += i - 1 # 블록을 제일 밑으로 떨어트린다
                elif event.key == pg.K_UP: # 윗 방향키가 눌렸을 때
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']]) # 블록의 모양 변화
                    if not CHpiece(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                elif event.key == pg.K_r: # R키가 눌렸을 때
                    soundObj = pg.mixer.Sound('../Sound/key.wav') # 키보드 관련 효과음 출력
                    soundObj.play()
                    Run(GAME,FPS,MainFont) # 게임 재시작

        if time.time() - lastFallTime > fallsp: # 블록이 제시간에 맞게 떨어진 경우
            if not CHpiece(board, fallingPiece, Y=1):
                addToBoard(board, fallingPiece) # 보드에 해당 블록을 채운다
                score += remove(board) # 지워진 라인 수 만큼 스코어 증가
                level, fallsp = ingamesp(score) # 레벨과 떨어지는 속도 조정
                fallingPiece = None # 떨어지는 블록은 현재 없다
            else:
                #1초 간격으로 블록이 떨어지게 y 좌표 변화
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        GAME.fill(BLACK) # 게임 배경색을 검은색으로
        drawBoard(board) # 보드를 화면에 렌더링
        drawStatus(score, level) # 스코어와 레벨 텍스트 렌더링
        NextPiece_info(nextPiece) # 다음 블록 렌더링
        if fallingPiece != None:
            drawPiece(fallingPiece) # 떨어지는 블록 렌더링

        pg.display.update() # 디스플레이 업데이트
        FPS.tick(30) # 30 프레임으로 진행

def CHpiece(board, piece, X=0, Y=0):
    for x in range(BOXWIDTH):
        for y in range(BOXHEIGHT):
            ispiece = y + piece['y'] + Y
            if ispiece < 0 or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK: # 블록 떨어지는 구간이 빈 공간일 경우
                continue # 남은 블록 관련 점검을 진행한다
            if not isOnBoard(x + piece['x'] + X, y + piece['y'] + Y):
                return False # 블록이 보드 틀을 벗어나려 한다면 false를 리턴
            if board[x + piece['x'] + X][y + piece['y'] + Y] != BLANK:
                return False # 블록 떨어지는 구간이 빈 공간이 아닐 경우 false를 리턴
    return True

def getBlankBoard():
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT) # 정해둔 보드 가로 세로 사이즈 만큼 보드 배열 생성
    return board # 보드 배열 리턴

def ingamesp(score):
    level = int(score/3) # 스코어 3배수 마다 레벨 증가
    if level < 6: # 레벨 6전까진 떨어지는 속도 감소
        fallsp = 0.6 -(level*0.1)+0.1
    else: # 6 이후론 일정 속도로 유지
        fallsp = 0.2

    return level, fallsp # 레벨 과 떨어지는 속도 값 리턴

def getNewPiece():
    shape = random.choice(list(PIECES.keys())) # 랜덤함수로 새로운 블록 지정
    newPiece = {'shape': shape, # 블록의 모양
                'rotation': random.randint(0, len(PIECES[shape]) - 1), # 블록의 회전 방향
                # 블록의 X,Y 좌표를 화면 한 가운데로 지정
                'x': int(BOARDWIDTH / 2) - int(BOXWIDTH / 2),
                'y': -2,
                'color': random.randint(0, len(COLORS)-1)} # 블록 색상 역시 랜덤 지정
    return newPiece # 만들어진 블록을 리턴

def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT # 블록이 보드 안에 있을 경우 true를 리턴

def drawStatus(score, level):
    scoreSurf = MainFont.render('Score: %s' % score, True, WHITE) # 화면에 스코어 텍스트 렌더링
    GAME.blit(scoreSurf, (WIDTH - 150, 20)) # 텍스트 배치

    levelSurf = MainFont.render('Level: %s' % level, True, WHITE) # 화면에 레벨 텍스트 렌더링
    GAME.blit(levelSurf, (WIDTH - 150, 60))

def addToBoard(board, piece):
    for x in range(BOXWIDTH):
        for y in range(BOXHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:# 블록이 떨어지려는 해당 보드 구간이 빈 공간이 아닐 경우
                board[x + piece['x']][y + piece['y']] = piece['color'] # 블록과 같은 색상으로 해당 보드 구간을 채운다
                blocksound = pg.mixer.Sound('../Sound/selection.wav') # 블록 관련 효과음 출력
                blocksound.play()

def remove(board):
    removeline = 0
    y = BOARDHEIGHT - 1
    while y >= 0:
        if isCompleteLine(board, y):
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1] # 지워지는 보드 라인 위에 쌓인 블록들을 밑으로 내린다
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK # 빈 공간 없이 라인이 블록으로 가득찰 경우 그 라인의 보드들을 비운다
                removesound = pg.mixer.Sound('../Sound/clear.wav') # 블록 삭제 관련 효과음 출력
                removesound.play()
            removeline += 1 # 지워진 라인 수 카운트 값 증가
        else:
            y -= 1
    return removeline # 지워진 라인 수 리턴

def isCompleteLine(board, y):
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK: # 보드의 라인에 빈 공간이 있을 경우
            return False #false를 리턴
    return True # 그 반대일 경우 true 리턴

def drawBoard(board):
    pg.draw.rect(GAME, BLUE, (XMARGIN - 3, YMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5) # 코딩 해둔 보드 배열을 화면에 렌더링 한다

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])

def drawBox(boxx, boxy, color, pixelx=None, pixely=None): # 보드 안에 꾸준하게 이벤트가 일어나는 블록 내용들을 렌더링
    for i in range(BOARDWIDTH):
        pg.draw.line(GAME, GRAY, ((XMARGIN+10)+(i*BOXSIZE-10), YMARGIN-3), ((XMARGIN+10)+(i*BOXSIZE-10) , YMARGIN+600),2) # 보드 사선 중 세로 선 그리기
    for j in range(BOARDHEIGHT):
        pg.draw.line(GAME, GRAY, (XMARGIN, (YMARGIN-3)+(j*BOXSIZE)), (XMARGIN + 300, (YMARGIN-3)+(j*BOXSIZE)),2) # 보드 사선 중 가로 선 그리기

    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = Pixel(boxx, boxy)
    pg.draw.rect(GAME, COLORS[color], (pixelx , pixely , BOXSIZE - 1, BOXSIZE - 1))
    pg.draw.rect(GAME, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 10, BOXSIZE - 10))

def NextPiece_info(piece):
    MFont = pg.font.SysFont('monaco', 50)
    nextSurf = MFont.render('Next:', True, WHITE)
    GAME.blit(nextSurf, (WIDTH - 120, 100)) # 화면 오른쪽에 다음 블록 관련 텍스트 배치

    drawPiece(piece, pixelx=WIDTH-150, pixely=130)

def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = Pixel(piece['x'], piece['y']) # 화면에 렌더링 해야할 블록 x,y 좌표를 픽셀 x,y로 받는다

    for x in range(BOXWIDTH):
        for y in range(BOXHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def Pixel(boxx, boxy):
    return (XMARGIN + (boxx * BOXSIZE)), (YMARGIN + (boxy * BOXSIZE))