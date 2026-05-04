#include <stdio.h>

int N;
int values[] = {1, 5, 10, 50};
bool possible_sums[1001]; // N=20, Max=50 -> MaxSum = 1000
int total_distinct_sums = 0;

// count: 현재까지 선택한 숫자의 개수
// current_sum: 현재까지의 합
// start_idx: 중복 조합을 피하기 위한 시작 인덱스
void solve(int count, int current_sum, int start_idx) {
  if (count == N) {
    if (!possible_sums[current_sum]) {
      possible_sums[current_sum] = true;
      total_distinct_sums++;
    }
    return;
  }

  for (int i = start_idx; i < 4; i++) {
    solve(count + 1, current_sum + values[i], i);
  }
}

int main() {
  if (scanf("%d", &N) != 1)
    return 0;

  // 가능한 합 초기화
  for (int i = 0; i <= 1000; i++)
    possible_sums[i] = false;

  solve(0, 0, 0);

  printf("%d\n", total_distinct_sums);

  return 0;
}
