"""
Initializes logging and cppyy. Creates Controller and enters main loop
"""
import logging
import sys
import argparse

from controller.Controller import Controller
from network.InitCppyy import init_cppyy

__author__ = "Marco"
__date__ = "25.04.2020 (date of doc. creation)"


def init_logging(log_level):
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

    rootLogger.setLevel(log_level * 10)


def main():
    # os.environ['SDL_VIDEODRIVER'] = 'x11'
    # os.environ['DISPLAY'] = '127.0.0.1:0'

    parser = argparse.ArgumentParser(description="Run script for No Time to Spy Client")
    parser.add_argument("--verbosity", "-v", default=1, choices=range(0, 6), type=int,
                        help="5=critical, 4=error, 3=warning, 2=info, 1=debug, 0=notset")
    args = parser.parse_args()

    init_cppyy()
    init_logging(args.verbosity)

    # create main controller
    controller = Controller()
    controller.init_components()
    controller.loop()


if __name__ == "__main__":
    main()
