include "globals.mzn";

int: Nodes;
set of int: NUM = 1..Nodes;
array[NUM,NUM] of int: Dist;

array[NUM,NUM] of var bool: flow;
array[NUM,NUM] of var 0..Nodes-1: visit_counter;

var int: total_distance;

/*
TODO:
a) flow related
  1) total flow coming from every node should be equal 1
  2) total flow going into every node should be equal 1
b) visit_counter related
  1) visit counter for edges originating from the first node is 0
  2) visit counter for inactive edges should be equal 0
  3) total* visit counter for edges ending at the first node should equal Nodes - 1
  4) total* visit counter for "normal" edges should be higher by 1 compared to the previous* edges
  total visit counter = sum of all the visit counters for the involved edges 
  previous edge = edge with the end being start of the successor edge
c) objective
  1) just calculate it based on the flow :)
*/

constraint forall(i in NUM)(
  sum([bool2int(flow[i,j]) | j in NUM]) == 1 /\
  sum([bool2int(flow[j,i]) | j in NUM]) == 1
);

constraint forall(i in NUM)(visit_counter[1,i] == 0);
constraint forall(i,j in NUM)(visit_counter[i,j] <= flow[i,j] * (Nodes * Nodes));
constraint sum([visit_counter[i,1] | i in NUM]) == Nodes - 1;
constraint forall(i in NUM where i != 1)(
  sum([visit_counter[i,j] | j in NUM]) == sum([visit_counter[j,i] | j in NUM]) + 1
);

constraint total_distance = sum([Dist[i,j] | i,j in NUM where flow[i,j]]);

solve minimize total_distance;

output ["total distance: \(total_distance)\n"] ++
       [if fix(flow[i,j]) then " -> \(j)" else "" endif | i, j in NUM];