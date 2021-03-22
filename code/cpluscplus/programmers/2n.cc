#include <iostream>
#include <stdlib.h>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

void print_vector(vector<string> vec) {
    for(int i = 0; i < vec.size(); i++)
        cout << vec[i] << " ";
    cout << endl;
}

void print_vector(vector<int> vec) {
    for(int i = 0; i < vec.size(); i++)
        cout << vec[i] << " ";
    cout << endl;
}


int solution(int n) {
    vector<int> answer;
    answer.push_back(1);
    answer.push_back(2);
    for(int i = 2; i < n; i++) {
        answer.push_back((answer[i-1] + answer[i-2])%1000000007);
    }
    cout << answer.size() << endl;

    //cout << "n: " << n << endl;
    //cout << "n_stack_row: " << n_stack_row << endl;
    //cout << "n_stack_col: " << n_stack_col << endl;
    //cout << "---------------" << endl;
    return answer[answer.size()-1]%1000000007;
}

int main() {
    int a;
    //a = solution(1);
    //a = solution(3);
    //a = solution(4);
    a = solution(5);
    cout << "a: " << a << endl;
    return 0;
}
