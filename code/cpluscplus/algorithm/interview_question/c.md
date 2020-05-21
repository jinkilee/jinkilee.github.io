문제 설명
-------------
○○피자집은 손님이 피자를 한 번 살 때마다 쿠폰 1장을 줍니다. 이 쿠폰을 3장 모으면 다음 주문 때 스파게티를 무료로 받습니다. (쿠폰을 2개 갖고 있을 때 피자를 주문하면 새 쿠폰을 받아 쿠폰이 3개이지만, 이 상황에서는 쿠폰을 쓸 수 없습니다) 무료로 스파게티를 받았을 때는 피자를 사도 쿠폰을 주지 않으며, 손님은 쿠폰을 4개 이상 모을 수 없습니다.

예를 들어, [1,3,3,2,4,3,3,2,4,2,2,4] 순으로 주문했다고 가정해봅시다. 괄호 안의 숫자는 손님 고유의 ID를 나타내며, 왼쪽부터 순서대로 주문한 것을 나타냅니다.
이를 표로 나타내어 첫 번째 행을 손님 고유의 ID, 두 번째 행을 해당 손님의 쿠폰 개수라 하면 다음과 같습니다.

이 경우엔 3번 손님, 2번 손님은 스파게티를 무료로 받습니다. 4번 손님은 쿠폰 3장을 모았지만, 이 쿠폰은 다음번 피자를 주문할 때 쓸 수 있습니다.

피자를 산 손님들의 ID가 매개변수 people로 주어졌을 때, 스파게티를 무료로 받은 손님들의 ID를 return 하는 solution 함수를 완성해 주세요. 예를 들어, 위의 예시에서는 3번 손님, 2번 손님 순으로 스파게티를 무료로 받았기 때문에 답은 [3,2]입니다. 단, 어떠한 손님도 스파게티를 무료로 받지 못한 경우에는 1차원 배열에 -1을 넣어서 return 해주세요.

제한사항
-------------
people의 길이 : 100,000 이하의 자연수
손님 ID : 1,000,000,000 이하의 자연수

입출력 예
-------------
```
people	answer
[1,3,3,2,4,3,3,2,4,2,2,4]	[3,2]
[1,1,3,3,3,3,1,3,3,3,3,2]	[3,3]
[1,2,3,4]	[-1]
```

입출력 예 설명
-------------
입출력 예 #1
문제의 예시와 같습니다.

입출력 예 #2
-------------
3번 손님이 두 번 연속으로 스파게티를 받았습니다.

입출력 예 #3
-------------
어떠한 손님도 스파게티를 무료로 받지 못한 경우입니다.


코드
```cpp
#include <vector>
#include <iostream>
#include <unordered_map>
using namespace std;

void print_vector(vector<int> vec) {
    for(auto v: vec)
        cout << v << " ";
    cout << endl;
}

void print_map(unordered_map<int, int> mymap) {
    for (auto it = mymap.begin(); it != mymap.end(); ++it)
        cout << it->first << ":" << it->second << " ";
    cout << endl;
}

vector<int> solution(vector<int> people) {
    vector<int> answer;
    unordered_map<int, int> coupons;
    for(int i = 0; i < people.size(); i++) {
        if(coupons.find(people[i]) == coupons.end()) {
            coupons.insert({people[i], 1});
        }
        else {
            if(coupons[people[i]] == 3) {
                coupons[people[i]] = 0;
                answer.push_back(people[i]);
                continue;
            }
            coupons[people[i]]++;
        }
    }
    if(answer.size() == 0)
        answer.push_back(-1);
    return answer;
}
```
