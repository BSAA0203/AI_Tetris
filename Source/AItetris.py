import pygame as pg
import random, time, sys
import copy,numpy,pyautogui,math

# Define settings and constants
pyautogui.PAUSE = 0.03
pyautogui.FAILSAFE = True

# 게임 가로 세로 사이즈
WINDOWWIDTH = 800
WINDOWHEIGHT = 640

#블록 사이즈,가로,세로 길이
BOXSIZE = 30
BOXWIDTH = 5
BOXHEIGHT = 5

#보드 가로, 세로 길이
BOARDWIDTH = 10
BOARDHEIGHT = 20

BLANK = '0' # 빈 공간

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
YMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

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

# 보드 그리고 텍스트 색상들
BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY

#컬러의 튜플화를 통한 랜덤 색상 지정 구현
COLORS =(BLUE, GREEN, RED, YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)

# 블록 디자인
S_SHAPE_TEMPLATE = [['00000', '00000', '00110', '01100', '00000'],
                    ['00000', '00100', '00110', '00010', '00000']]

Z_SHAPE_TEMPLATE = [['00000', '00000', '01100', '00110', '00000'],
                    ['00000', '00100', '01100', '01000', '00000']]

I_SHAPE_TEMPLATE = [['00100', '00100', '00100', '00100', '00000'],
                    ['00000', '00000', '11110', '00000', '00000']]

O_SHAPE_TEMPLATE = [['00000', '00000', '01100', '01100', '00000']]

J_SHAPE_TEMPLATE = [['00000', '01000', '01110', '00000',
                     '00000'], ['00000', '00110', '00100', '00100', '00000'],
                    ['00000', '00000', '01110', '00010',
                     '00000'], ['00000', '00100', '00100', '01100', '00000']]
L_SHAPE_TEMPLATE = [['00000', '00010', '01110', '00000',
                     '00000'], ['00000', '00100', '00100', '00110', '00000'],
                    ['00000', '00000', '01110', '01000',
                     '00000'], ['00000', '01100', '00100', '00100', '00000']]

T_SHAPE_TEMPLATE = [['00000', '00100', '01110', '00000',
                     '00000'], ['00000', '00100', '00110', '00100', '00000'],
                    ['00000', '00000', '01110', '00100',
                     '00000'], ['00000', '00100', '01100', '00100', '00000']]
PIECES = {
    'S': S_SHAPE_TEMPLATE,
    'Z': Z_SHAPE_TEMPLATE,
    'J': J_SHAPE_TEMPLATE,
    'L': L_SHAPE_TEMPLATE,
    'I': I_SHAPE_TEMPLATE,
    'O': O_SHAPE_TEMPLATE,
    'T': T_SHAPE_TEMPLATE
}

# Define learning parameters
alpha = 0.01
gamma = 0.9
MAX_GAMES = 20
explore_change = 0.5
weights = [-1, -1, -1, -30]  # Initial weight vector

def Run_game(weights, explore_change):
    board = get_blank_board() # 보드 생성
    score = 0 # 스코어 초기화
    level, fall_freq = get_level_and_fall_freq(score) # 레벨 그리고 블록 떨어지는 속도 초기화
    current_move = [0, 0]  # 블록의 최적화 움직임
    falling_piece = get_new_piece() # 떨어지는 블록을 받고
    next_piece = get_new_piece() # 다음 블록 만든다
    last_fall_time = time.time() # 1초마다 블록이 떨어진다

    while True:
        if falling_piece is None:
            # 떨어지는 블록이 없으면 다음 블록을 받는다
            falling_piece = next_piece
            next_piece = get_new_piece()
            last_fall_time = time.time()  # reset last_fall_time

            if not is_valid_position(board, falling_piece): # 보드보다 블록이 더 높게 쌓였을 경우
                # can't fit a new piece on the board, so game over
                return score, weights, explore_change # 게임 오버로 인한 스코어, 학습 값 상태를 리턴
            current_move, weights = gradient_descent(board, falling_piece, weights,
                                                     explore_change)
            if explore_change > 0.001:
                explore_change = explore_change * 0.99
            else:
                explore_change = 0

        current_move = make_move(current_move)
        for event in pg.event.get():  # event handling loop
            if event.type == pg.QUIT:
                check = False
                sys.exit()

            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_LEFT or event.key == pg.K_a) and is_valid_position(
                            board, falling_piece, adj_x=-1): # 왼쪽 방향키
                    falling_piece['x'] -= 1
                elif (event.key == pg.K_RIGHT or event.key == pg.K_d) and is_valid_position(
                          board, falling_piece, adj_x=1): # 오른쪽 방향키
                    falling_piece['x'] += 1
                elif (event.key == pg.K_UP or event.key == pg.K_w): # 위 방향키
                    falling_piece['rotation'] = (falling_piece['rotation'] + 1) % len(PIECES[falling_piece['shape']])
                    if not is_valid_position(board, falling_piece):
                        falling_piece['rotation'] = (falling_piece['rotation'] - 1) % len(PIECES[falling_piece['shape']])
                elif (event.key == pg.K_DOWN or event.key == pg.K_s): # 아래 방향키
                    if is_valid_position(board, falling_piece, adj_y=1):
                        falling_piece['y'] += 1
                elif event.key == pg.K_SPACE: # 스페이스 키
                    for i in range(1, BOARDHEIGHT):
                        if not is_valid_position(board, falling_piece, adj_y=i):
                            break
                    falling_piece['y'] += i - 1

        if time.time() - last_fall_time > fall_freq: # 블록이 제시간에 맞게 떨어진 경우
            if not is_valid_position(board, falling_piece, adj_y=1):
                add_to_board(board, falling_piece) # 보드에 해당 블록을 채운다
                lines, board = remove_complete_lines(board) # 지워진 라인 수를 받아
                score += lines * lines # 스코어에 증가
                level, fall_freq = get_level_and_fall_freq(score) # 레벨과 떨어지는 속도 조정
                falling_piece = None # 떨어지는 블록은 현재 없다
            else:
                # 1초 간격으로 블록이 떨어지게 y 좌표 변화
                falling_piece['y'] += 1
                last_fall_time = time.time()
        GAME.fill(BGCOLOR)
        draw_board(board)
        draw_status(score, level, current_move,games_completed)
        draw_next_piece(next_piece)
        if falling_piece is not None:
            draw_piece(falling_piece)

        pg.display.update()
        FPS.tick(30) # 30 프레임으로 게임 동작

def make_text_objs(text, font, color):
    surf = font.render(text, True, color) # 폰트 렌더링
    return surf, surf.get_rect()

def show_text_screen(text): # 화면에 해당하는 내용 텍스트 출력
    title_surf, title_rect = make_text_objs(text, SubFont, TEXTSHADOWCOLOR)
    title_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    GAME.blit(title_surf, title_rect)

    title_surf, title_rect = make_text_objs(text, SubFont, TEXTCOLOR)
    title_rect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    GAME.blit(title_surf, title_rect)

    press_key_surf, press_key_rect = make_text_objs('Please wait to continue.',
                                                    SubFont, TEXTCOLOR)
    press_key_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    GAME.blit(press_key_surf, press_key_rect)

    pg.display.update()
    FPS.tick()
    time.sleep(0.5)

def get_level_and_fall_freq(score):
    level = int(score / 3)  # 스코어 3배수 마다 레벨 증가
    if level < 6:  # 레벨 6전까진 떨어지는 속도 감소
        fallsp = 0.6 - (level * 0.1) + 0.1
    else:  # 6 이후론 일정 속도로 유지
        fallsp = 0.2

    return level, fallsp  # 레벨 과 떨어지는 속도 값 리턴

def get_new_piece():
    # 랜덤함수로 새로운 블록 지정
    shape = random.choice(list(PIECES.keys()))
    new_piece = {
        'shape': shape,
        'rotation': random.randint(0,
                                   len(PIECES[shape]) - 1),
        'x': int(BOARDWIDTH / 2) - int(BOXWIDTH / 2),
        'y': -2,  # start it above the board (i.e. less than 0)
        'color': random.randint(1,
                                len(COLORS) - 1)
    }
    return new_piece

def add_to_board(board, piece):
    for x in range(BOXWIDTH):
        for y in range(BOXHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK and x + piece['x'] < 10 and y + piece['y'] < 20: # 블록이 떨어지려는 해당 보드 구간이 빈 공간이 아닐 경우
                board[x + piece['x']][y + piece['y']] = piece['color']# 블록과 같은 색상으로 해당 보드 구간을 채운다

def get_blank_board():
    # 정해둔 보드 가로 세로 사이즈 만큼 보드 배열 생성
    board = []
    for _ in range(BOARDWIDTH):
        board.append(['0'] * BOARDHEIGHT)
    return board

def is_on_board(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT # 블록이 보드 안에 있을 경우 true를 리턴

def is_valid_position(board, piece, adj_x=0, adj_y=0):
    for x in range(BOXWIDTH):
        for y in range(BOXHEIGHT):
            is_above_board = y + piece['y'] + adj_y < 0
            if is_above_board or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK: # 블록 떨어지는 구간이 빈 공간일 경우
                continue # 남은 블록 관련 점검을 진행한다
            if not is_on_board(x + piece['x'] + adj_x, y + piece['y'] + adj_y):
                return False  # 블록이 보드 틀을 벗어나려 한다면 false를 리턴
            if board[x + piece['x'] + adj_x][y + piece['y'] + adj_y] != BLANK:
                return False  # 블록 떨어지는 구간이 빈 공간이 아닐 경우 false를 리턴
    return True


def is_complete_line(board, y):
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK: # 보드의 라인에 빈 공간이 있을 경우
            return False #false를 리턴
    return True # 그 반대일 경우 true 리턴


def remove_complete_lines(board):
    lines_removed = 0
    y = BOARDHEIGHT - 1
    while y >= 0:
        if is_complete_line(board, y):
            for pull_down_y in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pull_down_y] = board[x][pull_down_y - 1] # 지워지는 보드 라인 위에 쌓인 블록들을 밑으로 내린다
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK # 빈 공간 없이 라인이 블록으로 가득찰 경우 그 라인의 보드들을 비운다
            lines_removed += 1# 지워진 라인 수 카운트 값 증가
        else:
            y -= 1
    return lines_removed, board

def convert_to_pixel_coords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (YMARGIN + (boxy * BOXSIZE))

def draw_box(boxx, boxy, color, pixelx=None, pixely=None):# 보드 안에 꾸준하게 이벤트가 일어나는 블록 내용들을 렌더링
    for i in range(BOARDWIDTH):
        pg.draw.line(GAME, GRAY, ((XMARGIN + 10) + (i * BOXSIZE - 10), YMARGIN - 3),
                     ((XMARGIN + 10) + (i * BOXSIZE - 10), YMARGIN + 600), 2)  # 보드 사선 중 세로 선 그리기
    for j in range(BOARDHEIGHT):
        pg.draw.line(GAME, GRAY, (XMARGIN, (YMARGIN - 3) + (j * BOXSIZE)),
                     (XMARGIN + 300, (YMARGIN - 3) + (j * BOXSIZE)), 2)  # 보드 사선 중 가로 선 그리기

    if color == BLANK:
        return
    if pixelx is None and pixely is None:
        pixelx, pixely = convert_to_pixel_coords(boxx, boxy)
    pg.draw.rect(GAME, COLORS[color],
                     (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pg.draw.rect(GAME, LIGHTCOLORS[color],
                     (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

def draw_board(board):
    # 코딩 해둔 보드 배열을 화면에 렌더링 한다
    pg.draw.rect(GAME, BORDERCOLOR,
                     (XMARGIN - 3, YMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8,
                      (BOARDHEIGHT * BOXSIZE) + 8), 5)
    # fill the background of the board
    pg.draw.rect(
        GAME, BGCOLOR,
        (XMARGIN, YMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            draw_box(x, y, board[x][y])


def draw_status(score, level, best_move, games_completed): # 화면에 스코어 레벨, 학습상태 그리고 다음 최적화된 블록 방향을 렌더링
    # draw the score text
    score_surf = SubFont.render('Score: %s' % score, True, TEXTCOLOR)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOWWIDTH - 200, 20)
    GAME.blit(score_surf, score_rect)

    # draw the level text
    level_surf = SubFont.render('Level: %s' % level, True, TEXTCOLOR)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (WINDOWWIDTH - 200, 50)
    GAME.blit(level_surf, level_rect)

    # draw the best_move text
    move_surf = SubFont.render('Current Move: %s' % best_move, True, TEXTCOLOR)
    move_rect = move_surf.get_rect()
    move_rect.topleft = (WINDOWWIDTH - 230, 300)
    GAME.blit(move_surf, move_rect)

    # draw the best_move text
    move_surf = SubFont.render('Learing level : %s' % games_completed, True, TEXTCOLOR)
    move_rect = move_surf.get_rect()
    move_rect.topleft = (20, 150)
    GAME.blit(move_surf, move_rect)

def draw_piece(piece, pixelx=None, pixely=None):
    shape_to_draw = PIECES[piece['shape']][piece['rotation']]
    if pixelx is None and pixely is None:
        # 화면에 렌더링 해야할 블록 x,y 좌표를 픽셀 x,y로 받는다
        pixelx, pixely = convert_to_pixel_coords(piece['x'], piece['y'])

    for x in range(BOXWIDTH):
        for y in range(BOXHEIGHT):
            if shape_to_draw[y][x] != BLANK:
                draw_box(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def draw_next_piece(piece): # 화면에 다음 블록 모양 렌더링
    # draw the "next" text
    next_surf = SubFont.render('Next:', True, TEXTCOLOR)
    next_rect = next_surf.get_rect()
    next_rect.topleft = (WINDOWWIDTH - 200, 80)
    GAME.blit(next_surf, next_rect)
    # draw the "next" piece
    draw_piece(piece, pixelx=WINDOWWIDTH - 180, pixely=100)

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
            if int(board[i][j]) > 0:  # Is the cell occupied?
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
            if int(board[i][j]) > 0:
                occupied = 1  # If a block is found, set the 'Occupied' flag to 1
            if int(board[i][j]) == 0 and occupied == 1:
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
    if not is_valid_position(test_board, test_piece, adj_x=sideways, adj_y=0):
        # The move itself is not valid!
        return None

    # Move the test_piece to collide on the board
    test_piece['x'] += sideways
    for i in range(0, BOARDHEIGHT):
        if is_valid_position(test_board, test_piece, adj_x=0, adj_y=1):
            test_piece['y'] = i

    # Place the piece on the virtual board
    if is_valid_position(test_board, test_piece, adj_x=0, adj_y=0):
        add_to_board(test_board, test_piece)
        test_lines_removed, test_board = remove_complete_lines(test_board)

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


def Run(g,f,s):
    global GAME, FPS, SubFont
    global weights,explore_change, games_completed
    GAME = g
    FPS = f
    SubFont = s

    games_completed = 0
    while True:  # game loop
        games_completed += 1
        newScore, weights, explore_change = Run_game(weights, explore_change)
        print("Game Number ", games_completed, " achieved a score of: ", newScore )
        if games_completed == MAX_GAMES: # 총 20번의 게임을 반복하면 게임 종료
            show_text_screen('Game Finish')
            time.sleep(3)
            return
        else:
            show_text_screen('Game Over') # 아닐경우 계속해서 플레이