package com.slimp.model.types;

public abstract sealed class Type permits BasicType, TupleType, ListType, MapType, StringType, NoType {

    public abstract boolean equals(Type other);
    public abstract String mapToCode();
    public abstract String toString();
}