package com.slimp.visitors;

import com.slimp.CodeBuilder;
import com.slimp.generated.SlimpParser;
import com.slimp.generated.SlimpParserBaseVisitor;
import com.slimp.model.Function;
import com.slimp.model.FunctionRegister;
import com.slimp.model.VariableScope;
import com.slimp.model.Function.Parameter;
import com.slimp.model.types.Type;
import com.slimp.utils.SlimpLogger;

public class ProgramVisitor extends SlimpParserBaseVisitor<Void> {
    private FunctionRegister functionRegister;
    private VariableScope variableScope;
    private CodeBuilder codeBuilder;


    public ProgramVisitor(FunctionRegister functionRegister, VariableScope variableScope, CodeBuilder codeBuilder) {
        this.functionRegister = functionRegister;
        this.variableScope = variableScope;
        this.codeBuilder = codeBuilder;
    }

    @Override
    public Void visitGlobalVariable(SlimpParser.GlobalVariableContext ctx) { 
        PatternVisitor patternVisitor = new PatternVisitor(variableScope, codeBuilder);
        Type variableType = patternVisitor.visit(ctx.pattern());

        codeBuilder.append(" = ");

        ExpressionVisitor expressionVisitor = new ExpressionVisitor(functionRegister, variableScope, codeBuilder);
        Type expressionType = expressionVisitor.visit(ctx.expression());

        if (!variableType.equals(expressionType)) {
            SlimpLogger.logError(
                "Cannot assign expression of type `" + expressionType.toString() + "` to variable of type `" + variableType.toString() + "`", 
                ctx.getStart().getLine(), 
                ctx.expression().getStart().getCharPositionInLine()
            );
            System.exit(1);
        }

        codeBuilder.append(";\n");
        return null; 
    }
    
    @Override
    public Void visitFunction(SlimpParser.FunctionContext ctx) {
        Function function = functionRegister.get(ctx.IDENTIFIER().getText());
        VariableScope functionVariableScope = new VariableScope(variableScope);
        writeFunctionDefinitionCode(function, functionVariableScope);

        BlockVisitor blockVisitor = new BlockVisitor(functionRegister, functionVariableScope, codeBuilder);

        codeBuilder.append("{\n");
        Type returnType = blockVisitor.visit(ctx.block());
        codeBuilder.append("}\n");

        if (!function.getReturnType().equals(returnType)) {
            SlimpLogger.logError(
                "`" + function.getIdentifier() + "`" + "function return type and type of returned value does not match", 
                ctx.getStart().getLine(), 
                ctx.type() != null ? ctx.type().getStart().getStartIndex() : ctx.RPAREN().getSymbol().getStartIndex() + 1
            );
            System.exit(1);
        }

        return null;
    }

    private void writeFunctionDefinitionCode(Function function, VariableScope functionVariableScope) {
        boolean first = true;

        codeBuilder.append(function.getReturnType().mapToCode());
        codeBuilder.append(" ");
        codeBuilder.append(function.getIdentifier());
        codeBuilder.append("(");

        for (Parameter parameter : function.getParameters()) {
            if (first) {
                first = false;
            } else {
                codeBuilder.append(", ");
            }
            codeBuilder.append(parameter.type.mapToCode());
            codeBuilder.append(" ");
            functionVariableScope.declareInScope(parameter.identifier, parameter.type);
            codeBuilder.append(functionVariableScope.getScopeId(parameter.identifier) +parameter.identifier);
        };
        codeBuilder.append(") ");
    }
}
