from multiprocessing import freeze_support
from app import DunUniApp

if __name__ == '__main__':
    freeze_support()
    DunUniApp().run()
