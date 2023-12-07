package com.slimp.model;

import java.util.ArrayList;
import java.util.List;

import com.slimp.model.types.NoType;
import com.slimp.model.types.Type;

public class Function {
    public class Parameter {
        public String identifier;
        public Type type;

        public Parameter(String identifier, Type type) {
            this.identifier = identifier;
            this.type = type;
        }
    }

    private List<Parameter> parameters = new ArrayList<Parameter>();
    private String identifier;
    private Type returnType = new NoType();

    public void addToParameters(String identifier, Type type) {
        parameters.add(new Parameter(identifier, type));
    }

    public boolean checkIfParametersMatch(List<Type> otherParamTypes) {
        if (this.parameters.size() != otherParamTypes.size()) return false; 
        for (int i=0; i< this.parameters.size(); ++i) {
            if (!this.parameters.get(i).type.equals(otherParamTypes.get(i))) return false;
        }
        return true;
    }

    public Type getReturnType() {
        return returnType;
    }

    public void setReturnType(Type type) {
        this.returnType = type;
    }

    public void setIdentifier(String identifier) {
        this.identifier = identifier;
    }

    public String getIdentifier() {
        return identifier;
    }

    public List<Parameter> getParameters() {
        return parameters;
    }
}
