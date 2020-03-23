import logging
import sys
from controller.Controller import Controller


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
    init_logging()
    #logging examples
    logging.info("Info output")
    logging.debug("Debug output")
    logging.warning("Warning output")
    logging.error("Error output")
    logging.critical("Critical output")

    #create main controller
    controller = Controller()
    controller.init_components()
    controller.loop()



if __name__ == "__main__":
    main()
