import os
import logging
import sys
import cppyy

from controller.Controller import Controller

from network.LibClientHandler import LibClientHandler

cppyy.load_library("libSopraClient")
cppyy.load_library("libSopraCommon")
cppyy.load_library("libSopraNetwork")

cppyy.add_include_path("extern/LibClient/src")
cppyy.add_include_path("extern/LibClient/extern/LibCommon/src")

cppyy.include("datatypes/gadgets/Gadget.hpp")
cppyy.include("datatypes/gadgets/Cocktail.hpp")
cppyy.include("util/Point.hpp")
cppyy.include("datatypes/matchconfig/MatchConfig.hpp")

gadget = cppyy.gbl.spy.gadget.Gadget()
gadget.setUsagesLeft(3)
usagesleft = gadget.getUsagesLeft()
print("UsagesLeft", usagesleft)

cocktail = cppyy.gbl.spy.gadget.Cocktail()
cocktail.setIsPoisoned(True)
if cocktail.isPoisoned():
    print("The ocktail was poisoned")



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
