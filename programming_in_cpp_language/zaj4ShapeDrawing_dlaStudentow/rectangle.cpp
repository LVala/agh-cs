#include "rectangle.h"

Shapes::Rectangle::Rectangle(int xFrom, int yFrom, int xTo, int yTo):
x_coord(xFrom),
y_coord(yFrom),
xTo_coord(xTo),
yTo_coord(yTo) {}

bool Shapes::Rectangle::isIn(int x, int y) const {
    return x >= x_coord && x <= xTo_coord && y >= y_coord && y <= yTo_coord;
}