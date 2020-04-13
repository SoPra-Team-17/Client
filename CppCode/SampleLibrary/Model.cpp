#include "Model.hpp"

void Model::setText(std::string t) {
    this->text = t;
}

void Model::printText() {
    std::cout << this->text << std::endl;
}