include "globals.mzn";

%%%%%%%% CONSTANTS %%%%%%%%

int: room_cost = 200;
int: n_interviews = 3;
set of int: Interview = 1..n_interviews;

set of int: Preference = 1..5;
set of int: Slot = 1..20;

%%%%%%%% PARAMETERS %%%%%%%%

int: n_students;
int: n_companies;
set of int: Student = 1..n_students;
set of int: Company = 1..n_companies;

array[Student, Company] of Preference: preferences;
array[Student] of int: best_expectations;
array[Company] of int: min_capacities;
array[Company] of int: max_capacities;
array[Company] of int: attendance_costs;
array[Company] of int: parallel_limits;
array[Student] of set of Slot: slots;

%%%%%%%% VARIABLES %%%%%%%%

% company for each of the student's interviews
array[Student, Interview] of var Company: companies;

% timeslot for each of the student's interviews
array[Student, Interview] of var Slot: timeslots;

% using this gives slight performance boost compared to calculating total_attendance_cost from companies and timeslots arrays
array[Company] of var set of 1..5: schedule;
constraint forall(i in Company, j in Slot, k in Student, m in Interview)(
  (companies[k,m] = i /\ timeslots[k,m] = j) -> ((j-1) div 4) + 1 in schedule[i]
);

%%%%%%%% CONSTRAINTS %%%%%%%%

% all of each student's interviews must be conducted by a different company
constraint forall(i in Student)(
  strictly_increasing(companies[i,..])  % instead of alldifferent to break symmetry
);

% all of each student's interviews must be in a different timeslots
constraint forall(i in Student)(
  alldifferent(timeslots[i,..])
);

% capacity for each company
array[Company] of var 0..n_students: gcc_companies;
constraint global_cardinality(companies, array1d(Company, [i | i in Company]), gcc_companies);
constraint forall(i in Company)(
  gcc_companies[i] >= min_capacities[i] /\ gcc_companies[i] <= max_capacities[i]
);

% how many students each company can interview in parallel
constraint forall(i in Slot)(
  forall(j in Company)(
    count(array1d(1..n_students*n_interviews, [companies[k,m] * bool2int(timeslots[k,m] = i)| k in Student, m in Interview]), j) <= parallel_limits[j]
  )
);

% when students can attend the interviews
constraint forall(i in Student, j in Interview)(
  timeslots[i,j] in slots[i]
);

%%%%%%%% OBJECTIVE %%%%%%%%

% total room cost
array[Slot] of var 0..n_students: gcc_timeslots;  % global cardinality count
constraint global_cardinality(timeslots, array1d(Slot, [i | i in Slot]), gcc_timeslots);
var 0..room_cost*n_students: total_rooms_cost = max(gcc_timeslots) * room_cost;

% total attendance cost
var 0..infinity: total_attendance_cost = sum([(max(schedule[i]) - min(schedule[i]) + 1) * attendance_costs[i] | i in Company]);

% total disappointment value
array[Student, Interview] of var Preference: assigned_preferences;
constraint forall(i in Student, j in Interview)(
  assigned_preferences[i, j] = preferences[i, companies[i,j]]
);
var 0..n_students*12: total_disappointment_value = 
  sum(array1d(Student, [max(sum(assigned_preferences[i,..]) - best_expectations[i], 0) | i in Student]));

% objective itself
var 0..infinity: obj = total_rooms_cost + total_disappointment_value + total_attendance_cost;

solve minimize obj;  % did not find any search annotations that would improve the performance

%%%%%%%% OUTPUT %%%%%%%%

output
["companies = ", show(companies), ";\n"] ++
["timeslots = ", show(timeslots), ";\n"] ++
["obj = ", show(obj), ";\n"]
;