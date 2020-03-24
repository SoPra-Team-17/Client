#ifndef SAMPLELIBRARY_LIBRARY_H
#define SAMPLELIBRARY_LIBRARY_H

#include <string>


class TestClass {
public:

    TestClass() {
        text = "init";
    }

    std::string text;

    void setText(std::string t);

    std::string getText();

    void printText();

};

void printTestClass(TestClass tc);

#endif //SAMPLELIBRARY_LIBRARY_H