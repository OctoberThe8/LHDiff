# Source - https://stackoverflow.com/a
# Posted by ebarr
# Retrieved 2025-11-29, License - CC BY-SA 3.0

from multiprocessing import Lock, Pool

def worker():
    r = other.work()
    return r

def main():
    pool = Pool(4)

    # note: this is apply_async, not apply_sync
    result = pool.apply_async(worker,())
    result.wait()

    # See here
    actual_result = result.get()
