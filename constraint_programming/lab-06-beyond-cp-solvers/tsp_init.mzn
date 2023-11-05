include "globals.mzn";

int: Nodes;
set of int: NUM = 1..Nodes;
array[NUM,NUM] of int: Dist;
array[NUM] of var NUM: route;

var int: total_distance;

/*
TODO: 
- it's exactly the same as `tsp_naive.mzn` but just "satisfies" the constraints
*/

constraint route[1] == 1;
constraint alldifferent(route);
constraint total_distance = sum([Dist[route[i],route[(i mod Nodes) + 1]] | i in NUM]);

solve satisfy;


output ["distance: \(total_distance)\nroute = \(route)"];