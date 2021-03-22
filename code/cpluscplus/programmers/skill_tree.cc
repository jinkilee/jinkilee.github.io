#include <iostream>
#include <map>
#include <string>
#include <vector>

using namespace std;

bool in_order(string skill_tree, map<char, int> hs_skill) {
    char temp;
    int last_found_idx = 0;
    for(int j = 0; j < skill_tree.size(); j++) {
        temp = skill_tree[j];
        if(hs_skill[temp] != 0) {
            if(last_found_idx + 1 == hs_skill[temp])
                last_found_idx = hs_skill[temp];
            else
                return false;
        }
        cout << "temp: " << temp << " hs_skill[temp]: " << hs_skill[temp] << endl;
    }
    return true;
}

int solution(string skill, vector<string> skill_trees) {
    int answer = 0;
    map<char, int> hs_skill;
    for(int i = 0; i < skill.size(); i++)
        hs_skill[(char)skill[i]] = i + 1;

    int count = 0;
    char temp;
    for(int i = 0; i < skill_trees.size(); i++) {
        if(in_order(skill_trees[i], hs_skill)) {
            count++;
            cout << skill_trees[i] << endl;
        }
    }
    return count;
}

//"CBD", ["BACDE", "CBADF", "AECB", "BDA"]
int main() {
    vector<string> skill_trees;
    skill_trees.push_back("BACDE");
    skill_trees.push_back("CBADF");
    skill_trees.push_back("AECB");
    skill_trees.push_back("BDA");
    int a = solution("CBD", skill_trees);
    cout << "----------------" << endl;
    cout << a << endl;
    return 0;
}
