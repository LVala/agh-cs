#=
FEM problem solution for RRIR labs
Description in opracowanie_mes.pdf in this repo (in Polish)
Author: Łukasz Wala

to use Plots package, it needs to be installed via Julia REPL (described in README.md)
=#

using Plots

function gaussian_elimination(X::Array, b::Array)
    A = hcat(X, b)
    row_num = size(A, 1)
    for i = 1:row_num-1
        pivot = A[i,i]
        for j = i+1:row_num
            base = A[j,i] / pivot
            A[j,:] = A[j,:] - (base .* A[i,:])
        end
    end

    B = A[:, end]
    B[end] /= A[end, end-1]
    for i = row_num-1:-1:1
        pivot = A[i,i]
        B[i] -= sum(A[i,i+1:end-1] .* B[i+1:end])
        B[i] /= pivot
    end

    return B
end

# returns i-th point
x_i(i) = elemSize * i

# function rho
function p(x::Number)
    if x > 1 && x <=2
        return 1
    else
        return 0
    end
end

# returns function e_i(x)
function e_i(i::Integer)
    return function(x)
        if x > x_i(i-1) && x <= x_i(i)
            return (x - x_i(i-1)) / elemSize
        elseif x > x_i(i) && x < x_i(i+1)
            return (x_i(i+1) - x) / elemSize
        else
            return 0
        end
    end
end

# returns derivative of function e_i(x)
function de_i(i::Integer)
    return function(x)
        if x > x_i(i-1) && x <= x_i(i)
            return 1 / elemSize
        elseif x > x_i(i) && x < x_i(i+1)
            return -1 / elemSize
        else
            return 0
        end
    end
end

# integral calculation function
# uses Gauss–Legendre quadrature for 4 points
# with integration interval changed to [a,b]
const w12 = (18 + sqrt(30))/36
const w34 = (18 - sqrt(30))/36
function integrate(f, a::Number, b::Number)
    # new_x calculates new point after interval change
    new_x(x) = (b-a)/2 * x + (a+b)/2

    x1 = sqrt((3/7) - (2/7) * sqrt(6/5))
    x2 = x1
    x3 = sqrt((3/7) + (2/7) * sqrt(6/5))
    x4 = -x3

    return (b-a)/2 * (w12 * f(new_x(x1)) + w12 * f(new_x(x2)) + w34 * f(new_x(x3)) + w34 * f(new_x(x4)))
end

# preprocesing of the left side matrix of the system of equations
function X_preprocesing(X::Array)
    # values above the main diagonal
    # copied to symetrical positions
    for i = 1:n-2
        f_1(x) = de_i(i)(x) * de_i(i+1)(x)
        X[i,i+1] = -integrate(f_1, x_i(i), x_i(i+1))
        X[i+1,i] = X[i,i+1]
    end

    #values on the main diagonal
    f_2(x) = de_i(1)(x) * de_i(1)(x)
    X[1,1] = -integrate(f_2, x_i(0), x_i(2))
    for i = 2:n-1
        X[i,i] = X[1,1]
    end
end

# preprocesing of the right side matrix of the system of equations
function Y_preprocesing(Y::Array)
    for i = 1:n-1
        f_1(x) = e_i(i)(x) * p(x)
        res_1 = 4 * pi * G * (integrate(f_1, x_i(i-1), x_i(i)) + integrate(f_1, x_i(i), x_i(i+1)))
        f_2(x) = (-1/3) * de_i(i)(x)
        res_2 = (integrate(f_2, x_i(i-1), x_i(i)) + integrate(f_2, x_i(i), x_i(i+1)))
        Y[i] = res_1 + res_2
    end
end

# main function solving FEM
function fem()
    X = zeros(Float64, n-1, n-1)
    Y = Array{Float64}(undef, n-1)
    
    println("Matrices preprocesing...")
    X_preprocesing(X)
    Y_preprocesing(Y)
    
    println("Solving system of equations...")
    B = gaussian_elimination(X, Y)

    return function(x)
        res = 5 - (x/3)
        for i = 1:n-1
            res += B[i] * e_i(i)(x)
        end
        return res
    end
end

# plotting
function visualize(f)
    println("Creating plot...")
    X = [x_i(i-1) for i = 1:n+1]
    Y = zeros(Float64, n+1)
    Y[1] = 5
    Y[n+1] = 4
    for i = 2:n
       Y[i] = f(x_i(i-1)) 
    end

    # creating plot using Plots package
    plt = plot(X, Y, 
        title="Gravitational potential", 
        xlabel="x - distance from the point of mass", 
        label="Θ(x)",
        markershape = :auto,
        markersize = 3,
        margin = 3Plots.mm,
        seriescolor = "green",
        linecolor = "green",
        size=(1300,700))

    display(plt)
end

# input and constants
print(">>> ")
const n = parse(Int32, readline())
const rangeStart = 0
const rangeEnd = 3
const elemSize = (rangeEnd - rangeStart)/n
const G = 6.6743e-11

# solving FEM
theta = fem()

# visualization
visualize(theta)

# to make plot window not close instantly
print("Press enter to exit")
readline()
