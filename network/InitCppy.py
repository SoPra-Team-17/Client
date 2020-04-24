import cppyy

def init_cppyy():
    cppyy.load_library("SopraClient")
    cppyy.load_library("SopraCommon")
    cppyy.load_library("SopraNetwork")
