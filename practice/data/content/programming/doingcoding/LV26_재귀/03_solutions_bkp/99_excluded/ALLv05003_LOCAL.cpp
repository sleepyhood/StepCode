#include <stdio.h>

void print_bar(int depth) {
    for (int i = 0; i < depth; i++) printf("____");
}

void chatbot(int depth, int n) {
    print_bar(depth);

    if (depth == n) {
        // 기저 조건: 결론을 출력하고 종료
        printf("\"재귀함수가 뭔가요?\"\n");
        print_bar(depth);
        printf("\"재귀함수는 자기 자신을 호출하는 함수라네.\"\n");
    } else {
        // 재귀 호출 전: 질문과 고민 시작
        printf("\"재귀함수가 뭔가요?\"\n");
        print_bar(depth);
        printf("\"잘 들어보게. 옛날옛날 한 산 꼭대기에 선인이 있었어.\n");
        print_bar(depth);
        printf("마을 사람들은 모두 그 선인에게 수많은 질문을 했고, 모두 지혜롭게 대답해 주었지.\n");
        print_bar(depth);
        printf("그 선인에게 한 제자가 찾아와서 물었어.\"\n");

        // 재귀 호출 (한 단계 더 깊이)
        chatbot(depth + 1, n);
    }

    // 재귀 호출 후: 되돌아오며 마무리
    print_bar(depth);
    printf("라고 답변하였지.\n");
}

int main() {
    int n;
    scanf("%d", &n);

    // 고정 첫 줄 출력 (깊이 0, 들여쓰기 없음)
    printf("어느 한 학생이 챗봇에게 물었다.\n");
    chatbot(0, n);

    return 0;
}