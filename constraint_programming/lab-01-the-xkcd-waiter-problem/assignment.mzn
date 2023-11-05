% Parameters
0..infinity: money_limit;
set of int: menu_items = index_set(menu_prices); 
array[int] of 0..infinity: menu_prices;
array[menu_items] of string: menu_names;
array[menu_items] of int: yumyum_factors; 
array[menu_items] of int: available;

% Variables
array[menu_items] of var 0..infinity: order;
var int: total_yumyum = sum([order[i] * yumyum_factors[i] | i in menu_items]);
var int: total_price = sum([order[i] * menu_prices[i] | i in menu_items]);

% Constraints
constraint total_price <= money_limit;

% Objective
solve maximize total_yumyum;

% Output
output ["\(menu_names[i]): \(order[i])\n" | i in menu_items] ++ 
       ["- total price:\t\(total_price)/\(money_limit)\n"] ++
       ["- total yumyum:\t\(total_yumyum)"];
