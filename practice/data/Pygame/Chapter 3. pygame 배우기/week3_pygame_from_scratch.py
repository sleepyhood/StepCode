# Week 3 - pygame 기본기 (From Scratch 과제)
# 거의 100% 직접 구현: 윈도우 생성, 루프, 그리기, 입력, 충돌, 점수 표시까지.
# 각 TODO를 채우면 자연스럽게 한 단계씩 완성됩니다.
#
# 실행 전: pip install pygame
#
# 권장 진행(50~90분)
#  - TODO 1~4: 초기화, 창, 루프, 배경 그리기
#  - TODO 5~7: 플레이어 이동 및 경계 처리, dt 적용
#  - TODO 8~10: 타겟 스폰/충돌/점수, 텍스트 렌더링
#  - (옵션) TODO 11~14: 사운드, 그리드, 난이도, 일시정지/재시작
#
# 컨셉: "Collect Game"
#  - 화살표 키로 플레이어 사각형을 움직여 화면에 나타나는 타겟(원)을 먹습니다.
#  - 먹을 때마다 점수가 오르고, 일정 점수마다 속도가 증가합니다.
#  - 화면 밖으로 못 나가도록 경계 처리를 합니다.

import pygame
import random
from dataclasses import dataclass

# ------------------------------ 상수 ------------------------------
WIDTH, HEIGHT = 800, 600      # TODO 1: 사이즈 조정 가능
FPS_START = 60                # 기본 프레임 상한
PLAYER_SIZE = 28
PLAYER_SPEED = 220            # TODO 5: dt와 곱해 사용 (px/s)
TARGET_RADIUS = 12
SPEED_STEP_SCORE = 5          # TODO 10: 이 점수마다 난이도(속도) 소폭 증가
FONT_NAME = "malgungothic"    # OS에 따라 대체 폰트가 사용될 수 있음
BG = (18, 18, 18)
FG = (230, 230, 230)
GRID = (40, 40, 40)
PLAYER_COLOR = (0, 200, 120)
TARGET_COLOR = (220, 70, 70)

# ------------------------------ 유틸 ------------------------------
def clamp(value, low, high):
    return max(low, min(value, high))

# ------------------------------ 엔티티 ------------------------------
@dataclass
class Player:
    x: float
    y: float
    w: int = PLAYER_SIZE
    h: int = PLAYER_SIZE
    vx: float = 0.0
    vy: float = 0.0

    # TODO 6: update(self, dt) - 키 입력을 바탕으로 속도/위치 갱신하고, 화면 경계 내로 클램핑
    def update(self, dt, keys):
        raise NotImplementedError("TODO 6: Player.update - 입력, 속도, 위치, 경계 처리 구현")

    # TODO 4: draw(self, surf) - 사각형으로 플레이어 그리기
    def draw(self, surf):
        raise NotImplementedError("TODO 4: Player.draw - pygame.draw.rect 사용")

    # 보조: 파이게임 Rect로 충돌판정에 사용
    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

@dataclass
class Target:
    x: float
    y: float
    r: int = TARGET_RADIUS

    # TODO 8: draw(self, surf) - 원 그리기
    def draw(self, surf):
        raise NotImplementedError("TODO 8: Target.draw - pygame.draw.circle 사용")

    @property
    def pos(self):
        return (int(self.x), int(self.y))

# ------------------------------ 게임 상태 ------------------------------
class Game:
    def __init__(self):
        # TODO 2: pygame 초기화, 화면/시계/폰트 생성 및 상태값 초기화
        raise NotImplementedError("TODO 2: Game.__init__ - 초기화 및 상태 구성")

    # TODO 3: run(self) - 메인 루프(이벤트 처리 → 업데이트 → 렌더 → tick)
    def run(self):
        raise NotImplementedError("TODO 3: Game.run - 메인 루프 구현")

    # -------------------------- 로직 보조 --------------------------
    # TODO 5: 입력 처리 - 화살표(또는 WASD)로 플레이어 이동 방향 결정
    def handle_input(self):
        raise NotImplementedError("TODO 5: Game.handle_input - 입력 처리 및 종료/재시작")

    # TODO 7: 타겟 생성 - 화면 안 랜덤 좌표
    def spawn_target(self):
        raise NotImplementedError("TODO 7: Game.spawn_target - 랜덤 위치 배치")

    # TODO 9: 충돌판정 - 플레이어 사각형과 타겟 원의 충돌(근사: 원의 중심이 rect안에 들어오면 히트)
    def check_collision(self):
        raise NotImplementedError("TODO 9: Game.check_collision - 플레이어와 타겟 충돌 검사")

    # TODO 10: 점수/난이도 처리 - 점수 획득 시 속도 또는 목표 스폰 주기/크기 변경 등
    def on_score(self):
        raise NotImplementedError("TODO 10: Game.on_score - 난이도/속도 조정")

    # -------------------------- 렌더링 --------------------------
    def draw_grid(self):
        # (옵션) TODO 12: 보기 편한 그리드
        pass

    # TODO 4/8 연계: 엔티티 그리기 + HUD(점수, 속도, 도움말)
    def draw(self):
        raise NotImplementedError("TODO 4/8: Game.draw - 배경/그리드/플레이어/타겟/HUD 렌더")

    # (옵션) TODO 11: 사운드 - 점수 획득 시 효과음
    def play_pick_sound(self):
        pass

# ------------------------------ 진입점 ------------------------------
if __name__ == "__main__":
    # TODO 1~3을 통과하면 Game().run()으로 게임이 동작합니다.
    game = Game()
    game.run()
