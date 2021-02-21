from fei.ppds import Thread, Mutex


class Shared():
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end
        self.mutex = Mutex()


class Histogram(dict):
    def __init__(self, seq=[]):
        for item in seq:
            self[item] = self.get(item, 0) + 1


def counter(shared):
    while True:
        shared.mutex.lock()
        if shared.counter >= shared.end:  # (1)
            break
        shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()


for _ in range(10):
    sh = Shared(1_000_000)
    t1 = Thread(counter, sh)
    t2 = Thread(counter, sh)

    t1.join()
    t2.join()

    print(Histogram(sh.array))

# V takomto pripade je riesenie nespravne z dovodu deadlocku v momente
# ako nahle splni podmienku (1). Po splneni tejto podmienky sa pomocou break
# ukonci cyklus no thread ostane locknuty a uz sa nedostane k unlocku
# a tym zablokuje pristup vsetkym vlaknam
