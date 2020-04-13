#include <iostream>
#include <SampleLibrary/Network.hpp>
#include <SampleLibrary/CallbackClass.hpp>
#include <SampleLibrary/Model.hpp>

int main() {
    Model model;
    CallbackClass callback;
    Network network = Network(callback, model);

    network.sentSetText("HalloSopra");
    network.receivedGetText();

    return 0;
}

