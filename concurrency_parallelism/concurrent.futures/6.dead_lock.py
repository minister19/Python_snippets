import threading
import random
import time


class DiningPhilosopher(threading.Thread):
    running = True

    def __init__(self, xname, Leftfork, Rightfork):
        threading.Thread.__init__(self)
        self.name = xname
        self.Leftfork = Leftfork
        self.Rightfork = Rightfork

    def run(self):
        while(self.running):
            time.sleep(random.uniform(3, 13))
            print('%s is hungry.' % self.name)
            self.dine()

    def dine(self):
        fork1, fork2 = self.Leftfork, self.Rightfork

        while self.running:
            fork1.acquire(True)
            locked = fork2.acquire(False)
            if locked:
                break
            fork1.release()
            print('%s swaps forks' % self.name)
            fork1, fork2 = fork2, fork1
        else:
            return

        self.dining()
        fork2.release()
        fork1.release()

    def dining(self):
        print('%s starts eating ' % self.name)
        time.sleep(random.uniform(1, 10))
        print('%s finishes eating and now thinking.' % self.name)


def Dining_Philosophers():
    forks = [threading.Lock() for n in range(5)]
    philosopherNames = ('1st', '2nd', '3rd', '4th', '5th')

    philosophers = [DiningPhilosopher(philosopherNames[i], forks[i % 5], forks[(i+1) % 5])
                    for i in range(5)]

    random.seed()
    DiningPhilosopher.running = True
    for p in philosophers:
        p.start()
    time.sleep(30)
    DiningPhilosopher.running = False
    print(" It is finishing.")


if __name__ == "__main__":
    Dining_Philosophers()
