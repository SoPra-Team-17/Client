import os
import logging
import sys
import cppyy

from controller.Controller import Controller

cppyy.load_library("libSopraClient")
cppyy.load_library("libSopraCommon")
cppyy.load_library("libSopraNetwork")

cppyy.add_include_path("extern/LibClient/src")

cppyy.include("LibClient.hpp")

#obj_cpp = cppyy.gbl.LibClient()
#micro = cppyy.gbl.std.chrono.microseconds



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


def main():
    #os.environ['SDL_VIDEODRIVER'] = 'x11'
    #os.environ['DISPLAY'] = '127.0.0.1:0'

    init_logging()

    #create main controller
    controller = Controller()
    controller.init_components()
    controller.loop()



if __name__ == "__main__":
    main()
