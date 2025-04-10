from pathlib import Path

current = Path(__file__).parent
filename = current / 'record.txt'




def get_record():
    if not filename.is_file():
        with open(filename, 'w') as f:
            f.write('0\n')

    record = None

    with open(filename, 'r') as f:
        record = int(f.readline().strip())
    return int(record)


def write_record(record:int):
    with open(filename, 'w') as f:
        f.write(f"{record}\n")


if __name__ == "__main__":
    ...




