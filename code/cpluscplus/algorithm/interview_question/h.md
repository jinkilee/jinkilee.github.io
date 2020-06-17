문제 설명
-------------
철수는 외환 업무 처리를 위해 해외 지점에서 영어로 불러주는 숫자를 받아 적으려 합니다. 다행히 상대방은 zero부터 nine까지의 단어만 사용해 숫자를 말해줍니다.

예를 들어 불러준 숫자가 onesevenfive이면 상대가 말한 숫자는 차례로 one, seven, five이므로, 철수는 175를 받아 적으면 됩니다.

영어로 된 숫자가 들어있는 문자열 number가 매개변수로 주어질 때, 이를 숫자로 변환해 return 하도록 solution 함수를 완성해주세요.

제한사항
-------------
number의 길이는 3 이상 1,000 이하입니다.
number는 알파벳 소문자로만 이루어져 있습니다.
올바르게 숫자로 바꿀 수 있는 경우만 입력으로 주어집니다.
사용되는 단어는 zero, one, two, three, four, five, six, seven, eight, nine입니다.
숫자가 커질 수 있으므로, 문자열 형태로 return 해주세요.

입출력 예
-------------
```
number	result
"onesevenfive"	"175"
"threetwo"	"32"
"fourthreenine"	"439"
"eight"	"8"
"fivetwoonetwo"	"5212"
"zerosix"	"06"
```

입출력 예 설명
-------------
```
입출력 예 #1
문제의 예시와 같습니다.

입출력 예 #2
three, two 이므로 32를 return 합니다.

입출력 예 #3
four, three, nine 이므로 439를 return 합니다.

입출력 예 #4
eight 은 8을 return 합니다.

입출력 예 #5
five, two, one, two 이므로 5212를 return 합니다.

입출력 예 #6
zero, six 이므로 06을 return 합니다.
```


코드
----------------
```cpp
#include <string>
#include <vector>
#include <iostream>
#include <map>

using namespace std;

string solution(string number) {
    string answer = "";
    map<string, int> nmap;
    map<string, int>::iterator it;
    
    nmap["zero"] = 0;
    nmap["one"] = 1;
    nmap["two"] = 2;
    nmap["three"] = 3;
    nmap["four"] = 4;
    nmap["five"] = 5;
    nmap["six"] = 6;
    nmap["seven"] = 7;
    nmap["eight"] = 8;
    nmap["nine"] = 9;
    
    string subnum;
    int start = 0;
    int end = 1;
    int cnt = 1;
    for(int i = 1; i <= number.length(); i++) {
        subnum = number.substr(start, cnt);
        it = nmap.find(subnum);
        if(it != nmap.end()) {
            start = i;
            cnt = 1;
            answer += to_string(nmap[subnum]);
        }
        else
            cnt++;
    }
    return answer;
}
```
