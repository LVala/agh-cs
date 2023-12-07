package com.slimp.model.types;

public final class BasicType extends Type {
    private BasicTypeEnum type;
    public BasicType(BasicTypeEnum type) {
        this.type = type;
    }

    @Override
    public boolean equals(Type other) {
        if (other instanceof BasicType otherGenericType) {
            return this.type == otherGenericType.type;
        }
        return false;
    }

    @Override
    public String mapToCode() {
        return type.code;
    }

    @Override
    public String toString() {
        return type.identifier;
    }

    public static BasicType BoolBasicType = new BasicType(BasicTypeEnum.BOOL);
    public static BasicType CharBasicType = new BasicType(BasicTypeEnum.CHAR);
    public static BasicType IntBasicType = new BasicType(BasicTypeEnum.INT);
    public static BasicType FloatBasicType = new BasicType(BasicTypeEnum.FLOAT);
}
