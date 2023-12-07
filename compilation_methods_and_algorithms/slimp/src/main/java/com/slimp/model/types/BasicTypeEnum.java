package com.slimp.model.types;

public enum BasicTypeEnum {
    INT("int", "int"),
    CHAR("char", "char"),
    BOOL("bool", "int"),
    FLOAT("float", "double");

    public final String identifier;
    public final String code;

    BasicTypeEnum(String identifier, String code) {
        this.code = code;
        this.identifier = identifier;
    }
}
