"""
Initializes cppyy
"""
import cppyy

__author__ = "Marco Deuscher"
__date__ = "20.05.2020 (doc creation)"


def init_cppyy() -> None:
    """"
    Initzializes cppyy
    Sets path to library and loads the shared libs
    """
    cppyy.add_library_path("/usr/local/lib")

    cppyy.load_library("SopraClient")
    cppyy.load_library("SopraCommon")
    cppyy.load_library("SopraNetwork")
