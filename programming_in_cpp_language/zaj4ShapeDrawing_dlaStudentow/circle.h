#ifndef CIRCLE_H
#define CIRCLE_H

#include "shape.h"

namespace Shapes {
class Circle: public Shape {
    public:
        Circle(int xCenter, int yCenter, int radius);
        bool isIn(int x, int y) const;
        int x() const {return xCenter;}
        int y() const {return yCenter;}
        int getRadius() const {return radius;}

    private:
        int xCenter;
        int yCenter;
        int radius;
};
}

#endif