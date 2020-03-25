#include "library.h"

#include <iostream>

void printTestClass(TestClass tc) {
    tc.printText();
}

void TestClass::setText(std::string t) {
    this->text = t;
}

std::string TestClass::getText() {
    return this->text;
}

void TestClass::printText() {
    std::cout << this->text << std::endl;
}