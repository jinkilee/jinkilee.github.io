문제 설명
-----------
숫자 야구 게임이란 2명이 서로가 생각한 숫자를 맞추는 게임입니다. 게임해보기

각자 서로 다른 1~9까지 3자리 임의의 숫자를 정한 뒤 서로에게 3자리의 숫자를 불러서 결과를 확인합니다. 그리고 그 결과를 토대로 상대가 정한 숫자를 예상한 뒤 맞힙니다.

* 숫자는 맞지만, 위치가 틀렸을 때는 볼
* 숫자와 위치가 모두 맞을 때는 스트라이크
* 숫자와 위치가 모두 틀렸을 때는 아웃
예를 들어, 아래의 경우가 있으면

A : 123
B : 1스트라이크 1볼.
A : 356
B : 1스트라이크 0볼.
A : 327
B : 2스트라이크 0볼.
A : 489
B : 0스트라이크 1볼.
이때 가능한 답은 324와 328 두 가지입니다.

질문한 세 자리의 수, 스트라이크의 수, 볼의 수를 담은 2차원 배열 baseball이 매개변수로 주어질 때, 가능한 답의 개수를 return 하도록 solution 함수를 작성해주세요.

제한사항
-----------
질문의 수는 1 이상 100 이하의 자연수입니다.
baseball의 각 행은 [세 자리의 수, 스트라이크의 수, 볼의 수] 를 담고 있습니다.

입출력 예
-----------
baseball	return
[[123, 1, 1], [356, 1, 0], [327, 2, 0], [489, 0, 1]]	2

입출력 예 설명
-----------
문제에 나온 예와 같습니다.




#include <string>
#include <vector>
#include <iostream>
using namespace std;

void print_vector(vector<int> vec) {
    for(int i = 0; i < vec.size(); i++)
        cout << vec[i] << " ";
    cout << endl;
}

int fight(string target, string number) {
    int strike = 0;
    int ball = 0;
    char onechar;
    for(int i = 0; i < 3; i++) {
        onechar = target[i];
        for(int j = 0; j < 3; j++) {
            if(onechar == number[j]) {
                if(i == j)
                    strike++;
                else
                    ball++;
                break;
            }
        }
    }
    //cout << "strike:" << strike << " " << "ball:" << ball << endl;
    return strike*10+ball;
}

int solution(vector<vector<int>> baseball) {
    //int ntarget = 324;
    //int nnumber = 123;
    //nnumber = 356;
    //nnumber = 327;
    //nnumber = 489;
    //number = to_string(nnumber);
    //target = to_string(ntarget);
    //cout << fight(target, number) << endl;

    int answer = 0;
    string target, number;
    int strike, ball;
    bool pass;
   
    //*/
    for(int i = 123; i <= 987; i++) {
        target = to_string(i);
        pass = true;
        
        if(target[0] == '0' || target[1] == '0' || target[2] == '0') {
            continue;
        }
        if(target[0] == target[1] || target[1] == target[2] || target[0] == target[2]) {
            continue;
        }
        
        for(int j = 0; j < baseball.size(); j++) {
            strike = baseball[j][1];
            ball = baseball[j][2];
            
            if((strike*10 + ball) != fight(target, to_string(baseball[j][0]))) {
                pass = false;
                break;
            }
        }
        if(pass)
            answer++;
    }
    //*/
    return answer;
}
