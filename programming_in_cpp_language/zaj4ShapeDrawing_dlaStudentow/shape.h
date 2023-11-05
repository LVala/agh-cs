#ifndef SHAPE_H
#define SHAPE_H

/** @file stage.h
@brief Implementacja klasy czysto abstrakcyjnej `Shape`, majacej funkcje:
1. `bool isIn(int x, int y) const = 0;`, ktora zwraca informacje czy dany punkt jest wewnatrz figury czy nie
2. Proszę zaimplementować klasę `Rectangle` dziedziczącą po `Shape` i implementującą powyższą metodę.
   Implementacja klasy powinna być dokonana w nowo-utworzonych plikach: rectangle.h i rectangle.cpp
3. Proszę zaimplementować klasę `Circle` dziedziczącą po `Shape` i implementującą jej metodę.
   Implementacja klasy powinna być dokonana w nowo-utworzonych plikach: circle.h i circle.cpp
4. Proszę zaimplementować klasę-kompozyt `ShapeComposite` dziedziczącą po `Shape` i implementującą jej metodę.
   Klasa ta w konstruktorze powinna przyjąć:
    - dwie instancje `shared_ptr<Shape>`
    - operacje na zbiorach `enum class ShapeOperation`: `INTERSECTION`, `SUM`, `DIFFERENCE`
    - w oparciu o to bedzie mozna cala hierarchie figur polaczyc w jedno drzewo,
      dla ktorego bedzie mozna zapytac czy dany punkt jest w hierarchii, czy nie (metoda `isIn`).
5. Opcjonalnie mozna sobie zaimplementowac klase `Stage` rysujaca na konsole.
________________________
Przyklad obrazka jaki można osiągnąć komponując dwa kształty przy pomocy operacji na zbiorach:
```
     21:            *******
     20:          ***********
     19:         *************
     18:        ***************
     17:       *****************
     16:      *******************
     15:      *******************
     14:     *********************
     13:     *********************
     12:     ***      ***      ***
     11:     ***      ***      ***
     10:     ***      ***      ***
      9:     ***      ***      ***
      8:     ***      ***      ***
      7:     ***      ***      ***
      6:     ***      ************
      5:     ***      ************
      4:     ***      ************
      3:     ***      ************
      2:     ***      ************
      1:     *********************
```
____________________________________________________________________________________
## Uwaga:
Wszystkie atrybuty powinny być prywatne, konstruktory i metody - publiczne,
metody większe niż 1-linijkowe powinny być zadeklarowane w klasie, zdefiniowane
poza klasą, obiekty typów klasowych powinny być w miarę możliwości przekazywane
w argumentach funkcji przez referencję, proszę też stosować słówko "const" w
odpowiednich miejscach.
@note Co się da na listę inicjalizacyjną konstruktora.

Mozna tworzyc dowolna ilosc metod pomocniczych, jednakze aby byly one prywatne.
**/

namespace Shapes
{
struct Point
{
    int x_, y_;
};

class Shape
{
    public:
        virtual bool isIn(int x, int y) const = 0;
        virtual ~Shape() {}
};
} // namespace Shapes

#endif // SHAPE_H
