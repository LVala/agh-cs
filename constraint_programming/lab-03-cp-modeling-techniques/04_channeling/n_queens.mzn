include "alldifferent.mzn";
include "lex_lesseq.mzn";

int: N;
set of int: indexes = 1..N;

% 1st model

array[indexes] of var indexes: rows;

constraint alldifferent(rows);
constraint alldifferent([rows[i] + i | i in indexes]);
constraint alldifferent([rows[i] - i | i in indexes]);

% 2nd model

array[indexes, indexes] of var bool: qb;

constraint forall(i in indexes)(
  count(qb[i,..], true) == 1
);
constraint forall(i in indexes)(
  count(qb[..,i], true) == 1
);
constraint forall(i in 2..2*N)(
  count([qb[a,b] | a,b in indexes where a + b == i], true) <= 1
);
constraint forall(i in -N+1..N-1)(
  count([qb[a,b] | a,b in indexes where a - b == i], true) <= 1
);

% symmetry breaking

constraint lex_lesseq(array1d(qb), [ qb[j,i] | i,j in 1..N ])
/\  lex_lesseq(array1d(qb), [ qb[i,j] | i in reverse(1..N), j in 1..N ])
/\  lex_lesseq(array1d(qb), [ qb[j,i] | i in 1..N, j in reverse(1..N) ])
/\  lex_lesseq(array1d(qb), [ qb[i,j] | i in 1..N, j in reverse(1..N) ])
/\  lex_lesseq(array1d(qb), [ qb[j,i] | i in reverse(1..N), j in 1..N ])
/\  lex_lesseq(array1d(qb), [ qb[i,j] | i,j in reverse(1..N) ])
/\  lex_lesseq(array1d(qb), [ qb[j,i] | i,j in reverse(1..N) ]);

% connecting models

constraint forall (i,j in indexes) ( qb[i,j] <-> (rows[i]=j) );

solve satisfy; 
  
output [ if fix(rows[j]) == i then "|Q" else "|_" endif ++
  if j == N then "\n" else "" endif | i,j in 1..N];
