// author: Grzegorz Prowadzacy

#include <algorithm>
#include <stdexcept>
#include <utility> // std::swap()
#include <iostream>

#include "vector.h"
#include "fraction.h"

Vector::Vector(std::size_t initial_size) {
    data_ = new Fraction[initial_size];
    size_ = 0;
    capacity_ = initial_size;
}

Vector::~Vector() {
    delete[] data_;
}

Vector::Vector(const Vector& other) {
    size_ = other.size_;
    capacity_ = other.capacity_;
    data_ = new Fraction[capacity_];
    for (int i=0; i<size_; ++i) {
        data_[i] = other.data_[i];
    }
}

Vector::Vector(Vector&& other) noexcept : Vector() {
    swap(*this, other);
}

void swap(Vector& first, Vector& second) {
    using std::swap;
    swap(first.size_, second.size_);
    swap(first.capacity_, second.capacity_);
    swap(first.data_, second.data_);
}

Vector& Vector::operator= (Vector other) {
    swap(*this, other);
    return *this;
}

void Vector::push_back(Fraction new_elem) {
    if (size_ == capacity_) {
        Fraction *new_data = new Fraction[capacity_ + 1];
        for (int i=0; i<size_; ++i) {
            new_data[i] = data_[i];
        }
        delete[] data_;
        data_ = new_data;
        capacity_ = capacity_ + 1;
    }
    data_[size_] = new_elem;
    ++size_;
}

Fraction Vector::operator[](std::size_t index) {
    if (index >= size_ || index < 0)
        throw std::out_of_range("Index out of range");
    
    return data_[index];
}

Fraction Vector::operator[](std::size_t index) const {
    if (index >= size_ || index < 0)
        throw std::out_of_range("Index out of range");
    
    return data_[index];
}
