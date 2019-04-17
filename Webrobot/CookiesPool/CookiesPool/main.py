from scheduler import Scheduler
from importer import Importer

if __name__ == '__main__':
    init = Importer('weibo')
    init.input_accounts()
    pool = Scheduler()
    pool.run()
