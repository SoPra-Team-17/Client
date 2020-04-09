#include <iostream>
#include <SampleLibrary/library.h>

int main() {
    std::string text;

    TestClass tc = TestClass();
    text = tc.getText();
    std::cout<<text<<std::endl;
    tc.printText();
    printTestClass(tc);

    tc.setText("abc");
    text = tc.getText();
    std::cout<<text<<std::endl;
    tc.printText();
    printTestClass(tc);

    tc.text = "def";
    text = tc.getText();
    std::cout<<text<<std::endl;
    tc.printText();
    printTestClass(tc);

    return 0;
}

