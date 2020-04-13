import os
import logging
import sys
from controller.Controller import Controller

import cppyy
cppyy.load_library('SampleLibrary')
cppyy.include('SampleLibrary/Network.hpp')
cppyy.include('SampleLibrary/Model.hpp')
cppyy.include('SampleLibrary/CallbackClass.hpp')


def init_logging():
    formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s]"
        " [%(levelname)-8.8s] "
        "[%(filename)-20.20s - %(funcName)-20.20s - %(lineno)-4.4s]"
        " %(message)s")
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler("out.log")
    fileHandler.setFormatter(formatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(formatter)
    rootLogger.addHandler(consoleHandler)

    rootLogger.setLevel(logging.DEBUG)


class PythonCallbackClass(cppyy.gbl.CallbackClass):
    def setModel(self):
        self.model = cppyy.gbl.Model()

    def receivedGetText(self):
        print("Python Callback")
        self.model.printText()
        print("Python Callback")


def callbackTest():
    callback = PythonCallbackClass()
    callback.setModel()
    network = cppyy.gbl.Network(callback, callback.model)

    network.sentSetText("HalloSopra")
    network.receivedGetText()


def main():
    callbackTest()
    #os.environ['SDL_VIDEODRIVER'] = 'x11'
    #os.environ['DISPLAY'] = '127.0.0.1:0'

    init_logging()
    #logging examples
    logging.info("Info output")
    logging.debug("Debug output")
    logging.warning("Warning output")
    logging.error("Error output")
    logging.critical("Critical output")


    #create main controller
    #controller = Controller()
    #controller.init_components()
    #controller.loop()


if __name__ == "__main__":
    main()

