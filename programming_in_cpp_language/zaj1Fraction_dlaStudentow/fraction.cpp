#include <iostream>
#include <cstring>
#include <cctype>

using namespace std;

#include "fraction.h"

#if IMPLEMENTED_classFractionExists
#ifndef _MSC_FULL_VER // if not Visual Studio Compiler
    #warning "Klasa jest do zaimplementowania. Instrukcja w pliku naglowkowym"
#else
    #pragma message ("Klasa jest do zaimplementowania. Instrukcja w pliku naglowkowym")
#endif
#endif // IMPLEMENTED_classFractionExists

Fraction::Fraction(int num, int den) {
    numerator = num;
    denominator = den;
}

Fraction::Fraction(int num, int den, string fName) : fractionName(fName){
    numerator = num;
    denominator = den;
}

int Fraction::removedFractions_ = 0;
int Fraction::invalidDenominatorValue = 0;

void Fraction::load(std::istream& is) {
    string fraction;
    is >> fraction;

    string delimiter = "/";
    numerator = stoi(fraction.substr(0, fraction.find(delimiter)));
    denominator = stoi(fraction.substr(fraction.find(delimiter) + 1, fraction.length()));
}