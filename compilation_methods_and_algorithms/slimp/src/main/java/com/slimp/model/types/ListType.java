package com.slimp.model.types;

public final class ListType extends Type {
    public Type type;
    public int length;
    public String typeSuffix = "[]";

    public ListType(Type type, int length) {
        this.type = type;
        this.length = length;
        if (type instanceof ListType) {
            typeSuffix += ((ListType) type).typeSuffix;
        }
    }

    @Override
    public boolean equals(Type other) {
        if (other instanceof ListType otherListType) {
            if (this.length != otherListType.length) return false;
            return this.type.equals(otherListType.type);
        }
        return false;
    }

    @Override
    public String mapToCode() {
        return type.mapToCode() ;
    }

    @Override
    public String toString() {
        // TODO
        return "TODO";
    }
}
