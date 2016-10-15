
#include <iostream>
#include <vector>


int len(std::vector<int> array){
    return array.size();
}

int max(std::vector<int> array){
    int max = array.front();
    for (int i = 0; i < len(array); i++) {
        if (array[i] > max){
            max = array[i];
        }
    }
    return max;
}


int min(std::vector<int> array){
    int min = array.front();
    for (int i = 0; i < len(array); i++) {
        if (array[i] < min){
            min = array[i];
        }
    }
    return min;
}


int sum(std::vector<int> array){
    int sum = 0;
    for (int i = 0; i < len(array); i++) {
        sum += array[i];
    }
    return sum;
}



int main(){

    std::vector<int> array = {2, 3, 0, 7, -7, -79, -14, 89, 0, 0, -8};

    std::cout << "Length: " << len(array) << std::endl;
    std::cout << "Max: "<< max(array) << std::endl;
    std::cout << "Min: " << min(array) << std::endl;
    std::cout << "Sum: " << sum(array) << std::endl;

    return false;

}
