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

bool is_balanced(string p) {
    vector<char> stack;
    char open = '(';
    for(int i = 0; i < p.size(); i++) {
        if(p[i] == open)
           stack.push_back((char)p[i]);
        else {
            if(stack.empty())
                return false;
            stack.pop_back();
        }
    }

    if(stack.empty())
        return true;
    else
        return false;
}

string transform(string p) {
    string new_p;
    for(int i = 1; i < p.size() - 1; i++) {
        if((char)p[i] == '(')
            new_p = new_p + ")";
        else
            new_p = new_p + "(";
    }
    return new_p;
}

string split_to_uv(string p) {
    if(!p.size() || is_balanced(p))
        return p;

    int cnt = 0;
    int i;
    char open = '(';
    string u = "";
    string v = "";
    for(i = 0; i < p.size(); i++) {
        if(i && cnt == 0)
            break;
        if((char)p[i] == open)
            cnt++;
        else
            cnt--;
    }

    u = p.substr(0, i);
    v = p.substr(i, p.size()-i);

    if(is_balanced(u))
        return u + split_to_uv(v);
    else {
        return "(" + split_to_uv(v) + ")" + transform(u);
    }


    return split_to_uv(u) + split_to_uv(v);
    //return u + v;
}

string solution(string p) {
    if(is_balanced(p))
        return p;
    return split_to_uv(p);
}

int main() {
    //string a = solution("()))((()");
    //string a = solution("(()())()");
    string t1 = "(()())()";
    string t2 = ")(";
    string t3 = "()))((()";

    cout << solution(t1) << endl;
    cout << solution(t2) << endl;
    cout << solution(t3) << endl;

    //cout << is_balanced("(())(())") << endl;
    //string a = solution("))((");
    return 0;
}
