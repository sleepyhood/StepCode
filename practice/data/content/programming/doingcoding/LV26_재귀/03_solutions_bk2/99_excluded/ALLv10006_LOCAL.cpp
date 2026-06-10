#include <stdio.h>
#include <string.h>

int cnt; // 호출 횟수를 기록할 전역 변수

int recursion(const char *s, int l, int r) {
    cnt++; // 함수 호출 시마다 카운트 증가
    if (l >= r) return 1;
    else if (s[l] != s[r]) return 0;
    else return recursion(s, l + 1, r - 1);
}

int isPalindrome(const char *s) {
    return recursion(s, 0, strlen(s) - 1);
}

int main() {
    int t;
    char s[1001];
    scanf("%d", &t);
    while (t--) {
        scanf("%s", s);
        cnt = 0; // 테스트 케이스마다 초기화
        int result = isPalindrome(s);
        printf("%d %d\n", result, cnt);
    }
    return 0;
}