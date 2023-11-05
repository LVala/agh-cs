include "alldifferent.mzn";

int: N;
set of int: indexes = 1..N;

array[indexes] of var indexes: rows;

constraint alldifferent(rows);
constraint alldifferent([rows[i] + i | i in indexes]);
constraint alldifferent([rows[i] - i | i in indexes]);

solve :: int_search(rows, first_fail, indomain_min, complete) satisfy; 
  
output [ if fix(rows[j]) == i then "|Q" else "|_" endif ++
  if j == N then "\n" else "" endif | i,j in 1..N];
