import time
from typing import Dict, Union


_log = False  # 用于控制是否记录日志


def log(func):
    """
    装饰器函数，用于记录被装饰函数的调用信息
    func: 被装饰的函数
    """
    def wrapper(*args, **kwargs):
        """
        内部函数，用于包装被装饰的函数，记录其调用信息

        参数:
        args: 被装饰函数的非关键字参数
        kwargs: 被装饰函数的关键字参数
        """
        result = func(*args, **kwargs)  # 调用被装饰的函数，并获取其返回值
        if _log:  # 如果全局变量_log为True，则记录日志
            with open('log.txt', 'a') as f:  # 以追加模式打开日志文件
                print(
                    f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}', file=f)  # 打印当前时间
                print(f'{func.__name__}', file=f)  # 打印被装饰函数的名称
                for i in range(len(args)):  # 遍历非关键字参数
                    print(f'{i},{args[i]}', file=f)  # 打印参数索引和值
                for i in kwargs:  # 遍历关键字参数
                    print(f'{i}:{kwargs[i]}', file=f)  # 打印参数名和值
                print(f'result:{result}', file=f)  # 打印函数返回值
                print(
                    '--------------------------------------------------------------------------------', file=f)  # 打印分隔线
        return result  # 返回被装饰函数的返回值
    return wrapper  # 返回包装后的函数


@log  # 使用log装饰器装饰Log函数
def Log(*args, **kwargs):
    """
    日志记录函数，用于记录函数调用信息。

    参数:
    args: 非关键字参数
    kwargs: 关键字参数
    """
    return  # 返回None


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
