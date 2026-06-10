#include <stdio.h>
#include <string.h>

char str[105];

void wrap(int i) {
  // 기저 조건: 다음 문자가 없으면 현재가 마지막 문자임
  if (str[i + 1] == '\0') {
    printf("%c", str[i]);
    return;
  }

  // [전위 처리] 호출 전: 현재 문자 출력 + 열린 괄호
  printf("%c(", str[i]);

  // 재귀 호출: 다음 인덱스로 이동
  wrap(i + 1);

  // [후위 처리] 호출 후: 닫힌 괄호 + 현재 문자 대칭 출력
  printf(")%c", str[i]);
}

int main() {
  if (scanf("%s", str) == 1) {
    wrap(0);
    printf("\n");
  }
  return 0;
}