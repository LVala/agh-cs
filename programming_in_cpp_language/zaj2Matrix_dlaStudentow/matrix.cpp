#include <iostream>
#include <string>

using namespace std;

#include "matrix.h"

TwoDimensionMatrix::TwoDimensionMatrix() {
    for (int i=0;i<size;++i)
        for (int j=0;j<size;++j)
            this->matrix[i][j] = 0;
}

TwoDimensionMatrix::TwoDimensionMatrix(const MatrixElement array[size][size]) {
    for (int i=0;i<size;++i)
        for (int j=0;j<size;++j)
            this->matrix[i][j] = array[i][j];
}

TwoDimensionMatrix::TwoDimensionMatrix(const TwoDimensionMatrix &obj) {
    for (int i=0;i<size;++i)
        for (int j=0;j<size;++j)
            this->matrix[i][j] = obj.get(i, j);
}

std::ostream& operator << (std::ostream &stream, const TwoDimensionMatrix &matrix) {
    for (int i=0;i<matrix.size;++i) {
        for (int j=0;j<matrix.size;++j)
            stream << matrix.matrix[i][j] << " ";
        stream << "\n";
    }
    return stream;
}

std::istream& operator >> (std::istream &stream, TwoDimensionMatrix &matrix) {
    for (int i=0;i<matrix.size;++i)
        for (int j=0;j<matrix.size;++j)
            stream >> matrix.matrix[i][j];


    return stream;
}

TwoDimensionMatrix operator+(const TwoDimensionMatrix& matrix1, const TwoDimensionMatrix& matrix2) {
    TwoDimensionMatrix new_matrix;
    for (int i=0;i<matrix1.getSize();++i)
        for (int j=0;j<matrix1.getSize();++j)
            new_matrix.set(i, j, matrix1.get(i,j) + matrix2.get(i,j));
    return new_matrix;
}

TwoDimensionMatrix& TwoDimensionMatrix::operator*=(MatrixElement number) {
    for (int i=0;i<size;++i)
        for (int j=0;j<size;++j)
            this->matrix[i][j] *= number;
    return *this;
}

TwoDimensionMatrix TwoDimensionMatrix::operator&&(const TwoDimensionMatrix& matrix) const {
    TwoDimensionMatrix new_matrix;
    for (int i=0;i<size;++i)
        for (int j=0;j<size;++j)
            new_matrix.set(i,j, this->matrix[i][j] & matrix.get(i,j));
    return new_matrix;
}

const MatrixElement* TwoDimensionMatrix::operator[](size_t i) const {
    return matrix[i];
}

MatrixElement* TwoDimensionMatrix::operator[](size_t i) {
    return matrix[i];
}

TwoDimensionMatrix::operator size_t() const {
    return this->getSize();
}
