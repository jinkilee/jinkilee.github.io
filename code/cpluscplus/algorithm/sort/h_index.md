문제 설명
----------------
H-Index는 과학자의 생산성과 영향력을 나타내는 지표입니다. 어느 과학자의 H-Index를 나타내는 값인 h를 구하려고 합니다. 위키백과1에 따르면, H-Index는 다음과 같이 구합니다.

어떤 과학자가 발표한 논문 n편 중, h번 이상 인용된 논문이 h편 이상이고 나머지 논문이 h번 이하 인용되었다면 h의 최댓값이 이 과학자의 H-Index입니다.

어떤 과학자가 발표한 논문의 인용 횟수를 담은 배열 citations가 매개변수로 주어질 때, 이 과학자의 H-Index를 return 하도록 solution 함수를 작성해주세요.

제한사항
----------------
과학자가 발표한 논문의 수는 1편 이상 1,000편 이하입니다.
논문별 인용 횟수는 0회 이상 10,000회 이하입니다.

입출력 예
----------------
citations	return
[3, 0, 6, 1, 5]	3

입출력 예 설명
----------------
이 과학자가 발표한 논문의 수는 5편이고, 그중 3편의 논문은 3회 이상 인용되었습니다. 그리고 나머지 2편의 논문은 3회 이하 인용되었기 때문에 이 과학자의 H-Index는 3입니다.


코드
```cpp
#include <string>
#include <vector>
#include <iostream>

using namespace std;

void swap(vector<int>& v, int x, int y);

void quicksort(vector<int> &vec, int L, int R) {
    int i, j, mid, piv;
    i = L;
    j = R;
    mid = L + (R - L) / 2;
    piv = vec[mid];

    while (i<R || j>L) {
        while (vec[i] < piv)
            i++;
        while (vec[j] > piv)
            j--;

        if (i <= j) {
            swap(vec, i, j); //error=swap function doesnt take 3 arguments
            i++;
            j--;
        }
        else {
            if (i < R)
                quicksort(vec, i, R);
            if (j > L)
                quicksort(vec, L, j);
            return;
        }
    }
}

void swap(vector<int>& v, int x, int y) {
    int temp = v[x];
    v[x] = v[y];
    v[y] = temp;

}

void print_vector(vector<int> vec) {
    for(int i = 0; i < vec.size(); i++)
        cout << vec[i] << " ";
    cout << endl;
}

bool is_hindex(vector<int> citations, int h) {
    for(int i = 0; i < citations.size(); i++) {
        if(citations[i] == 0)
            continue;
        if((citations[i] >= h) && (citations.size() - i >= h)) {
            return true;
        }
    }
    return false;
}
int solution(vector<int> citations) {
    int answer = 0;
    int n_ctt = citations.size();
    int remains;
    
    quicksort(citations, 0, n_ctt-1);
    //print_vector(citations);
    
    int min_h = 1;
    int max_h = citations[n_ctt-1];
    
    for(int h = min_h; h <=max_h; h++) {
        //cout << "h:" << h << " " << is_hindex(citations, h) << endl;
        if(is_hindex(citations, h))
            answer = h;
        else
            break;
    }
    return answer;
}
```
