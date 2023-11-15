import time

from filter import *
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start = time.time()
    sortBy()
    end = time.time() - start  ## собственно время работы программы

    print(f"Время выполнения: {end}")