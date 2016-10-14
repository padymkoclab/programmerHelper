
#include <iostream>
#include <iterator>
#include <initializer_list>

using namespace std;


int len(const initializer_list<int>& array){

    int len = 0;

    for (auto x : array)
        len ++;

    return len;
}


int max(int *numbers){

    int max = -99999;
    int number;

    for (int i = 0; i < 10; i++) {
        number = numbers[i];
        if (max == -99999){
            max = number;
        } else if (number > max) {
            max = number;
        }
    }

    return max;

}


int min(int *numbers){

    int min = -99999;
    int number;

    for (int i = 0; i < 10; i++) {
        number = numbers[i];
        if (min == -99999){
            min = number;
        } else if (number < min) {
            min = number;
        }
    }

    return min;

}


int sum(int *numbers){

    int sum = 0;

    for (int i = 0; i < 10; i++) {
        sum += numbers[i];
    }

    return sum;

}

int main(){

    int array [] = {2, 3, 0, 7, -7, -79, -14, 89, 0, 0};

    cout << "Length: " << len({2, 3, 0, 7, -7, -79, -14, 89, 0, 0}) << endl;
    cout << "Max: "<< max(array) << endl;
    cout << "Min: " << min(array) << endl;
    cout << "Sum: " << sum(array) << endl;

    return false;

}
