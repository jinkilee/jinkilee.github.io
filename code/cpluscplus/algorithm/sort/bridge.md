문제 설명
---------------------
트럭 여러 대가 강을 가로지르는 일 차선 다리를 정해진 순으로 건너려 합니다. 모든 트럭이 다리를 건너려면 최소 몇 초가 걸리는지 알아내야 합니다. 트럭은 1초에 1만큼 움직이며, 다리 길이는 bridge_length이고 다리는 무게 weight까지 견딥니다.
※ 트럭이 다리에 완전히 오르지 않은 경우, 이 트럭의 무게는 고려하지 않습니다.

예를 들어, 길이가 2이고 10kg 무게를 견디는 다리가 있습니다. 무게가 [7, 4, 5, 6]kg인 트럭이 순서대로 최단 시간 안에 다리를 건너려면 다음과 같이 건너야 합니다.

경과 시간	다리를 지난 트럭	다리를 건너는 트럭	대기 트럭
0	[]	[]	[7,4,5,6]
1~2	[]	[7]	[4,5,6]
3	[7]	[4]	[5,6]
4	[7]	[4,5]	[6]
5	[7,4]	[5]	[6]
6~7	[7,4,5]	[6]	[]
8	[7,4,5,6]	[]	[]
따라서, 모든 트럭이 다리를 지나려면 최소 8초가 걸립니다.

solution 함수의 매개변수로 다리 길이 bridge_length, 다리가 견딜 수 있는 무게 weight, 트럭별 무게 truck_weights가 주어집니다. 이때 모든 트럭이 다리를 건너려면 최소 몇 초가 걸리는지 return 하도록 solution 함수를 완성하세요.

제한 조건
---------------------
bridge_length는 1 이상 10,000 이하입니다.
weight는 1 이상 10,000 이하입니다.
truck_weights의 길이는 1 이상 10,000 이하입니다.
모든 트럭의 무게는 1 이상 weight 이하입니다.

입출력 예
---------------------
bridge_length	weight	truck_weights	return
2	10	[7,4,5,6]	8
100	100	[10]	101
100	100	[10,10,10,10,10,10,10,10,10,10]	110


코드
---------------------
```cpp
#include <string>
#include <vector>
#include <queue>
#include <iostream>

using namespace std;

void print_array(int* time, int n_truck) {
    for(int i = 0; i < n_truck; i++)
        cout << time[i] << " ";
    cout << endl;
}
void print_queue(queue<int> q) {
    while(!q.empty()) {
        cout << q.front() << " ";
        q.pop();
    }
    cout << endl;
}

//*/
int solution(int bridge_length, int weight, vector<int> truck_weights) {
    int answer = 0;
	queue<int> times, passing;
    int sum = 0;
    int idx = 0;
    for(int i = 1; ; i++) {
        //cout << "current time: " << i << endl;
        if(times.size() > 0) {
            if(i - times.front() == bridge_length) {
                //cout << "before pop, times: ";
                //print_queue(times);
                //cout << "before pop, queue: ";
                //print_queue(passing);
                answer = bridge_length + times.front();
                times.pop();
				//cout << "before pop, sum: " << sum << endl;
                sum -= passing.front();
				//cout << "after pop, sum: " << sum << endl;
                passing.pop();
				if((idx == truck_weights.size()) && passing.size() == 0) {
                    return answer;
                }
            }
        }
		while(1) {
            // if heavier -> break
            // if lighter or equal -> load truck and idx++
            if(sum + truck_weights[idx] > weight || idx == truck_weights.size()) {
                //cout << "all trucks were already loaded" << endl;
                break;
            }
            else {
                passing.push(truck_weights[idx]);
                times.push(i);
                //cout << "after pushing, passing: ";
                //print_queue(passing);
                //cout << "after pushing, times: ";
                //print_queue(times);
                //cout << "sum: " << sum << endl;
                sum += truck_weights[idx];
                //cout << "sum: " << sum << endl;
                idx++;
               	break;
            }
            
        }
        //cout << "----------------" << endl;
    }
    return answer;
}
//*/
```
