#include <iostream>
#include <string>
#include <vector>

using namespace std;

void print_vector(vector<int> vec) {
    for(int i = 0; i < vec.size(); i++)
        cout << vec[i] << " ";
    cout << endl;
}

vector<int> solution(vector<int> prices) {
    vector<int> answer;
    int n_prices = prices.size();
    int lidx = 0;
    int ridx = n_prices - 1;

    for(int i = 0; i < n_prices; i++) {
        if(lidx >= ridx) {
            cout << lidx << "," << ridx << endl;
            cout << "ridx: " << ridx << " -> target: " << ridx-1 << endl;
            break;
        }
        cout << lidx << "," << ridx << endl;
        cout << "lidx: " << lidx << " -> target: " << lidx << endl;
        cout << "ridx: " << ridx << " -> target: " << ridx-1 << endl;
        lidx++;
        ridx--;
    }
    return answer;
}

vector<int> solution_1(vector<int> prices) {
    vector<int> answer;
    vector<int> tq;
    int n_prices = prices.size();

    // initialize answer
    for(int i = 0; i < n_prices; i++) {
        answer.push_back(0);
    }

    // write answers only when observing decreased stock prices
    int t;
    for(int i = 0; i < n_prices; i++) {
        while(!tq.empty() && prices[tq.back()] > prices[i]) {
            //cout << i << " " << prices[i] << endl;
            t = tq.back();
            tq.pop_back();
            answer[t] = i - t;            
        }
        tq.push_back(i);
        //print_vector(tq);
    }

    // write answers for the rest
    while(!tq.empty()) {
        t = tq.back();
        answer[t] = n_prices - t - 1;
        tq.pop_back();
    }

    print_vector(answer);
    return answer;
}

int main() {
    vector<int> result;
    vector<int> prices;

    prices.push_back(1);
    prices.push_back(2);
    prices.push_back(3);
    prices.push_back(2);
    prices.push_back(3);

    result = solution(prices);
    return 0;
}
