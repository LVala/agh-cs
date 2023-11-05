% Length of the sequence
int: N;

array[0..N] of var 0..N: magic;
  
constraint forall(i in 0..N)(magic[i] == count(magic, i));
  
solve satisfy;
  
output [ "magic sequence = ", show(magic),";\n"];
