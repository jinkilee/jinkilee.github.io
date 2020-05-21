문제 설명
------------
중고차 딜러는 중고차를 사고 팔아 이익을 내려고 합니다. 중고차는 매일매일 가격이 변합니다. 중고차를 사거나 팔려고 할 때는 그 날의 중고차 가격으로만 거래할 수 있습니다. 또, 중고차는 주어진 기간동안 단 한 번만 구매 후 판매할 수 있습니다.
n일 동안의 중고차 가격이 들어있는 배열(prices)이 입력으로 주어질 때 얻을 수 있는 최대 이익을 return 하도록 solution 함수를 완성해 주세요. 배열의 i번째 요소는 i번째 날의 중고차 가격을 나타냅니다. 예를 들어 5일간 중고차의 가격이 [3, 2, 4, 8, 7] 인 경우 2원에 중고차를 구매하여 이틀 후 8원에 팔면 6의 이익이 발생하고, 이때 최대 이익을 얻을 수 있습니다. 단, 이익이 발생하지 않을 때는 중고차를 구매하지 않을 수도 있으며, 이때는 0을 return 합니다.

제한사항
------------
중고차 가격이 들어있는 배열(prices)의 크기 : 100,000 이하인 자연수
중고차 가격 : 1,000,000 이하인 자연수

입출력 예
------------
```
prices	answer
[3, 2, 4, 8, 7]	6
[3, 4, 1, 5, 4]	4
```

입출력 예 설명
------------
입출력 예 #1
문제의 예시와 같습니다.

입출력 예 #2
3번째 날에 1원에 구매한 뒤, 다음 날 5원으로 팔면 4의 이익이 발생하는데, 이때 최대 이익을 얻을 수 있습니다.

코드
```cpp
#include <vector>
#include <iostream>
#include <queue>

using namespace std;

void print_queue(priority_queue<int> q) {
    while(!q.empty()) {
        cout << q.top() << " ";
        q.pop();
    }
    cout << endl;
}

void print_queue(priority_queue<int, vector<int>, greater<int>> q) {
    while(!q.empty()) {
        cout << q.top() << " ";
        q.pop();
    }
    cout << endl;
}
void print_vector(vector<int> vec) {
    for(auto v: vec)
        cout << v << " ";
    cout << endl;
}

int solution(vector<int> prices)
{
	int answer = 6;
    int n_prices = prices.size();
	priority_queue< int, vector<int>, greater<int> > minq;    
    priority_queue<int> maxq;

    int start = 0;
    int end = prices.size() - 1;
    while(start != end) {
        minq.push(prices[start]);
        maxq.push(prices[end]);
        start++;
        end--;
    }
    minq.push(prices[start]);
    maxq.push(prices[end]);
    
    answer = maxq.top() - minq.top();
	return answer;
}
```
