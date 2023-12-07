package com.slimp.visitors;

import com.slimp.CodeBuilder;
import com.slimp.generated.SlimpParser;
import com.slimp.generated.SlimpParserBaseVisitor;
import com.slimp.model.VariableScope;
import com.slimp.model.VariableScope.VariableAlreadyDefined;
import com.slimp.model.VariableScope.VariableUndefined;
import com.slimp.model.types.ListType;
import com.slimp.model.types.Type;
import com.slimp.utils.SlimpLogger;

public class PatternVisitor extends SlimpParserBaseVisitor<Type> {
    private VariableScope variableScope;
    private CodeBuilder codeBuilder;

    public PatternVisitor(VariableScope variableScope, CodeBuilder codeBuilder) {
        this.codeBuilder = codeBuilder;
        this.variableScope = variableScope;
    }

    @Override 
    public Type visitUntypedPatternIdentifier(SlimpParser.UntypedPatternIdentifierContext ctx) {
        String identifier = ctx.IDENTIFIER().getText();
        Type type = null; 
        
        try {
            type = variableScope.getType(identifier);
        } catch (VariableUndefined e) {
            SlimpLogger.logError(
                "Variable " + identifier +" was not defined", 
                ctx.getStart().getLine(), 
                ctx.getStart().getCharPositionInLine()
            );
            System.exit(1);
        }

        codeBuilder.append(variableScope.getScopeId(identifier) + ctx.IDENTIFIER().getText());
        
        return type; 
    }

	@Override public Type visitTypedPatternIdentifier(SlimpParser.TypedPatternIdentifierContext ctx) {
        TypeVisitor typeVisitor = new TypeVisitor();

        String identifier = ctx.typedIdentifier().IDENTIFIER().getText();
        Type type = typeVisitor.visit(ctx.typedIdentifier().type());

        try {
            variableScope.declareInScope(identifier, type);  // possible but when using in its initialization
        } catch (VariableAlreadyDefined e) {
            SlimpLogger.logError(
                "Variable " + identifier +" already declared", 
                ctx.getStart().getLine(), 
                ctx.getStart().getCharPositionInLine()
            );
            System.exit(1);
        }

        codeBuilder.append(type.mapToCode());
        codeBuilder.append(" ");
        codeBuilder.append(variableScope.getScopeId(identifier) + identifier);
        if (type instanceof ListType) {
            codeBuilder.append("[" + ((ListType) type).length + "]");
        }
        
        return type;
    }

    // TODO rest of the cases

    protected String aggregateResult(String aggregate, String nextResult) {
        // analogical situation to aggregateResult in BlockVisitor

        if (nextResult != null) return nextResult;
        return aggregate;
	}
    
}
