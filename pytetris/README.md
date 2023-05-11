# PyTetris
---
1. 블록 이동: 
    - 사용자가 왼쪽, 오른쪽, 아래 방향키를 누를 때마다 블록의 위치를 해당 방향으로 한 칸씩 이동합니다.
    - 일정 시간이 지날 때마다 블록이 자동으로 아래로 한 칸씩 이동합니다.
2. 블록 회전:
   - 사용자가 위쪽 방향키를 누를 때마다 블록을 시계방향으로 90도씩 회전합니다. 
   - 이때 블록의 모양은 2차원 배열로 표현되며, 배열을 회전시키는 방법으로 구현할 수 있습니다.
3. 충돌 검사: 
   - 블록이 이동하거나 회전할 때마다 게임 보드의 범위 밖으로 나가거나, 이미 쌓여 있는 블록과 겹치는지를 검사합니다. 
   - 만약 그렇다면 이동이나 회전이 취소됩니다.
4. 라인 클리어: 
   - 게임 보드의 한 줄이 모두 블록으로 채워지면, 그 줄이 삭제되고 위에 있는 모든 줄이 아래로 한 칸씩 이동합니다. 
   - 이때 점수를 획득하게 됩니다.