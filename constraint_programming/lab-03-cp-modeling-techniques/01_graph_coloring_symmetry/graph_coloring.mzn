% parameters
int: nodesNumber;
array [1..nodesNumber, 1..nodesNumber] of bool: edges;
int: minColorsNumber;
array [1..minColorsNumber] of 1..nodesNumber: maxClique;

% decision variables
var 1..nodesNumber: colorsNumber;
array [1..nodesNumber] of var 1..nodesNumber: nodes;

% constraints
constraint forall(i in 1..minColorsNumber)(
  nodes[maxClique[i]] = i
);

constraint colorsNumber = max(nodes);

constraint forall (i,j in 1..nodesNumber where i < j /\ edges[i,j])(
  nodes[i] != nodes[j]
);

% goal
solve minimize colorsNumber;

% output
output [show(colorsNumber), " colors\n",] ++
       [show(nodes[i]) ++ " " | i in 1..nodesNumber]
