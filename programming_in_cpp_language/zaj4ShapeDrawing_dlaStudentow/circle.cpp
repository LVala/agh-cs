#include "circle.h"

Shapes::Circle::Circle(int xCenter, int yCenter, int radius):
    xCenter(xCenter),
    yCenter(yCenter),
    radius(radius) {}

bool Shapes::Circle::isIn(int x, int y) const {
    return (x-xCenter)*(x-xCenter) + (y-yCenter)*(y-yCenter) <= radius*radius;
}