package com.slimp.model.types;

public final class NoType extends Type {
    @Override
    public boolean equals(Type other) {
        if (other instanceof NoType otherNoType) return true;
        return false;
    }

    @Override
    public String mapToCode() {
        return "void";
    }

    @Override
    public String toString() {
        // TODO
        return "TODO";
    }
}
