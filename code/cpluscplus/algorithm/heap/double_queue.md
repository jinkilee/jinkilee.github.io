




코드
----------------
```cpp
// my solution
vector<int> solution(vector<string> operations) {
    vector<int> answer;
    
    int num, min;
    int n_min_delete = 0;
    int n_max_delete = 0;
    int n_pop_to_last;
    string code;
    priority_queue<int> doubleq;

    for(int i = 0; i < operations.size(); i++) {
        code = operations[i].substr(0, 1);
        num = stoi(operations[i].substr(2, operations[i].length()-2));
        if(code.compare("I") == 0)
            doubleq.push(num);
        else if(code.compare("D") == 0) {
            if(num == 1) {
                if((doubleq.size() - n_min_delete) == 0)
                    continue;
                n_max_delete++;
                doubleq.pop();
            }
            else {
                if(doubleq.size() != 0)
                    n_min_delete++;
            }
        }
    }
    
    // make answer
    int size = doubleq.size() - n_min_delete;
    if(size <= 0 || doubleq.empty()) {
        answer.push_back(0);
        answer.push_back(0);
    }
    else {
        answer.push_back(doubleq.top());
        n_pop_to_last = doubleq.size() - n_min_delete;
        while(n_pop_to_last--) {
            min = doubleq.top();
            doubleq.pop();
        }
        answer.push_back(min);
    }
    return answer;
}
```

```cpp
// someone's solution
#include <set>
vector<int> solution(vector<string> arguments) {
    vector<int> answer;
    multiset<int> que;
    multiset<int>::iterator iter;
    string sub;

    for(auto s : arguments) {
        sub =s.substr(0, 2);
        if(sub=="I ") que.insert(stoi(s.substr(2,s.length()-2))); 
        else if(s.substr(2,1)=="1"&&que.size()>0) { que.erase(--que.end()); }
        else if(que.size()>0) { que.erase(que.begin()); }
    }

    if(que.size()==0) { answer.push_back(0); answer.push_back(0); }
    else { 
        iter = --que.end(); answer.push_back(*iter); 
        iter = que.begin(); answer.push_back(*iter);
    }

    return answer;
}
```
