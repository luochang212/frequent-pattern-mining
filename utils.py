import os
import collections
import pickle
import pandas as pd


def gen_abspath(directory: str, rel_path: str) -> str:
    """
    Generate the absolute path by combining the given directory with a relative path.

    :param directory: The specified directory, which can be either an absolute or a relative path.
    :param rel_path: The relative path with respect to the 'dir'.
    :return: The resulting absolute path formed by concatenating the absolute directory
             and the relative path.
    """
    abs_dir = os.path.abspath(directory)
    return os.path.join(abs_dir, rel_path)


def read_csv(
    file_path: str,
    sep: str = ',',
    header: int = 0,
    on_bad_lines: str = 'warn',
    encoding: str = 'utf-8',
    dtype: dict = None,
    **kwargs
) -> pd.DataFrame:
    """
    Read a CSV file from the specified path.
    """
    return pd.read_csv(file_path,
                       header=header,
                       sep=sep,
                       on_bad_lines=on_bad_lines,
                       encoding=encoding,
                       dtype=dtype,
                       **kwargs)


class Convert:

    def __init__(self, lst: list, file_path='./item_list.pkl'):
        self.lst = lst
        self.file_path = file_path

        # 对 lst 进行编码
        self.item_list = None
        self.item_dict = None
        self.parse()

    @staticmethod
    def to_dict(item_list):
        item_dict = dict()
        for i, item in enumerate(item_list):
            item_dict[item] = i
        return item_dict

    def parse(self):
        """对列表元素编码"""

        # 统计字符串频率
        frequency = collections.Counter(self.lst)

        # 按字符串频率，倒序排列
        sorted_items = sorted(frequency.items(),
                              key=lambda e: e[1],
                              reverse=True)

        self.item_list = [e[0] for e in sorted_items]
        self.item_dict = self.to_dict(self.item_list)

    def reset(self):
        self.item_list = self.read()
        self.item_dict = self.to_dict(self.item_list)

    def __len__(self):
        return len(self.item_list)

    def __getitem__(self, index):
        return self.item_list[index]

    def encoder(self, item):
        return self.item_dict.get(item)

    def save(self):
        with open(self.file_path, 'wb') as f:
            pickle.dump(self.item_list, f)

    def read(self):
        with open(self.file_path, 'rb') as f:
            item_list = pickle.load(f)
        return item_list
