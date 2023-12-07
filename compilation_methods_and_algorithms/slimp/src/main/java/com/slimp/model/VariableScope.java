package com.slimp.model;

import java.util.HashMap;

import com.slimp.model.types.Type;

public class VariableScope extends HashMap<String, Type>{
    // you should be able to get from the parent as well, not implemented
    public class VariableException extends RuntimeException {
        private String identifier;

        public String getVariableID() {
            return identifier;
        }
    }

    public class VariableAlreadyDefined extends VariableException {
        public VariableAlreadyDefined(String identifier) {
            super.identifier = identifier;
        }
    }

    public class VariableUndefined extends VariableException {
        public VariableUndefined(String identifier) {
            super.identifier = identifier;
        }
    }

    static int ID = -1;
    private VariableScope parent;
    private final String scopeId;

    public VariableScope(VariableScope parent) {
        this.parent = parent;
        ID++;
        this.scopeId = "BLOCK" + ID + "_";
    }

    public boolean inScope(String identifier) {
        if (super.containsKey(identifier)) {
            return true;
        }
        return parent != null && parent.inScope(identifier);
    }

    public Type getType(String identifier) throws VariableUndefined {
        Type type = super.get(identifier);
        if (type == null && parent != null) type = parent.getType(identifier);
        if (type == null) throw new VariableUndefined(identifier);
        return type;
    }

    public Type getParentType(String identifier) throws VariableUndefined {
        if (parent == null) throw new VariableUndefined(identifier);
        Type type = parent.get(identifier);
        if (type == null) return parent.getParentType(identifier);
        return type;
    }

    public String getParentScopeId(String identifier) {
        if (parent == null) throw new RuntimeException("Parent does not exist");
        Type type = parent.get(identifier);
        if (type == null) return parent.getParentScopeId(identifier);
        return parent.scopeId;
    }

    public void declareInScope(String identifier, Type type) throws VariableAlreadyDefined {
        if (super.containsKey(identifier)) throw new VariableAlreadyDefined(identifier);
        super.put(identifier, type);
    }

    public String getScopeId(String identifier) {
        String scopeId = null;
        Type type = super.get(identifier);
        if (type != null) {
            scopeId = this.scopeId;
        }
        if (type == null && parent != null) {
            scopeId = parent.getScopeId(identifier);
        }
        if (scopeId == null) throw new VariableUndefined(identifier);
        return scopeId;
    }
}
