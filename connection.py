from typing import List


def read_file(file_path: str) -> List[List[str]]:
    with open(file_path) as work_file:
        row = work_file.readlines()
        data = [item.replace('\n', '').split(';') for item in row]
        return data


def append_file(data: List[str], file_path: str) -> None:
    with open(file_path, 'a') as work_file:
        row = ';'.join(data)
        work_file.write(row + '\n')


def write_file(data: List[List[str]], file_path: str) -> None:
    with open(file_path, 'w') as work_file:
        for item in data:
            row = ';'.join(item)
            work_file.write(row + '\n')
