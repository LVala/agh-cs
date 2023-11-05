include "diffn_nonstrict.mzn";
include "cumulative.mzn";

int: nr; % number of reclaimers
           % number of rails = nr for stages A,B,C,D,E
           % number of rails = (nr + 1) div 2 for stage F
set of int: RECLAIMER = 1..nr;
bool: stageF; % is this stage F data

int: ns; % number of stockpiles
set of int: STOCKPILE = 1..ns;
array[STOCKPILE] of int: size; % size in 10000 tonnes
array[STOCKPILE] of SHIP: ship; % which ship carries stockpile
 
int: maxtime; % time considered
set of int: TIME = 0..maxtime;

int: nsh; % number of ships
set of int: SHIP = 1..nsh;
array[SHIP] of TIME: arrival; % when ship arrives in port

int: len; % length of pad
set of int: POSITION = 0..len;

int: stack_time;
int: reclaim_time;
int: reclaim_speed;

array[STOCKPILE] of var POSITION: westend;
array[STOCKPILE] of var POSITION: eastend;
array[STOCKPILE] of var TIME: stack;
array[STOCKPILE] of var TIME: endstack;
array[STOCKPILE] of var TIME: reclaim;
array[STOCKPILE] of var TIME: finished;
array[STOCKPILE] of var RECLAIMER: which;

% Go crazy here

% Stage A - Packing Problem
% Two stockpiles can't overlap in "spacetime"

% 1) what's the relation between endstack and stack times
constraint forall(i in STOCKPILE)(
  endstack[i] == stack[i] + (size[i] * stack_time)
);
% 2) what's the relation between finished and stack times
constraint forall(i in STOCKPILE)(
  stack[i] <= finished[i]
);
% 3) what's the relation between reclaim and endstack times
constraint forall(i in STOCKPILE)(
  endstack[i] == reclaim[i]
);
% 4) what's the relation between finished and reclaim times
constraint forall(i in STOCKPILE)(
  finished[i] = reclaim[i] + (size[i] * reclaim_time)
);
% 5) what's the relation between eastend and westend offsets
constraint forall(i in STOCKPILE)(
  eastend[i] = westend[i] + size[i]
);
% 6) packing problem
%    a) stockpiles should not overlap in "spacetime", treat them as rectangles
constraint diffn_nonstrict(stack, westend, [abs(finished[i] - stack[i]) | i in STOCKPILE], size);
constraint cumulative(stack, [abs(finished[i] - stack[i]) | i in STOCKPILE], size, len);
constraint cumulative(westend, size, [abs(finished[i] - stack[i]) | i in STOCKPILE], maxtime);
%    b) stockpiles can't use more space than there is available
constraint forall(i in STOCKPILE)(
  eastend[i] <= len
);
%    c) we can't go beyond the time limit
constraint forall(i in STOCKPILE)(
  finished[i] <= maxtime
);


% Stage B 
% Two stockpiles reclaimed by the same reclaimer do not overlap in time
%
% Tip: write your first custom predicate, i.e.
% predicate not_overlap(var STOCKPILE: s1, var STOCKPILE: s2) =
% <something something> ;
predicate not_overlap(var STOCKPILE: s1, var STOCKPILE: s2) =
          let {
              var int: time_to_move = abs(westend[s1] - westend[s2]) * reclaim_speed
          } in reclaim[s1] != reclaim[s2] /\
             ((reclaim[s1] < reclaim[s2] -> finished[s1] + time_to_move <= reclaim[s2]) /\
              (reclaim[s2] < reclaim[s1] -> finished[s2] + time_to_move <= reclaim[s1]));

constraint forall(i,j in STOCKPILE where i < j)(
  which[i] == which[j] -> not_overlap(i,j)
);


% Stage C
% 1) no stockpile can be reclaimed onto a ship before the arrival time of the ship
constraint forall(i in STOCKPILE)(
  arrival[ship[i]] <= reclaim[i]
);
% 2) also no two stockpiles can be reclaimed onto the same ship at the same time. Make sure these reclaims do not overlap in time.
% TIP: reuse your "not_overlap" predicate
constraint forall(i,j in STOCKPILE where i < j)(
  ship[i] == ship[j] -> not_overlap(i,j)
);


% Stage D
% Add constraints to your model to ensure that if a reclaimer finishes reclaiming a stockpile with westend at x and then has to start reclaiming a stockpile with westend at y there is at least |y − x| ∗ reclaim speed time between these two events.
% TIP: just make your "not_overlap" predicate smarter
% TIP: you can introduce local variables in the constraints/predicates
% let {
%  <local variables>
% } in <then something>



% Stage E
% Add a definition of the objective to your model and change the model to minimize this value.
% You may well need to significantly change your search strategy to get good solutions for the objective.

% TIP: definetely change the line below
var int: obj = sum([max([finished[j] | j in STOCKPILE where ship[j] == i]) - arrival[i] | i in SHIP]);

% search ordering constraints
array[1..4*ns] of var TIME: search_times;
constraint forall(i in STOCKPILE)(
  search_times[4*i-3] == reclaim[i] /\
  search_times[4*i-2] == finished[i] /\
  search_times[4*i-1] == stack[i] /\
  search_times[4*i] == endstack[i]
);
array[1..2*ns] of var POSITION: search_positions;
constraint forall(i in STOCKPILE)(
  search_positions[2*i-1] == westend[i] /\
  search_positions[2*i] == eastend[i]
);


solve :: seq_search([
                     int_search(search_times, input_order, indomain_split),
                     int_search(search_positions, input_order, indomain_split)
                     ]) minimize obj;
% solve minimize obj;


% Stage F
% Add constraints in your model so that the two reclaimers on rail i numbered 2i − 1 and 2i for i ∈ 1..nr div 2 remain so the western one 2i − 1 is never east of the eastern one 2i. Note they can legitimately be in the same position (this is for simplicity, its not very real). Note that if there are
% an odd number of reclaimers the last reclaimer is on its own rail and has no further constraints.
% TIP: do some "channeling" and model reclaimers' positions explicitely with a new array of variables.
int: n_railway_reclaimers = (nr div 2)*2;
set of int: RAILWAY_RECLAIMERS = 1..n_railway_reclaimers;
array[RAILWAY_RECLAIMERS, TIME] of var POSITION: rail_positions;

constraint stageF -> forall(r in RAILWAY_RECLAIMERS)(
  forall(s IN STOCKPILE where which[s] = r)(
    % position of the reclaimer is fixed when it's reclaiming
    forall(t in TIME)(
      t >= reclaim[s] /\ t <= finished[s] -> rail_positions[r,t] = westend[s]
    ) /\
    % limiting the reclaimer's movement speed
    forall(t in reclaim_speed..maxtime)(
      rail_positions[r,t] != rail_positions[r,t-1] -> all_equal([rail_positions[r,tt] | tt in t-reclaim_speed..t-1])
    )
  )
)

% reclaimers sharing a rail can't corss
constraint stageF -> forall(i in 1..nr div 2)(
  let {
    RECLAIMER: r1 = 2*i - 1,
    RECLAIMER: r2 = 2+i
  } in
  forall(t in TIME)(
    rail_positions[r1,t] <= rail_positions[r2,t] 
  )
)

% don't change the output
output 
["westend  = ", show(westend), ";\n"] ++
["eastend  = ", show(eastend), ";\n"] ++
["stack    = ", show(stack), ";\n"] ++
["endstack = ", show(endstack), ";\n"] ++
["reclaim  = ", show(reclaim), ";\n"] ++
["finish   = ", show(finished) , ";\n"] ++
["which    = ", show(which), ";\n"] ++
["obj = ",show(obj), ";\n"]
;
