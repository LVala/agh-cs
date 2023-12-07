package com.slimp.model;

import java.util.HashMap;

public class FunctionRegister extends HashMap<String, Function> {
    public class FunctionException extends RuntimeException {
        private String identifier;

        public String getFunctionID() {
            return identifier;
        }
    }

    public class FunctionAlreadyDefined extends FunctionException {
        public FunctionAlreadyDefined(String identifier) {
            super.identifier = identifier;
        }
    }

    public class FunctionDoesNotExist extends FunctionException {
        public FunctionDoesNotExist(String identifier) {
            super.identifier = identifier;
        }
    }

    public void registerFunction(String identifier, Function function) throws FunctionAlreadyDefined {
        if (super.containsKey(identifier)) {
            throw new FunctionAlreadyDefined(identifier);
        }
        super.put(identifier, function);
    }

    public boolean isFunction(String identifier) {
        return super.containsKey(identifier);
    }

    public Function get(String identifier) throws FunctionDoesNotExist {
        if (!isFunction(identifier)) throw new FunctionDoesNotExist(identifier);
        return super.get(identifier);
    }
}
