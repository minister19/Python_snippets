from multiprocessing import Process, Queue, Pipe


def f1(q):
    q.put([42, None, 'hello'])


def main():
    q = Queue()
    p = Process(target=f1, args=(q,))
    p.start()
    print(q.get())
    p.join()


if __name__ == '__main__':
    main()


def f2(conn):
    conn.send([42, None, 'hello'])
    conn.close()


def main2():
    (parent_conn, child_conn) = Pipe()
    p = Process(target=f2, args=(child_conn,))
    p.start()
    print(parent_conn.recv())
    p.join()


if __name__ == '__main__':
    main2()
