// Merge Sort: Counting Inversions

#include <algorithm>
#include <vector>
#include <iostream>

using namespace std;

void print_vector(vector<int> v) {
	for(int i = 0; i < v.size(); i++)
		cout << v[i] << " ";
	cout << endl;
}

vector<int> merge(vector<int> a, vector<int> b, long* count) {
	int lena = a.size();
	int lenb = b.size();
	int i = 0;
	int j = 0;
	int k = 0;
	vector<int> merged(lena+lenb);
	while(1) {
		if(lena == i || lenb == j)
			break;
		if(a[i] <= b[j])
			merged[k++] = a[i++];
		else {
			merged[k++] = b[j++];
			(*count) += (lena-i);
		}
	}
	while(i < lena)
		merged[k++] = a[i++];
	while(j < lenb)
		merged[k++] = b[j++];
	return merged;
}

vector<int> sort(vector<int> arr, long* count) {
	int arrlen = arr.size();
	if(arrlen == 1)
		return arr;

	// split data
	int mid = arrlen / 2;
	vector<int> a(mid);
	vector<int> b(arrlen-mid);
	for(int i = 0; i < mid; i++)
		a[i] = arr[i];
	for(int i = 0; i < arrlen-mid; i++)
		b[i] = arr[mid+i];
	
	a = sort(a, count);
	b = sort(b, count);

	return merge(a, b, count);
}

long countInversions(vector<int> arr) {
	long count = 0;
	arr = sort(arr, &count);

	//cout << "merged: ";
	//print_vector(arr);

	cout << "inversion count: " << count << endl;
	return count;
}

int main() {
	//vector<int> a{ 5,4,3,2,1 };
	//vector<int> a{ 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,17,17 };
	vector<int> a;
	for(int i = 10000; i > 0; i--)
		a.push_back(i);
	countInversions(a);
	return 0;
}
