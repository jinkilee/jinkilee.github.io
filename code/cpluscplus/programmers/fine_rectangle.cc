using namespace std;

long long solution(int w,int h) {
    long long wl = (long) w;
    long long hl = (long) h;
    long long answer;
    long long gcd = 0;
    long long shorter = (wl > hl)? hl: wl;
    for(long long i = shorter; i > 0; i--) {
        if(wl % i == 0 && hl % i == 0) {
            gcd = i;
            break;
        }
    }
    answer = wl*hl - wl - hl + gcd;
    return answer;
}
