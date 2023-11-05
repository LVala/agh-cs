#ifndef FRACTION_H
#define FRACTION_H


/** @file fraction.h
 *  @brief Bardziej zlozona implementacja klasy Fraction (Ulamek):
1. Klasa powinna posiadac pola `numerator_` (licznik) i `denominator_` (mianownik).
   Najlepiej aby byly to zmienne calkowite.
2. Powinna zawierac jeden konstruktor ustawiajacy licznik (domyslnie na 0)
   i mianownik (domyslne na 1)
3. Gettery i settery do wartosci licznika i mianownika m.in.: `denominator()` i `setDenominator(...)`.
    - Prosze pamietac, ze gettery, jako metody nic nie zmieniajace powinny byc oznaczone jako metody stale.
    - W mysl zasady aby w razie potrzeby kod modyfikowac w mniejszej ilosci miejsc sugeruje aby
      typem zwracanym getterow bylo `auto`.
4. `operator+` dla ulamka zwracajacy ulamek przez kopie. Metoda stala.
5. `operator*` dla ulamka zwracajacy ulamek przez kopie. Metoda stala.
6. Niepoprawny mianownik (=0) powinien byc zglaszany przez wyjatek `std::invalid_argument`.
   Dotyczy to wszystkich miejsc, gdzie jest ustawiany mianownik.
7. Prosze o automatyczne skracanie ulamkow po operacji + i *
   Pomocny moze sie okazac algorytm euklidesa, oczywiscie tutaj robimy tylko dla przypadkow dodatnich.
   Zachecam do uzycia `std::gcd(...)`.
____________________________________________________________________________________
## Najczestrze pytania:
1. Czy w setterach skracać ułamki?
   Setter swoją nazwą mówi -ustawX, więc powinien to zrobić i nic więcej.
   Trochę dziwne byłoby zachowanie gdy użytkownik ustawia 1/4 na 2/4 i by nagle się mu zrobiło 1/2,
   mimo iż ustawiał tylko licznik na 2.
____________________________________________________________________________________
## Uwaga:
Wszystkie atrybuty powinny być prywatne, konstruktory i metody - publiczne,
metody większe niż 1-linijkowe powinny być zadeklarowane w klasie, zdefiniowane
poza klasą, obiekty typów klasowych powinny być w miarę możliwości przekazywane
w argumentach funkcji przez referencję, proszę też stosować słówko "const" w
odpowiednich miejscach.

Mozna tworzyc dowolna ilosc metod pomocniczych, jednakze aby byly one prywatne.

Gettery i settery operujace na liczbach, ktore nie rzucaja wyjatku, warto zadeklarowac jako `noexcept`.
**/


class Fraction
{
public:
    Fraction(int num = 0, int den = 1);
    int denominator() const {return denominator_;}
    void setDenominator(int den);
    int numerator() const {return numerator_;}
    void setNumerator(int num) {numerator_ = num;}
    Fraction operator +(const Fraction& other) const;
    Fraction operator *(const Fraction& other) const;
private: // members:
    int numerator_;
    int denominator_;
};


#endif // FRACTION_H
