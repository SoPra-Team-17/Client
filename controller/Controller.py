import time
import logging



class Controller:

    def __init__(self):
        pass

    def initComponents(self):
        #initialize components (model,view,self)
        logging.info("Controller init done")
        pass

    def loop(self):
        #main game loop is started from here
        while(True):
            print("Hallo")
            time.sleep(5)


    #todo remove: example function for unit test
    def someFunc(self,a,b):
        return (a + b)
