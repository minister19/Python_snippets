from threading import Lock


def lock_decorator(method):
    def new_deco_method(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)
    return new_deco_method


class Decorator_class(set):
    def __init__(self, *args, **kwargs):
        self._lock = Lock()
        super(Decorator_class, self).__init__(*args, **kwargs)

    @lock_decorator
    def add(self, elem):
        return super(Decorator_class, self).add(elem)

    @lock_decorator
    def delete(self, elem):
        return super(Decorator_class, self).delete(elem)
