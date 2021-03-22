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

string solution(string number, int k) {
    string answer = "";
    int n = number.size() - k;
    int start = 0;
    for(int i = 0; i < n; i++) {
        int maxidx = start;
        int maxnum = number[maxidx] - '0';
        for(int j = start; j <= k+i; j++) {
            if(number[j]-'0' > maxnum) {
                maxidx = j; 
                maxnum = number[j] - '0';
            }
        }
        start = maxidx + 1;
        answer += to_string(maxnum);
    }
    return answer;
}

int main() {
    string answer = solution("1924", 2);    // 94
    //string answer = solution("1231234", 3);    // 3234
    //string answer = solution("4177252841", 4);    // 775841
    cout << answer << endl;
    return 0;
}
