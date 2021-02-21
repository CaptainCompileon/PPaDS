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
        if shared.counter >= shared.end:
            shared.mutex.unlock()
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
    print(sh.counter)

# V tomto pripade by sa mal program spravat korektne z dovodu prakticky
# serioveho vykonavania kazdeho kroku cyklu while funkcie counter. Jeden
# z threadov si acquirne mutex
# lock v prvom kroku cyklu a vrati ho v oboch pripadoch:
# 1. ak splni podmienku kontroly, ci sa nenachadza mimo index pola zdielaneho
# objektu Shared
# 2. ak nesplni, tak vykona inkrementaciu hodnoty na indexe v poli a hodnotu
# counter zdielaneho objektu Shared
# Vysledok: algoritmus sa sprava spravne vzhladom na to ze sa kazdy krok cyklu
# while vykona vzdy len jednym threadom,
# resp. kazda kriticka oblast je kryta mutex lockom
