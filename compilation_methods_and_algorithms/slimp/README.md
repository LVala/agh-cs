# Slimp - a simple programming language

This repository contains Antlr4 build and transpiler to C of the Slimp language.

## Authors

- Łukasz Wala
- Damian Tworek

## Setup for developement

Make sure you hava `gradle` and Java17 or newer installed. Run the app with

```bash
gradle run --args="-o program program.smp"
```

To pass arguments, use `gradle --args`.

## Examples

- below and in ./examples/ subdirectory

## Description

- Imperative programming language
- Statically, strongly typed (no automatic type conversion)
- tool: transpiler to C

### Data types: simple data types: `int`, `char`, `bool`

```rust
x: int = 5;
x: char = 'c';
x: bool = true;
```

### Data structures

```rust
list: [int; 5] = [1..5];
```

### Logical operations, comparison

```rust
a: bool = false;
b: bool = true;
x: bool = a && b
x: bool = a || b
x: bool = !b
x: bool = x < x;
x: bool = x > x;
x: bool = x == x;
x: bool = x != x;
x: bool = (true || (false && true)) || false && true;
x: bool = 1 < 2 && 1 < 2;
```

### Arithmetic operations

```rust
a: int = x + x;
a: int = x - x;
a: int = x * x;

a: int = x * (x + x);
e: int = -((54 - 34) * 44342) + 1;
```

### Comments

```rust
x: int = 1;  # comment
```

### Type casting

```rust
e: int = -((54 - 34) * 44342) + (1.0 as int) + (true as int); 
```

### Scope

```rust
a: int = 1;
fun main() : int {
    print(a);  # 1
    a: int = 2;
    print(@parent a, a);  # 1 2
    return 0;
}
```

### Start point

```rust
fun main() {
    print("Hello Slimp!");
}
```

### Functions

```rust
fun helloSlimp(year: int): () {
    if true {
        print("Hello Slimp", "!", year);
    }
}

fun main(): () {
    year: int = 2023;
    print(helloSlimp(year));
}
```

### Control flow

```rust
if x == 5 {
    print("abc");
} else if x == 8 {
    print("x is 8");
} else {
    print("else");
}
```

```rust

while true {
    break;
}
```

### For each

```rust
for i <- [1, 2, 3] {
    print(i);
}
```

### Recursive function

```rust
fun recursive(x: int, b: bool): int {
    if x == 3 {
        return 8921;
    }
    else {
        return recursive(3, 5);
    }
}
```
