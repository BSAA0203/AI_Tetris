import pygame as pg
import random, time, sys
import math, copy, numpy, pyautogui

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

# 머신 러닝 관련 파라미터 값
alpha = 0.01
gamma = 0.9
MAX_GAMES = 20
explore_change = 0.5
weights = [-1, -1, -1, -30]  # Initial weight vector

def make_text_objs(text, font, color):
    surf = font.render(text, True, color) # 받은 폰트를 기준으로 텍스트 렌더링
    return surf, surf.get_rect()

def show_text_screen(text): # 화면에 텍스트 배치
    # 텍스트 그림자 효과
    title_surf, title_rect = make_text_objs(text, MainFont, GRAY)
    title_rect.center = (int(WIDTH / 2), int(HEIGHT / 2))
    GAME.blit(title_surf, title_rect)

    # 타이틀 텍스트 렌더링
    title_surf, title_rect = make_text_objs(text, MainFont, WHITE)
    title_rect.center = (int(WIDTH / 2) - 3, int(HEIGHT / 2) - 3)
    GAME.blit(title_surf, title_rect)

    # 부가 설명 텍스트 렌더링
    press_key_surf, press_key_rect = make_text_objs('Please wait to continue.',
                                                    MainFont, WHITE)
    press_key_rect.center = (int(WIDTH / 2), int(HEIGHT / 2) + 100)
    GAME.blit(press_key_surf, press_key_rect)

    pg.display.update()
    FPS.tick()
    time.sleep(0.5)

def Run(g,f,m):
    global GAME, FPS, MainFont
    global weights,explore_change,games_completed
    GAME=g
    FPS=f
    MainFont=m

    games_completed = 0
    time.sleep(5)
    while True:
        games_completed += 1 # 게임이 돌 때 마다 카운트
        newScore, weights, explore_change = Run_game(weights, explore_change)
        print("Game Number ", games_completed, " achieved a score of: ", newScore) # 콘솔에 한번 돌때마다 해당 스코어 출력
        show_text_screen('Game Over')
        if games_completed > 20 : # 총 20번 돌면 게임 종료
            break

def Run_game(weights, explore_change):
    board = getBlankBoard()  # 게임 맵에 해당하는 보드 생성
    score = 0  # 게임 스코어 초기화
    level = 0 # 게임 레벨 초기화
    fallsp = 0.2 # 게임 레벨과 블록 떨어지는 속도 값 초기화
    lastFallTime = time.time()  # 1초 간격으로 블록이 떨어지는 효과를 위한 시간 체킹
    fallingPiece = getNewPiece()  # 떨어지는 블록 생성
    nextPiece = getNewPiece()  # 다음 블록 생성

    current_move = [0, 0]  # Relative Rotation, lateral movement

    check = True
    while check:
        if fallingPiece == None:  # 떨어지는 블록이 없을 경우
            fallingPiece = nextPiece  # 다음 블록으로 교체
            nextPiece = getNewPiece()  # 새로운 블록을 받는다
            lastFallTime = time.time()

            if not CHpiece(board, fallingPiece):  # 블록이 게임 보드 보다 높게 쌓였을 경우 게임 오버
                return score, weights, explore_change
            current_move, weights = gradient_descent(board, fallingPiece, weights,
                                                     explore_change)
            if explore_change > 0.001:
                explore_change = explore_change * 0.99
            else:
                explore_change = 0

        current_move = make_move(current_move)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                check = False
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT and CHpiece(board, fallingPiece, X=-1):  # 왼쪽 방향키가 눌렸을 때
                    fallingPiece['x'] -= 1  # 떨어지는 블록 왼쪽으로 이동
                elif event.key == pg.K_RIGHT and CHpiece(board, fallingPiece, X=1):  # 오른쪽 방향키가 눌렸을 때
                    fallingPiece['x'] += 1  # 떨어지는 블록 오른쪽 이동
                elif event.key == pg.K_DOWN and CHpiece(board, fallingPiece, Y=1):  # 밑 방향키가 눌렸을 때
                    fallingPiece['y'] += 1  # 떨어지는 블록 밑으로 이동
                elif event.key == pg.K_SPACE:  # 스페이스 키가 눌렸을 때
                    for i in range(BOARDHEIGHT):
                        if not CHpiece(board, fallingPiece, Y=i):
                            break  # 떨어지려는 구간이 더 이상 없을 경우 스페이스 기능 block
                    fallingPiece['y'] += i - 1  # 블록을 제일 밑으로 떨어트린다
                elif event.key == pg.K_UP:  # 윗 방향키가 눌렸을 때
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])  # 블록의 모양 변화
                    if not CHpiece(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])

        if time.time() - lastFallTime > fallsp:
            if not CHpiece(board, fallingPiece, Y=1):
                addToBoard(board, fallingPiece)  # 보드에 해당 블록을 채운다
                score += remove(board)  # 지워진 라인 수 만큼 스코어 증가
                level = int(score/3)  # 레벨은 3배수 단위로
                fallingPiece = None  # 떨어지는 블록은 현재 없다
            else:
                # 1초 간격으로 블록이 떨어지게 y 좌표 변화
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        GAME.fill(BLACK)  # 게임 배경색을 검은색으로
        drawBoard(board)  # 보드를 화면에 렌더링
        drawStatus(score, level)  # 스코어와 레벨 텍스트 렌더링
        NextPiece_info(nextPiece)  # 다음 블록 렌더링
        if fallingPiece != None:
            drawPiece(fallingPiece)  # 떨어지는 블록 렌더링

        pg.display.update()  # 디스플레이 업데이트
        FPS.tick(30)  # 30 프레임으로 진행

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
        board.append([BLANK] * BOARDHEIGHT) # 정해둔 맵 가로,세로 사이즈 만큼 보드를 배열로 구성
    return board # 보드 배열 리턴

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

    ailevelSurf = MainFont.render('Learn level : %s' % games_completed, True, WHITE)  # 화면에 레벨 텍스트 렌더링
    GAME.blit(ailevelSurf, (0, 120))

def addToBoard(board, piece):
    for x in range(BOXWIDTH):
        for y in range(BOXHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:# 블록이 떨어지려는 해당 보드 구간이 빈 공간이 아닐 경우
                board[x + piece['x']][y + piece['y']] = piece['color'] # 블록과 같은 색상으로 해당 보드 구간을 채운다

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










def get_parameters(board):
    # This function will calculate different parameters of the current board

    # Initialize some stuff
    heights = [0]*BOARDWIDTH
    diffs = [0]*(BOARDWIDTH-1)
    holes = 0
    diff_sum = 0

    # Calculate the maximum height of each column
    for i in range(0, BOARDWIDTH):  # Select a column
        for j in range(0, BOARDHEIGHT):  # Search down starting from the top of the board
            if board[i][j]!=BLANK:  # Is the cell occupied?
                heights[i] = BOARDHEIGHT - j  # Store the height value
                break

    # Calculate the difference in heights
    for i in range(0, len(diffs)):
        diffs[i] = heights[i + 1] - heights[i]

    # Calculate the maximum height
    max_height = max(heights)

    # Count the number of holes
    for i in range(0, BOARDWIDTH):
        occupied = 0  # Set the 'Occupied' flag to 0 for each new column
        for j in range(0, BOARDHEIGHT):  # Scan from top to bottom
            if board[i][j]!=BLANK:
                occupied = 1  # If a block is found, set the 'Occupied' flag to 1
            if board[i][j]==BLANK and occupied == 1:
                holes += 1  # If a hole is found, add one to the count

    height_sum = sum(heights)
    for i in diffs:
        diff_sum += abs(i)
    return height_sum, diff_sum, max_height, holes

def get_expected_score(test_board, weights):
    # This function calculates the score of a given board state, given weights and the number
    # of lines previously cleared.
    height_sum, diff_sum, max_height, holes = get_parameters(test_board)
    A = weights[0]
    B = weights[1]
    C = weights[2]
    D = weights[3]
    test_score = float(A * height_sum + B * diff_sum + C * max_height + D * holes)
    return test_score

def simulate_board(test_board, test_piece, move):
    # This function simulates placing the current falling piece onto the
    # board, specified by 'move,' an array with two elements, 'rot' and 'sideways'.
    # 'rot' gives the number of times the piece is to be rotated ranging in [0:3]
    # 'sideways' gives the horizontal movement from the piece's current position, in [-9:9]
    # It removes complete lines and gives returns the next board state as well as the number
    # of lines cleared.

    rot = move[0]
    sideways = move[1]
    test_lines_removed = 0
    reference_height = get_parameters(test_board)[0]
    if test_piece is None:
        return None

    # Rotate test_piece to match the desired move
    for i in range(0, rot):
        test_piece['rotation'] = (test_piece['rotation'] + 1) % len(PIECES[test_piece['shape']])

    # Test for move validity!
    if not CHpiece(test_board, test_piece, Ⅹ=sideways, Y=0):
        # The move itself is not valid!
        return None

    # Move the test_piece to collide on the board
    test_piece['x'] += sideways
    for i in range(0, BOARDHEIGHT):
        if CHpiece(test_board, test_piece, Ⅹ=0, Y=1):
            test_piece['y'] = i

    # Place the piece on the virtual board
    if CHpiece(test_board, test_piece, X=0, Y=0):
        CHpiece(test_board, test_piece)
        test_lines_removed= remove(test_board)

    height_sum, diff_sum, max_height, holes = get_parameters(test_board)
    one_step_reward = 5 * (test_lines_removed * test_lines_removed) - (height_sum - reference_height)
    return test_board, one_step_reward

def find_best_move(board, piece, weights, explore_change):
    move_list = []
    score_list = []
    for rot in range(0, len(PIECES[piece['shape']])):
        for sideways in range(-5, 6):
            move = [rot, sideways]
            test_board = copy.deepcopy(board)
            test_piece = copy.deepcopy(piece)
            test_board = simulate_board(test_board, test_piece, move)
            if test_board is not None:
                move_list.append(move)
                test_score = get_expected_score(test_board[0], weights)
                score_list.append(test_score)
    best_score = max(score_list)
    best_move = move_list[score_list.index(best_score)]

    if random.random() < explore_change:
        move = move_list[random.randint(0, len(move_list) - 1)]
    else:
        move = best_move
    return move

def make_move(move):
    # This function will make the indicated move, with the first digit
    # representing the number of rotations to be made and the seconds
    # representing the column to place the piece in.
    rot = move[0]
    sideways = move[1]
    if rot != 0:
        pyautogui.press('up')
        rot -= 1
    else:
        if sideways == 0:
            pyautogui.press('space')
        if sideways < 0:
            pyautogui.press('left')
            sideways += 1
        if sideways > 0:
            pyautogui.press('right')
            sideways -= 1

    return [rot, sideways]

def gradient_descent(board, piece, weights, explore_change):
    move = find_best_move(board, piece, weights, explore_change)
    old_params = get_parameters(board)
    test_board = copy.deepcopy(board)
    test_piece = copy.deepcopy(piece)
    test_board = simulate_board(test_board, test_piece, move)
    if test_board is not None:
        new_params = get_parameters(test_board[0])
        one_step_reward = test_board[1]
    for i in range(0, len(weights)):
        weights[i] = weights[i] + alpha * weights[i] * (
            one_step_reward - old_params[i] + gamma * new_params[i])
    regularization_term = abs(sum(weights))
    for i in range(0, len(weights)):
        weights[i] = 100 * weights[i] / regularization_term
        weights[i] = math.floor(1e4 * weights[i]) / 1e4  # Rounds the weights
    return move, weights