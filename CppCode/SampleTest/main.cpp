#include <SampleLibrary/Network.hpp>
#include <SampleLibrary/CallbackClass.hpp>
#include <SampleLibrary/Model.hpp>

#include <iostream>

class CppCallback: public CallbackClass {
public:

    CppCallback() = default;

    Model model = Model();

    void receivedGetText() {
        std::cout << "CppCallback" << std::endl;
        model.printText();
        std::cout << "CppCallback" << std::endl;
    };
};

int main() {
    CppCallback callback;
    Network network = Network(&callback, &callback.model);

    network.sentSetText("HalloSopraTeam");
    network.receivedGetText();

    return 0;
}

