import pygame as pg
import sys
import Playtetris
import AItetris

WHITE       = (255, 255, 255) # 텍스트 폰트 색상
BLACK       = (  0,   0,   0) #배경색
FontColor = (255,140,0) # 타이틀 폰트 색상

SIZE = [800,640] # 게임 디스플레이 사이즈
WIDTH = SIZE[0] # 디스플레이 가로 길이
HEIGHT = SIZE[1] # 디스플레이 세로 길이

# 폰트 배치 X,Y 좌표 전역 변수
x = WIDTH / 2
y = HEIGHT / 2

def main():
    pg.init() # Pygame 라이브러리 초기화
    GAME = pg.display.set_mode(SIZE) # 게임 디스플레이 옵션
    pg.display.set_caption('Tetris') # 디스플레이 타이틀 생성
    pg.display.set_icon(pg.image.load("../img/tetris.png"))
    FPS = pg.time.Clock() # 게임 프레임 옵션
    pg.mixer.music.load('../Sound/bgm.mp3') # 게임 BGM
    pg.mixer.music.play(-1)

    check = True
    while check:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                check = False
                sys.exit()

            elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_1: # 1번이 눌렸을 경우 직접 플레이로
                        soundObj = pg.mixer.Sound('../Sound/key.wav')  # 키보드 관련 효과음 출력
                        soundObj.play()
                        Playtetris.Run(GAME,FPS,MFont)
                    elif event.key ==  pg.K_2: # 2번이 눌렸을 경우 AI 플레이로
                        soundObj = pg.mixer.Sound('../Sound/key.wav')  # 키보드 관련 효과음 출력
                        soundObj.play()
                        AItetris.Run(GAME,FPS,SFont)

        GAME.fill(BLACK)
        TFont = pg.font.SysFont('Snap ITC', 100) # 게임 화면 타이틀 폰트
        GOsurf = TFont.render("Tetris", True, FontColor) # 타이틀 렌더링
        GAME.blit(GOsurf, (x - 150, y - 150)) # 타이틀 배치
        MFont = pg.font.SysFont('monaco', 50) # 게임 화면 텍스트 폰트
        SFont = pg.font.SysFont('monaco', 35) # 게임 화면 텍스트 폰트
        text = MFont.render("1. Play tetris", True, WHITE) # 텍스트 렌더링
        text2 = MFont.render("2. Watch Ai play tetris", True, WHITE)
        GAME.blit(text, (x - 120, y + 120))
        GAME.blit(text2, (x - 120, y + 200))

        pg.display.update()

main() # 시작은 메인함수부터