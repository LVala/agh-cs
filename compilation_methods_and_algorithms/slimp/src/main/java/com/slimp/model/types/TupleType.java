package com.slimp.model.types;

import java.util.List;

public final class TupleType extends Type {
    private List<Type> types;

    public TupleType(List<Type> types) {
        this.types = types;
    }

    @Override
    public boolean equals(Type other) {
        if (other instanceof TupleType otherTupleType) {
            if (types.size() != otherTupleType.types.size()) return false;
            for (int i=0; i<types.size(); ++i) {
                if (!types.get(i).equals(otherTupleType.types.get(i))) return false;
            }
            return true;
        }
        return false;
    }
    
    @Override
    public String mapToCode() {
        return "TODO";
    }

    @Override
    public String toString() {
        // TODO
        return "TODO";
    }
}
