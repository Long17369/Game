from typing import Dict, Union
from snd.others import Level


SCREEN_SIZE = (800, 600)
SCREEN_TITLE = "扫雷"
FPS = 60
MINEFIELD_SURFACE_RECT = (0.8, 3.2)


class Difficulty_Level():
    """
    | LEVEL | 难度 | 大小 | 雷数 |
    |----|----|----|----|
    | BEGINNER | 初级 | 9x9 | 10 |
    | INTERMEDIATE | 中级 | 16x16 | 40 |
    | ADVANCED | 高级 | 30x16 | 99 |
    """
    BEGINNER = Level(9, 9, 10)            # 初级 Beginner
    INTERMEDIATE = Level(16, 16, 40)      # 中级 Intermediate
    ADVANCED = Level(30, 16, 99)          # 高级 Advanced


LEVEL = Difficulty_Level
