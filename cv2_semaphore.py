from fei.ppds import Thread, Mutex, Semaphore
from fei.ppds import print


class SharedList:
    def __init__(self, end):
        self.array = [0, 1] + [0] * end
        self.current = 2
        self.end = end


def countfibonaccielementonindex(index, sharedlist):
    previous = sharedlist.array[index - 1]
    preprevious = sharedlist.array[index - 2]
    if (preprevious == 0 or previous == 0) and index > 2:
        raise Exception("Sorry, no zeros")
    sharedlist.array[index] = sharedlist.array[index - 1] + \
                              sharedlist.array[index - 2]


def fibonacci(sharedlist, index, threadname):
    countfibonaccielementonindex(index, sharedlist)
    print('%s index: %d actual: %d' % (threadname, index, sharedlist.array[index]))
    # sharedlist.current += 1
    # if len(sharedlist.array) >= sharedlist.end:
    #     break


# class NotSimpleBarrier:
#     def __init__(self, numberOfThreads):
#         self.numberOfThreads = numberOfThreads
#         self.count = 0
#         self.mutex = Mutex()
#         self.semaphore1 = Semaphore(0)
#         self.semaphore2 = Semaphore(0)
#
#
# def rendezvous(thread_name):
#     sleep(randint(1, 10) / 10)
#     print('rendezvous: %s' % thread_name)
#
#
# def ko(thread_name):
#     print('ko: %s' % thread_name)
#     sleep(randint(1, 10) / 10)
#
#
# def barrier(thread_name, notSimpleBarrrier):
#     while True:
#         rendezvous(thread_name)
#
#         notSimpleBarrrier.mutex.lock()
#         notSimpleBarrrier.count += 1
#         if notSimpleBarrrier.count == notSimpleBarrrier.numberOfThreads:
#             # notSimpleBarrrier.count = 0
#             notSimpleBarrrier.semaphore1.signal()
#         notSimpleBarrrier.mutex.unlock()
#         notSimpleBarrrier.semaphore1.wait()
#         notSimpleBarrrier.count -= 1
#
#         if notSimpleBarrrier.count != 0:
#             notSimpleBarrrier.semaphore1.signal()
#
#         ko(thread_name)
#
#         notSimpleBarrrier.mutex.lock()
#         notSimpleBarrrier.count += 1
#         if notSimpleBarrrier.count == notSimpleBarrrier.numberOfThreads:
#             # notSimpleBarrrier.count = 0
#             notSimpleBarrrier.semaphore2.signal()
#         notSimpleBarrrier.mutex.unlock()
#         notSimpleBarrrier.semaphore2.wait()
#
#         notSimpleBarrrier.count -= 1
#
#         if notSimpleBarrrier.count != 0:
#             notSimpleBarrrier.semaphore1.signal()
#
#
# numberOfThreads = 10
# notSimpleBarrier = NotSimpleBarrier(numberOfThreads)
# threads = list()
# for i in range(numberOfThreads):
#     t = Thread(barrier, 'Thread %d' % i, notSimpleBarrier)
#     threads.append(t)
#
# for t in threads:
#     t.join()


numberOfThreads = 100
threads = list()
shlist = SharedList(numberOfThreads)
for i in range(numberOfThreads):
    t = Thread(fibonacci, shlist, i + 2, 'Thread %d' % i)
    threads.append(t)

for t in threads:
    t.join()

print(shlist.array)
