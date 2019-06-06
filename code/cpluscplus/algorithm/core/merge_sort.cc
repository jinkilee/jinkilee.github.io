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

vector<int> merge(vector<int> a, vector<int> b) {
	int lena = a.size();
	int lenb = b.size();
	int i = 0;
	int j = 0;
	int k = 0;
	vector<int> merged(lena+lenb);
	while(1) {
		if(lena == i || lenb == j)
			break;
		if(a[i] < b[j])
			merged[k++] = a[i++];
		else
			merged[k++] = b[j++];
	}
	while(i < lena)
		merged[k++] = a[i++];
	while(j < lenb)
		merged[k++] = b[j++];
	return merged;
}

vector<int> sort(vector<int> arr) {
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
	
	a = sort(a);
	b = sort(b);
	cout << "merged: ";
	print_vector(merge(a, b));
	return merge(a, b);
}

long countInversion(vector<int> arr) {
	arr = sort(arr);
	print_vector(arr);
	return 1;
}

int main() {
	vector<int> a{ 1,2,3,4,5 };
	vector<int> b{ 1,5 };
	countInversion(a);
	return 0;
}
