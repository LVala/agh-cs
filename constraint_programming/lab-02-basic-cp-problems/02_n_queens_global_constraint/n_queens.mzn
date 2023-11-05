include "alldifferent.mzn";

% number of queens
int: N;

array[1..N] of var 1..N: rows;

constraint alldifferent(rows);
constraint alldifferent([i - rows[i] | i in 1..N]);
constraint alldifferent([i + rows[i] | i in 1..N]);

solve satisfy;

output [ if fix(rows[j]) == i then "|Q" else "|_" endif ++
  if j == N then "\n" else "" endif | i,j in 1..N];
