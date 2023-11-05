#include "shapecomposite.h"

Shapes::ShapeComposite::ShapeComposite (std::shared_ptr<Shape> shape1, std::shared_ptr<Shape> shape2, ShapeOperation op):
shape1(shape1),
shape2(shape2),
op(op) {}

bool Shapes::ShapeComposite::isIn(int x, int y) const {
    switch(op) {
        case ShapeOperation::DIFFERENCE:
            return shape1->isIn(x, y) && !shape2->isIn(x, y);
        case ShapeOperation::SUM:
            return shape1->isIn(x, y) || shape2->isIn(x, y);
        case ShapeOperation::INTERSECTION:
            return shape1->isIn(x, y) && shape2->isIn(x, y);
    }
    return false;
}
