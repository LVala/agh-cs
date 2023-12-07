# Solution of gravitational potential differential equation using finite element method - project for Differential and Difference Equations Course
### Łukasz Wala, 2021/22 winter semester, Computer Science WIEiT AGH UST

This repository contains [problem description (in Polish)](mes_opracowanie.pdf) and program written in Julia programming language that preproceses the equation matrix (mainly by solving some integrals by Gauss–Legendre quadrature) and solves the system of equations using Gaussian elimination.

To run you need [Julia compiler](https://julialang.org/downloads/) and [Plots](https://docs.juliaplots.org/latest/) package which can be downloaded via Julia REPL:
```
$ julia
julia> using Pkg
julia> Pkg.add("Plots")
```
Program can be run from the terminal:
```
$ julia mes_solver.jl
```
It is necessary to input one parameter: number of elements (points of division - 1) into which the interval will be divided:
```
>>> 100
```
