""""Author: Katarína Stasová
    Program uses a simple barrier to execute a part of code with all threads before the next
    part of code start to execute. """
from fei.ppds import Thread, Semaphore, Mutex, print


class SimpleBarrier:
    """"A simple barrier for waiting for all threads to complete the part of code
    """

    def __init__(self, thread_count):
        """Simple barrier initialization:
         all_thread_count - the number of threads used in the program
         count - the number of waiting threads in turnstile
         mutex - synchronization tool to make the critical area atomically executed
         turnstile - synchronization tool to management threads

        :param thread_count: the number of threads used in the program
        """
        self.all_thread_count = thread_count
        self.count = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)

    def wait(self):
        """Waiting until all threads have completed part of the code.
        Between locked mutex is code automatically executed.
        The turnstile method wait() blocks all threads, which invoke it, until method signal() happened.

        :rtype: None
        """
        self.mutex.lock()
        self.count += 1
        if self.count == self.all_thread_count:
            self.count = 0
            self.turnstile.signal(self.all_thread_count)
        self.mutex.unlock()
        self.turnstile.wait()


def use_barrier(barrier, thread_id):
    """All threads executing this function. Each of thread print the sentence before barrier with id.
    Barrier waits for all threads. Each of thread print the sentence after barrier with id.

    :param barrier: Instance of SimpleBarrier
    :param thread_id: Id of thread

    :rtype: None
    """
    print("Thread %d before barrier" % thread_id)
    barrier.wait()
    print("Thread %d after barrier" % thread_id)


if __name__ == '__main__':
    thread_count = 5
    sb = SimpleBarrier(thread_count)
    threads = [Thread(use_barrier, sb, i) for i in range(thread_count)]
    [t.join() for t in threads]
