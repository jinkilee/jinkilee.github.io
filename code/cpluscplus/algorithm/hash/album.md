문제 설명
-----------------
스트리밍 사이트에서 장르 별로 가장 많이 재생된 노래를 두 개씩 모아 베스트 앨범을 출시하려 합니다. 노래는 고유 번호로 구분하며, 노래를 수록하는 기준은 다음과 같습니다.

속한 노래가 많이 재생된 장르를 먼저 수록합니다.
장르 내에서 많이 재생된 노래를 먼저 수록합니다.
장르 내에서 재생 횟수가 같은 노래 중에서는 고유 번호가 낮은 노래를 먼저 수록합니다.
노래의 장르를 나타내는 문자열 배열 genres와 노래별 재생 횟수를 나타내는 정수 배열 plays가 주어질 때, 베스트 앨범에 들어갈 노래의 고유 번호를 순서대로 return 하도록 solution 함수를 완성하세요.

제한사항
-----------------
genres[i]는 고유번호가 i인 노래의 장르입니다.
plays[i]는 고유번호가 i인 노래가 재생된 횟수입니다.
genres와 plays의 길이는 같으며, 이는 1 이상 10,000 이하입니다.
장르 종류는 100개 미만입니다.
장르에 속한 곡이 하나라면, 하나의 곡만 선택합니다.
모든 장르는 재생된 횟수가 다릅니다.

입출력 예
-----------------
```
genres	plays	return
[classic, pop, classic, classic, pop]	[500, 600, 150, 800, 2500]	[4, 1, 3, 0]
```

입출력 예 설명
-----------------
classic 장르는 1,450회 재생되었으며, classic 노래는 다음과 같습니다.

고유 번호 3: 800회 재생
고유 번호 0: 500회 재생
고유 번호 2: 150회 재생
pop 장르는 3,100회 재생되었으며, pop 노래는 다음과 같습니다.

고유 번호 4: 2,500회 재생
고유 번호 1: 600회 재생
따라서 pop 장르의 [4, 1]번 노래를 먼저, classic 장르의 [3, 0]번 노래를 그다음에 수록합니다.

코드
-----------------
```cpp
#include <string>
#include <vector>
#include <iostream>
//#include <unordered_map>
#include <queue>
#include <map>
#include <utility>

using namespace std;

void print_vector(vector<int> vec) {
    for(auto v: vec)
        cout << v << " ";
    cout << endl;
}


void print_map(map<string, int> m) {
    for (map<string,int>::reverse_iterator rit=m.rbegin(); rit!=m.rend(); ++rit)
        cout << rit->first << " => " << rit->second << '\n';
}

struct Music{
	int id;
    int sec;
	Music(int index, int second) : id(index), sec(second) {
    }
};

struct compare {
    bool  operator()(Music &a, Music &b) {
        if(a.sec != b.sec)
            return a.sec <= b.sec;
        else
            return a.id > b.id;
    }
};

void print_queue(priority_queue<Music, vector<Music>, compare> q) {
    priority_queue<Music, vector<Music>, compare> qq = q;
    cout << "queue: ";
    while(!qq.empty()) {
        cout << qq.top().id << ":" << qq.top().sec << " ";
        qq.pop();
    }
    cout << endl;
}

vector<int> solution(vector<string> genres, vector<int> plays) {
    vector<int> answer;
    map<string, int> genmap;
    map<int, string> genmap_sorted;
    map<string, priority_queue<Music, vector<Music>, compare>> quemap;
    map<string, priority_queue<Music, vector<Music>, compare>>::iterator it;
    map<int, string>::reverse_iterator rit;
    map<string, int>::iterator git;
    string curr;

    /*/
    genres.clear();
    plays.clear();
    genres.push_back("pop");
	plays.push_back(2500);
    //*/
    
    for(int i = 0; i < genres.size(); i++) {
        it = quemap.find(genres[i]);
        Music music(i, plays[i]);
        if(it == quemap.end()) {
            priority_queue<Music, vector<Music>, compare> q;
            genmap.insert({genres[i], plays[i]});
            quemap.insert({genres[i], q});
            quemap[genres[i]].push(music);
        }
        else {
            genmap[genres[i]] += plays[i];
            quemap[genres[i]].push(music);
        }
    }

    for(git=genmap.begin(); git!=genmap.end(); ++git) {
        curr = git->first;
        genmap_sorted.insert({genmap[curr], curr});
    }

    for(rit=genmap_sorted.rbegin(); rit!=genmap_sorted.rend(); ++rit) {
        curr = genmap_sorted[rit->first];
        if(quemap[curr].size() < 2)
            answer.push_back(quemap[curr].top().id);
        else {
            answer.push_back(quemap[curr].top().id);
            quemap[curr].pop();
            answer.push_back(quemap[curr].top().id);
        }
    }
    
    return answer;
}
```
