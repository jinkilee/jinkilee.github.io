문제 설명
------------------
직사각형을 만드는 데 필요한 4개의 점 중 3개의 좌표가 주어질 때, 나머지 한 점의 좌표를 구하려고 합니다. 점 3개의 좌표가 들어있는 배열 v가 매개변수로 주어질 때, 직사각형을 만드는 데 필요한 나머지 한 점의 좌표를 return 하도록 solution 함수를 완성해주세요. 단, 직사각형의 각 변은 x축, y축에 평행하며, 반드시 직사각형을 만들 수 있는 경우만 입력으로 주어집니다.

제한사항
------------------
v는 세 점의 좌표가 들어있는 2차원 배열입니다.
v의 각 원소는 점의 좌표를 나타내며, 좌표는 [x축 좌표, y축 좌표] 순으로 주어집니다.
좌표값은 1 이상 10억 이하의 자연수입니다.
직사각형을 만드는 데 필요한 나머지 한 점의 좌표를 [x축 좌표, y축 좌표] 순으로 담아 return 해주세요.

입출력 예
------------------
```
v	result
[[1, 4], [3, 4], [3, 10]]	[1, 10]
[[1, 1], [2, 2], [1, 2]]	[2, 1]
```

입출력 예 설명
------------------
- 입출력 예 #1: 세 점이 [1, 4], [3, 4], [3, 10] 위치에 있을 때, [1, 10]에 점이 위치하면 직사각형이 됩니다.
- 입출력 예 #2: 세 점이 [1, 1], [2, 2], [1, 2] 위치에 있을 때, [2, 1]에 점이 위치하면 직사각형이 됩니다.

코드
------------------
```cpp
#include <iostream>
#include <vector>
#include <map>
using namespace std;

void print_vector(vector<int> vec) {
    for(int i = 0; i < vec.size(); i++)
        cout << vec[i] << " ";
    cout << endl;
}

void print_map(map<int, int> m) {
    for (map<int,int>::iterator it=m.begin(); it!=m.end(); ++it)
        cout << it->first << " => " << it->second << '\n';
}
vector<int> solution(vector<vector<int> > v) {
    vector<int> ans;
	map<int, int> rmap;
	map<int, int> cmap;
    map<int, int>::iterator it;

    int row, col;
    for(int i = 0; i < v.size(); i++) {
        row = v[i][0];
        col = v[i][1];
        
        // find row from rmap
        it = rmap.find(row);
        if(it == rmap.end()) {
            // row not found
            rmap[row] = 1;
        }
        else
            rmap[row]++;
       
        // find col from cmap
        it = rmap.find(col);
        if(it == cmap.end()) {
            // row not found
            cmap[col] = 1;
        }
        else
            cmap[col]++;
    }

   	// make answer for row
    for (it=rmap.begin(); it != rmap.end(); ++it) {
        if(it->second != 2) {
            ans.push_back(it->first);
            break;
        }
    }
   	// make answer for col
    for (it=cmap.begin(); it != cmap.end(); ++it) {
        if(it->second != 2) {
            ans.push_back(it->first);
            break;
        }
    }
    
    //print_map(rmap);
    //cout << "-----------" << endl;
    //print_map(cmap);
    //print_vector(ans);
    return ans;
}
```
