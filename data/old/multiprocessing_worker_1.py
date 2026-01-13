# Source - https://stackoverflow.com/q
# Posted by Xing Shi
# Retrieved 2025-11-29, License - CC BY-SA 3.0

from multiprocessing import Lock, Pool

def worker():
    r = other.work()
    return r

def main():
    pool = Pool(4)
    result = pool.apply_sync(worker,())
    result.wait()
