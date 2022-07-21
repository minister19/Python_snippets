import multiprocessing


def print_records(records):
    for record in records:
        print("Name: {0}\nScore: {1}\n".format(record[0], record[1]))


def insert_record(record, records):
    records.append(record)
    print("A New record is added\n")


if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        records = manager.list([('Computers', 1), ('Histoty', 5), ('Hindi', 9)])
        new_record = ('English', 3)

        p1 = multiprocessing.Process(target=insert_record, args=(new_record, records))
        p2 = multiprocessing.Process(target=print_records, args=(records,))
        p1.start()
        p1.join()
        p2.start()
        p2.join()


def Mng_NaSp(using_ns):
    using_ns.x += 5
    using_ns.y *= 10


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    using_ns = manager.Namespace()
    using_ns.x = 1
    using_ns.y = 1

    print('before', using_ns)
    p = multiprocessing.Process(target=Mng_NaSp, args=(using_ns,))
    p.start()
    p.join()
    print('after', using_ns)
