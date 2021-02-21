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
        if shared.counter >= shared.end:
            break
        shared.mutex.lock()
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

# V takomto pripade sa moze stat ze vo funkcii counter pri if podmienke sa\
# vykona nespravna kontrola z dovodu ze ju mozu vykonavat viacera vlakna
# ucasne a sice sa inkrementacie vykonaju atomicky tak sa moze stat scenar
# ze prvy thread skontroluje ci nie je mimmo indexu potom druhy thread vykona
# tu istu kontrolu (tu je problem) a nasledne prvy thread vykona zalockovanu
# sekciu zvysi index Shared.counter na index mimo velkosti pola.
# uz teraz vieme povedat ze ked sa pokusi druhy thread vykonat
# shared.array[shared.counter] += 1 vrati mu exception lebo pristupuje
# na index mimo pola. Tomuto by sa mohlo predist ak by sa cely jeden krok
# cyklu vykonaval atomicky.
