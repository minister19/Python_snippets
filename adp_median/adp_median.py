# ref: https://blog.csdn.net/qq_17758897/article/details/102695849

'''   自适应中值滤波器的python实现   '''
import numpy as np


def AdaptProcess(src, i, minSize, maxSize):
    filter_size = minSize

    kernelSize = filter_size // 2
    rio = src[i - kernelSize:i + kernelSize + 1]
    minPix = np.min(rio)
    maxPix = np.max(rio)
    medPix = np.median(rio)
    zxy = src[i]

    if (medPix > minPix) and (medPix < maxPix):
        if (zxy > minPix) and (zxy < maxPix):
            return zxy
        else:
            return medPix
    else:
        filter_size = filter_size + 1
        if filter_size <= maxSize:
            return AdaptProcess(src, i, filter_size, maxSize)
        else:
            return medPix


def adapt_meadian_filter(data, minsize=7, maxsize=14):
    borderSize = maxsize // 2

    src = list(data)
    src.extend(data[-1 - borderSize:-1])

    for m in range(borderSize, len(src) - borderSize):
        src[m] = AdaptProcess(src, m, minsize, maxsize)

    ret = src[0:len(data)]
    return ret


def main():
    data = [0, 1, 2, 3, 4, 100, 200, 1, 2, 3, 4, 3, 2, 1, 0]

    dst = adapt_meadian_filter(data=data, minsize=2, maxsize=7)
    print(data, len(data))
    print(dst, len(dst))


if __name__ == '__main__':
    main()
