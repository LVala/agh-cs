include "globals.mzn";

int: Nodes;
set of int: NUM = 1..Nodes;
array[NUM,NUM] of int: Dist;
array[NUM] of var NUM: route;

var int: total_distance;

/*
TODO: 
- the cities in the route should not repeat
- the first city in the route should be fixed to 1
- calculate the total distance based on the route
*/

constraint route[1] == 1;
constraint alldifferent(route);
constraint total_distance = sum([Dist[route[i],route[(i mod Nodes) + 1]] | i in NUM]);

solve minimize total_distance;


output ["distance: \(total_distance)\nroute = \(route)"];