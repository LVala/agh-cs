#ifndef SHAPECOMPOSITE_H
#define SHAPECOMPOSITE_H

#include <memory>
#include "shape.h"

namespace Shapes {
    enum class ShapeOperation {INTERSECTION, SUM, DIFFERENCE};

    class ShapeComposite: public Shape {
        public:
            ShapeComposite(std::shared_ptr<Shape> shape1, std::shared_ptr<Shape> shape2, ShapeOperation op);
            bool isIn(int x, int y) const;

        private:
            std::shared_ptr<Shape> shape1;
            std::shared_ptr<Shape> shape2;
            ShapeOperation op;
    };
}

#endif