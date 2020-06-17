문제 설명
--------------
매달 k 일은 아파트 관리비를 내는 날입니다. 만약 그달의 k 일이 주말(토요일, 일요일)이라면 관리비는 k 일로부터 가장 가까운 평일에 냅니다. 한 해의 시작일인 1월 1일에 해당하는 요일 day와 매달 관리비를 내야 하는 날짜 k가 매개변수로 주어질 때, 그해의 1월부터 12월까지 매달 k 일이 평일이면 0을, 주말이면 1을 순서대로 배열에 담아 return 하도록 solution 함수를 완성해주세요.

제한사항
--------------
1월 1일에 해당하는 요일은 다음과 같이 숫자로 주어집니다.
월요일: 0, 화요일: 1, 수요일: 2, 목요일: 3, 금요일: 4, 토요일: 5, 일요일: 6
k는 1 이상 28 이하의 자연수입니다.
각 달의 날짜 수는 1월부터 순서대로 [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] 이며, 윤년과 공휴일은 고려하지 않습니다.

입출력 예
--------------
```
day	k	result
6	1	[1,0,0,1,0,0,1,0,0,1,0,0]
6	25	[0,1,1,0,0,1,0,0,0,0,1,0]
```

입출력 예 설명
--------------
- 입출력 예 #1
```
이 예시에서 1월 1일은 일요일이고, 매달 1일에 관리비를 내야 합니다. 1월 1일은 주말이므로 result 배열의 첫 번째 원소는 1입니다. 2월부터 12월까지 매달 1일에 해당하는 요일은 다음과 같습니다.

2월: 수요일
3월: 수요일
4월: 토요일
5월: 월요일
6월: 목요일
7월: 토요일
8월: 화요일
9월: 금요일
10월: 일요일
11월: 수요일
12월: 금요일
따라서 1월부터 순서대로 [1,0,0,1,0,0,1,0,0,1,0,0]을 return 하면 됩니다.
```

- 입출력 예 #2
```
이 예시에서 1월 1일은 일요일이고, 매달 25일에 관리비를 내야 합니다. 1월 25일은 수요일이므로 result 배열의 첫 번째 원소는 0입니다. 마찬가지로 2월~12월까지 매달 25일에 해당하는 요일은 2월부터 순서대로 토요일, 토요일, 화요일, 목요일, 일요일, 화요일, 금요일, 월요일, 수요일, 토요일, 월요일입니다. 따라서 1월부터 순서대로 [0,1,1,0,0,1,0,0,0,0,1,0]을 return 하면 됩니다.
```


코드
-------------
```cpp
#include <string>
#include <vector>
#include <map>
#include <iostream>

using namespace std;

void print_vector(vector<int> vec) {
    for(int i = 0; i < vec.size(); i++)
        cout << vec[i] << " ";
    cout << endl;
}

vector<int> solution(int day, int k) {
    vector<int> answer;
    map<int, int> mmap;
    
    mmap[1] = 31;
    mmap[2] = 28;
    mmap[3] = 31;
    mmap[4] = 30;
    mmap[5] = 31;
    mmap[6] = 30;
    mmap[7] = 31;
    mmap[8] = 31;
    mmap[9] = 30;
    mmap[10] = 31;
    mmap[11] = 30;
    mmap[12] = 31;
    
    int maxdate;
    int firstday = day;
	int kday;
    for(int i = 1; i <= 12; i++) {
        maxdate = mmap[i];
        kday = (firstday + k - 1) % 7;
        firstday = (kday + (maxdate-k) + 1) % 7;
        //cout << "month:" << i << " maxday:" << mmap[i] << " " << "kday:" << kday << endl;
        //cout << "next firstday:" << firstday << endl;
        //break;
        
        if(kday < 5)
            answer.push_back(0);
        else
            answer.push_back(1);
    }
    return answer;
}
```
