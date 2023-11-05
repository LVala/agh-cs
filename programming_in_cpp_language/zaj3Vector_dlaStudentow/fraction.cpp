#include <iostream>
#include <stdexcept> // std::out_of_range
#include <numeric> // std::gcd

#include "fraction.h"

Fraction::Fraction(int num, int den) {
    if (den == 0) throw std::invalid_argument("Denominator must not be 0");
    numerator_ = num;
    denominator_ = den;
}

void Fraction::setDenominator(int den) {
    if (den == 0) throw std::invalid_argument("Denominator must not be 0");
    denominator_ = den;
}

Fraction Fraction::operator +(const Fraction& other) const {
    Fraction new_fraction;

    new_fraction.setNumerator(numerator_ * other.denominator() + other.numerator() * denominator_);
    new_fraction.setDenominator(denominator_ * other.denominator());
    int gcd = std::gcd(new_fraction.denominator_, new_fraction.numerator_);
    new_fraction.setNumerator(new_fraction.numerator_/gcd);
    new_fraction.setDenominator(new_fraction.denominator_/gcd);
    return new_fraction;
}

Fraction Fraction::operator*(const Fraction& other) const {
    Fraction new_fraction;
    new_fraction.setNumerator(numerator_ * other.numerator());
    new_fraction.setDenominator(denominator_ * other.denominator());
    int gcd = std::gcd(new_fraction.denominator_, new_fraction.numerator_);
    new_fraction.setNumerator(new_fraction.numerator_/gcd);
    new_fraction.setDenominator(new_fraction.denominator_/gcd);
    return new_fraction;
}
