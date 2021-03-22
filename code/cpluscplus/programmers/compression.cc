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

int minlen(string s, int jump) {
    int answer = 0;
    int dup = 1;
    string pivot = s.substr(0, jump);
    string comp;
    vector<int> dstack;
    vector<string> cstack;
    for(int i = jump; i < s.size(); i+=jump) {
        //*/
        comp = s.substr(i, jump);
        //cout << pivot << " " << comp << endl;
        if(pivot == comp) {
            dup++;
        }
        else {
            dstack.push_back(dup);
            cstack.push_back(pivot);
            dup = 1;
            pivot = comp;
        }
    }
    dstack.push_back(dup);
    cstack.push_back(comp);

    //cout << "------------------------------" << endl;
    int enclen = 0;
    int ndigit;
    int temp;
    for(int i = 0; i < dstack.size(); i++) {
        if(dstack[i] != 1) {
            temp = dstack[i];
            ndigit = 1;
            while(temp/10) {
                temp /= 10;
                ndigit++;
            }
            //cout << dstack[i] << " " << ndigit << endl;
            enclen += ndigit;
        }
        enclen += cstack[i].size();
    }
    //cout << "------------------------------" << endl;
    //print_vector(dstack);
    //print_vector(cstack);
    //cout << enclen << endl;
    return enclen;
}

int solution(string s) {
    vector<int> length;
    for(int i = 1; i < s.size(); i++) {
        length.push_back(minlen(s, i));
    }
    length.push_back(s.size());
    //print_vector(length);
    return *min_element(length.begin(), length.end());
}

// "aabbaccc" -> 2a2ba3c -> 7
// "aaaaaaaaaaaabbbbbbbbbbbb" -> 12a12b -> 6
// "aaabbbacccc" -> 3a3ba4c -> 7
// "aaaaaaaaaaaabbbbbbcc" -> 12a6b2c -> 7
int main() {
    int result;
    cout << rand() << endl;
    return 0;
}
