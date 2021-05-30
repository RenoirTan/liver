#include <iostream>
#include <vector>

using namespace std;

bool isValidOp(char op) {
    switch (op) {
        case '+':
        case '-':
        case '*':
        case '/':
            return true;
        default:
            return false;
    }
}

typedef int (*IntOperation)(int, int);

int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int multiply(int a, int b) {
    return a * b;
}

int divide(int a, int b) {
    return a / b;
}

IntOperation getOperator(char op) {
    switch (op) {
        case '+':
            return add;
        case '-':
            return subtract;
        case '*':
            return multiply;
        case '/':
            return divide;
        default:
            return nullptr;
    }
}

template <class T>
T reduce_vector(vector<T> &vec, T (*opfunc)(T, T)) {
    if (!vec.size()) {
        return T();
    }
    T acc = vec[0];
    for (auto it = vec.begin() + 1; it != vec.end(); it++) {
        acc = opfunc(acc, *it);   
    }
    return acc;
}

int main(int argc, char **argv) {
    vector<int> numbers;
    char operation;
    int n, input, result;
    cout << "Operation: ";
    cin >> operation;
    cout << "Number of integers: ";
    cin >> n;
    if (!isValidOp(operation)) {
        cerr << "Operation must be one of the following: +-*/";
        return 1;
    }
    cout << "Enter numbers below.\n";
    for (int _i = 0; _i < n; _i++) {
        cin >> input;
        numbers.push_back(input);
    }
    result = reduce_vector(numbers, getOperator(operation));
    cout << "Result: " << result;
    return 0;
}