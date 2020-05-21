문제 설명
------------
온라인으로 티켓 예매를 하기 위해 많은 이용자가 홈페이지의 예매 버튼을 클릭하였고, 예매 대기열이 생성되었습니다. 이때 예매 버튼을 여러 번 중복하여 클릭한 이용자들에 의해 예매 대기열에 여러 번 중복해서 등록된 이용자들이 있게 되었습니다. 사이트 관리자는 현재까지 생성된 예매 대기열에서 중복등록 된 이용자는 가장 앞쪽에 등록된 대기 하나만 인정하고, 나머지는 대기열에서 제거하려 합니다. 다음은 현재까지 생성된 예매 대기열에서 중복으로 등록된 이용자를 제거하는 예시입니다.

위 예시에서 각 숫자는 이용자의 ID 번호를 나타내며 왼쪽부터 순서대로 대기열에 등록된 상태입니다. 이때, 5번 이용자의 경우 ②번째와 ⑥번째 대기열에 중복으로 등록되어있기 때문에 ②번째에 위치한 대기만 인정되고, ⑥번째에 등록된 대기는 제거해야 합니다. 마찬가지로 8번 이용자의 경우 ③번째, ⑩번째에 중복으로 등록되었으며, ⑩번째에 위치한 대기는 제거해야 합니다. 마지막으로 4번 이용자의 경우 ⑦번째, ⑨번째에 중복등록 되어있으며, ⑨번째 대기는 제거되어야 합니다. 중복으로 등록된 이용자를 제거한 새로운 대기열은 아래 그림과 같습니다.

현재 생성된 예매 대기열의 상태가 담긴 배열 waiting이 매개변수로 주어질 때, 중복으로 등록된 이용자를 제거한 결과를 배열 형태로 return 하도록 solution 함수를 완성해주세요.

제한사항
------------
waiting은 현재 생성되어있는 예매 대기열이 담겨있는 배열이며, 길이는 1 이상 200,000 이하입니다.
waiting의 각 원소는 이용자의 ID이며, 예매 대기열에 등록된 순서대로 들어있습니다.
이용자의 ID는 1 이상 20억 이하의 자연수입니다.

입출력 예
------------
```
waiting	result
[1, 5, 8, 2, 10, 5, 4, 6, 4, 8]	[1, 5, 8, 2, 10, 4, 6]
[5, 4, 4, 3, 5]	[5, 4, 3]
```

입출력 예 설명
------------
입출력 예 #1
문제의 예시와 같습니다.

입출력 예 #2
------------
5와 4번 이용자가 각각 중복 등록되어있기 때문에 나중에 등록된 아이디를 대기열에서 삭제하면 대기열은 [5, 4, 3]이 됩니다.

코드
------------
```cpp
#include <vector>
#include <iostream>
#include <algorithm>
#include <set>

using namespace std;

void print_set(set<int> myset) {
    set<int>::iterator it;
    for (it = myset.begin(); it != myset.end(); ++it)
        cout << *it << " ";
    cout << endl;
}

void print_vector(vector<int> vec) {
    for(auto v: vec)
        cout << v << " ";
    cout << endl;
}

vector<int> solution(vector<int> waiting)
{
    vector<int> answer;
    set<int> waiting_set;
    set<int>::iterator it;
    
    for(int i = 0; i < waiting.size(); i++) {
        if(waiting_set.find(waiting[i]) == waiting_set.end()) {
            waiting_set.insert(waiting[i]);
            answer.push_back(waiting[i]);
        }
    }
    //print_set(waiting_set);
    //print_vector(answer);
    return answer;
}
```
