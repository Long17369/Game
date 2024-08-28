from typing import Dict, Union


SCREEN_SIZE = (800, 600)
SCREEN_TITLE = "扫雷"
FPS = 60
MINEFIELD_SURFACE_RECT = (20, 80)


class Level():
    """难度
    """

    x: int
    y: int
    mine_count: int

    def __init__(self, x=None, y=None, mine_count=None) -> None:
        if isinstance(x, (tuple, list, dict)):
            self.from_dict(dict(x))
            return
        if x == None:
            x = 9
        if y == None:
            y = x
        if mine_count == None:
            mine_count = 10
        if x < 9 or y < 9 or mine_count < 10:
            raise ValueError("参数不能太小")
        self.x = int(x)
        self.y = int(y)
        self.mine_count = int(mine_count)

    def __len__(self) -> int:
        return 3

    def __setitem__(self, index: Union[int, str], value: int) -> None:
        if index in [0, '0', 'x']:
            self.x = value
        elif index in [1, '1', 'y']:
            self.y = value
        elif index in [2, '2', 'mine_count']:
            self.mine_count = value
        else:
            raise IndexError

    def __getitem__(self, index: Union[int, str]) -> int:
        if index in [0, '0', 'x']:
            return self.x
        elif index in [1, '1', 'y']:
            return self.y
        elif index in [2, '2', 'mine_count']:
            return self.mine_count
        else:
            raise IndexError

    def __str__(self) -> str:
        return f'Level(x:{self.x}, y:{self.y}, mine_count:{self.mine_count})'

    @classmethod
    def from_dict(cls, d: Dict[str, Union[str, int]]):
        return cls(int(d['x']), int(d['y']), int(d['mine_count']))

class Difficulty_Level():
    """
    | LEVEL | 难度 |
    |----|----|
    | BEGINNER | 初级 |
    | INTERMEDIATE | 中级 |
    | ADVANCED | 高级 |
    """
    BEGINNER = Level(9, 9, 10)            # 初级 Beginner
    INTERMEDIATE = Level(16, 16, 40)      # 中级 Intermediate
    ADVANCED = Level(30, 16, 99)          # 高级 Advanced


LEVEL = Difficulty_Level
