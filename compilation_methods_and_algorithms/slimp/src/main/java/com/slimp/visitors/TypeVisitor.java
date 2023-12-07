package com.slimp.visitors;

import com.slimp.generated.SlimpParser;
import com.slimp.generated.SlimpParserBaseVisitor;
import com.slimp.model.types.*;
import com.slimp.utils.SlimpLogger;

public class TypeVisitor extends SlimpParserBaseVisitor<Type> {
    public class UnsupportedType extends RuntimeException {
        private String identifier;

        public UnsupportedType(String identifier) {
            this.identifier = identifier;
        }

        public String getTypeID() {
            return identifier;
        }
    }

    @Override 
    public Type visitTypeIdentifier(SlimpParser.TypeIdentifierContext ctx) { 
        String identifier = ctx.IDENTIFIER().getText();

        for (BasicTypeEnum type: BasicTypeEnum.values()) {
            if (type.identifier.equals(identifier)) return new BasicType(type);
        }

        throw new UnsupportedType(identifier);
    }

    @Override 
    public Type visitParenthesizedType(SlimpParser.ParenthesizedTypeContext ctx) {


        
        return visitChildren(ctx); 
    }

    @Override 
    public Type visitTupleType(SlimpParser.TupleTypeContext ctx) {
        // TODO
        if (ctx.tupleTypeElements().type().isEmpty()) return new NoType();
        return visitChildren(ctx); 
    }

    @Override 
    public Type visitArrayType(SlimpParser.ArrayTypeContext ctx) {
        Type type = visit(ctx.type());
        int length = 0;
        try {
            length = Integer.parseInt(ctx.expression().getText());
            if (length <= 0 ) throw new NumberFormatException();
        } catch (NumberFormatException e) {
            SlimpLogger.logError(
                "Array length must be positive", 
                ctx.getStart().getLine(), 
                ctx.getStart().getCharPositionInLine()
            );
            System.exit(1);
        }

        return new ListType(type, length);
    }

    @Override 
    public Type visitMapType(SlimpParser.MapTypeContext ctx) {
        // TODO
        return visitChildren(ctx); 
    }

    @Override 
    public Type visitTupleTypeElements(SlimpParser.TupleTypeElementsContext ctx) {
        // TODO
        return visitChildren(ctx); 
    }
}