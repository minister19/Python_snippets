import time
import multiprocessing


def square(n):
    result = n*n
    return result


if __name__ == '__main__':
    inputs = range(5)
    p = multiprocessing.Pool(processes=4)
    p_outputs = p.map(square, inputs)
    p.close()
    p.join()
    print('Pool: ', p_outputs)
