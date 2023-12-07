package com.slimp.model.types;

public final class StringType extends Type {
    private ListType type;

    public StringType(int length) {
        this.type = new ListType(new BasicType(BasicTypeEnum.CHAR), length);
    }

    @Override
    public boolean equals(Type other) {
        if (other instanceof StringType otherStringType) {
          return this.type.equals(otherStringType.type);
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
