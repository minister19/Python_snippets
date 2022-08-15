from threading import Lock


class extend_class(set):
    def __init__(self, *args, **kwargs):
        self._lock = Lock()
        super(extend_class, self).__init__(*args, **kwargs)

    def add(self, elem):
        self._lock.acquire()
        try:
            super(extend_class, self).add(elem)
        finally:
            self._lock.release()

    def delete(self, elem):
        self._lock.acquire()
        try:
            super(extend_class, self).delete(elem)
        finally:
            self._lock.release()
