#ifndef SAMPLELIBRARY_LIBRARY_H
#define SAMPLELIBRARY_LIBRARY_H

#include <string>
#include <iostream>


class Model {
public:

    Model() {
        text = "init";
    }

    std::string text;

    void setText(std::string t);

    void printText();

};

#endif //SAMPLELIBRARY_LIBRARY_H