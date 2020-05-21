문제 설명
--------------
프로그래밍 대회 참가 팀을 추가로 모집하려고 합니다. 추가로 참가하는 팀들의 팀 아이디를 등록하기 위해 각 팀으로부터 대회에 사용할 아이디를 순서대로 신청받았습니다. 단, 기존에 등록되어있는 아이디는 사용할 수 없으며, 두 팀 이상이 같은 아이디를 신청할 경우, 먼저 신청한 팀에 우선권이 있습니다. 예를 들어 이미 등록이 완료된 팀 아이디 목록은 [world, prog], 추가로 등록 신청을 받은 팀 아이디의 순서는 [hello, world, code, hello, try, code]일 때, 추가 등록 팀의 아이디가 등록되는 순서는 다음과 같습니다.

첫 번째로 신청받은 hello는 팀 아이디로 등록됩니다.
두 번째로 신청받은 world는 이미 등록된 아이디이므로 등록되지 않습니다.
세 번째로 신청받은 code는 팀 아이디로 등록됩니다.
네 번째로 신청받은 hello는 이미 등록된 아이디이므로 등록되지 않습니다.
다섯 번째로 신청받은 try는 팀 아이디로 등록됩니다.
여섯 번째로 신청받은 code는 이미 등록된 아이디이므로 등록되지 않습니다.
따라서 추가로 등록되는 아이디는 등록이 완료된 순서대로 [hello, code, try]가 됩니다.
기존에 등록되어있는 팀 아이디 목록 teamIDs 와 추가로 등록 신청을 받은 팀 아이디가 신청받은 순서대로 들어있는 목록 additional이 매개변수로 주어질 때, 추가 신청받은 아이디 중 등록이 완료되는 팀 아이디가 순서대로 있는 배열을 return 하도록 solution 함수를 완성해주세요.

제한사항
--------------
teamIDs는 기존에 등록되어있는 팀 아이디가 문자열 형태로 들어있는 배열이며, 배열의 길이는 1 이상 100,000 이하입니다.
teamIDs의 각 원소는 팀 아이디를 나타내며, 중복된 아이디가 들어있지 않습니다.
additional은 추가로 신청받은 팀 아이디가 첫 번째 원소부터 신청받은 순서대로 들어있는 배열이며, 길이는 1 이상 200,000 이하입니다.
additional의 각 원소는 추가로 신청받은 팀 아이디를 나타냅니다.
모든 팀 ID의 길이는 1 이상 10 이하이며, 알파벳 소문자로만 이루어져 있습니다.
additional의 첫 번째 원소부터 순서대로 아이디를 등록할 때, 추가 등록이 완료되는 아이디들을 먼저 등록된 아이디가 앞에 오도록 배열에 담아 return 하면 됩니다.
return 배열의 길이가 항상 1 이상인 경우만 입력으로 주어집니다. 즉, 추가 등록을 신청한 모든 아이디가 등록 실패하는 경우는 입력으로 주어지지 않습니다.

입출력 예
--------------
teamIDs	additional	result
[world,prog]	[hello,world,code,hello,try,code]	[hello,code,try]
[abc,hq,xyz]	[hq,abc,pp,xy,pp,hq]	[pp,xy]

입출력 예 설명
--------------
입출력 예 #1
문제의 예시와 같습니다.

입출력 예 #2
--------------
additional의 첫 번째 원소부터 순서대로 진행합니다.
hq와 abc는 이미 등록된 아이디이므로 새로 등록되지 않습니다.
세 번째, 네 번째 원소인 pp, xy는 아직 아무 팀도 등록하지 않았으므로 새로 등록됩니다.
이제 pp가 새로운 팀 아이디로 등록되어 있으므로 다섯 번째 원소인 pp는 새로 등록되지 않습니다.
마지막 원소인 hq는 이미 등록된 아이디이기 때문에 새로 등록되지 않습니다.
따라서 추가로 등록되는 아이디는 순서대로 [pp,xy]가 됩니다.

코드
--------------
```cpp
#include <string>
#include <vector>
#include <set>
#include <iostream>

using namespace std;

void print_vector(vector<string> vec) {
    for(auto v: vec)
        cout << v << " ";
    cout << endl;
}

void print_set(set<string> myset) {
    set<string>::iterator it;
    for (it = myset.begin(); it != myset.end(); ++it)
        cout << *it << " ";
    cout << endl;
}

vector<string> solution(vector<string> teamIDs, vector<string> additional) {
    vector<string> answer;
    set<string> ids;
    set<string>::iterator it;
   
    for(int i = 0; i < teamIDs.size(); i++)
        ids.insert(teamIDs[i]);
    
    for(int i = 0; i < additional.size(); i++) {
        it = ids.find(additional[i]);
        if(it == ids.end()) {
            ids.insert(additional[i]);
            answer.push_back(additional[i]);
        }
    }

    return answer;
}
```
