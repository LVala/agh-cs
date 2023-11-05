include "diffn_nonstrict.mzn";
include "cumulative.mzn";

% Parameters
%%%%%%%%%%%
int: n;                      % How many squares do we have?
set of int: SQUARES = 1..n;  % Set of the available squares
array[SQUARES] of int: sq_sizes = [i | i in SQUARES];  % Sizes of squares

% Variables
%%%%%%%%%%%
var n..sum([i | i in SQUARES]): height;    % height of the container
var n..sum([i | i in SQUARES]): width;     % width of the conainer
var sum([i*i | i in SQUARES])..pow(sum([i | i in SQUARES]), 2): area = height * width; % container's area
array[SQUARES] of var 0..sum([i | i in SQUARES])-1: x; % squares' coordinates in the container
array[SQUARES] of var 0..sum([i | i in SQUARES])-1: y; % squares' coordinated in the container

array[1..2*n] of var 0..sum([i | i in SQUARES])-1: search_arr;
  
% Constraints 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

% Constraint 1: Squares should fit inside the container
constraint forall(i in SQUARES)(
    x[i] <= sum([j | j in SQUARES])-i /\ y[i] <= sum([j | j in SQUARES])-i
);

% Constraint 2: Squares should not overlap
constraint diffn_nonstrict(x, y, sq_sizes, sq_sizes);

% assign height and width to the boxes extending the most
constraint height = max([y[i] + i | i in SQUARES]) /\ width = max([x[i] + i | i in SQUARES]);

% redundant constraints
constraint cumulative(x, sq_sizes, sq_sizes, height);
constraint cumulative(y, sq_sizes, sq_sizes, width);

% search ordering constraint
constraint forall(i in SQUARES)(
    search_arr[2*i-1] == x[n-i+1] /\ search_arr[2*i] == y[n-i+1] 
);

% Goal
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
solve :: seq_search([
            int_search([height, width], input_order, indomain_min, complete),
            int_search(search_arr, input_order, indomain_min, complete)
]) minimize area; 
  

% Boring output  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
output [ show(i) ++ " > (" ++ show(x[i]) ++ "," ++ show(y[i]) ++ ")\n" | i in 1..n] ++
  ["area = " ++ show(width) ++ " * " ++ show(height) ++ " = " ++ show(area)];
