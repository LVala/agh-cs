#ifndef RECTANGLE_H
#define RECTANGLE_H

#include "shape.h"

namespace Shapes {
class Rectangle: public Shape {
    public:
        Rectangle(int xFrom, int yFrom, int xTo, int yTo);
        bool isIn(int x, int y) const;
        int x() const {return x_coord;};
        int y() const {return y_coord;};
        int xTo() const {return xTo_coord;};
        int yTo() const {return yTo_coord;};

    private:
        int x_coord;
        int y_coord;
        int xTo_coord;
        int yTo_coord;
};
}

#endif