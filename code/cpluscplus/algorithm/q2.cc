// Merge Sort: Counting Inversions
// https://www.youtube.com/watch?v=XKu_SEDAykw&t=350s

#include <algorithm>
#include <vector>
#include <iostream>

using namespace std;

void print_vector(vector<int> v) {
	for(int i = 0; i < v.size(); i++)
		cout << v[i] << " ";
	cout << endl;
}

int sum_available(vector<int> arr, int target) {
	int i = 0;
	int j = arr.size() - 1;
	int sum = 0;
	int left = 0;
	int right = 0;
	while(1) {
		if (i == j)
			break;
		left = arr[i];
		right = arr[j];

		if(2*right < target || 2*left > target)
			return 0;
		if(left + right == target)
			return 1;
		else if(left + right < target)
			i++;
		else if(left + right > target)
			j--;
		else
			break;
	}
	return 0;
}
int main() {
	//vector<int> a{ 1,2,3,9 };
	//vector<int> a{ 1,2,4,4 };
	vector<int> a{ 4,5,8,8,12,13,18,19,20,24,25,26,27,29,30,33,33,36,36,39,45,45,46,47,48,49,49,51,52,53,55,56,56,58,58,58,59,61,62,63,65,65,68,70,73,77,77,79,90,92 };
	//vector<int> a{ 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,17,17 };
	/*
	vector<int> a;
	for(int i = 10000; i > 0; i--)
		a.push_back(i);
	*/
	int res = sum_available(a, -1000);
	cout << "res: " << res << endl;
	return 0;
}
