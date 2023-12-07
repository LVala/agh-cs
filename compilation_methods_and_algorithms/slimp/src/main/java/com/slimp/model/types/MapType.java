package com.slimp.model.types;

public final class MapType extends Type {
    private Type keyType;
    private Type valueType;

    public MapType(Type keyType, Type valueType) {
        this.keyType = keyType;
        this.valueType = valueType;
    }

    @Override
    public boolean equals(Type other) {
        if (other instanceof MapType otherMapType) {
            return this.keyType.equals(otherMapType.keyType) && this.valueType.equals(otherMapType.valueType);
        }
        return false;
    }

    @Override
    public String mapToCode() {
        return "TODO";  // TOOD
    }

    @Override
    public String toString() {
        // TODO
        return "TODO";
    }
}