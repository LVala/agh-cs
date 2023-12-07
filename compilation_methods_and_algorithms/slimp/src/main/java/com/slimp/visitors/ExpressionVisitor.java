package com.slimp.visitors;

import java.util.List;

import com.slimp.CodeBuilder;
import com.slimp.generated.SlimpParser;
import com.slimp.generated.SlimpParserBaseVisitor;
import com.slimp.model.Function;
import com.slimp.model.FunctionRegister;
import com.slimp.model.VariableScope;
import com.slimp.model.FunctionRegister.FunctionDoesNotExist;
import com.slimp.model.VariableScope.VariableUndefined;
import com.slimp.model.types.*;
import com.slimp.utils.SlimpLogger;

import static com.slimp.model.types.BasicType.*;

public class ExpressionVisitor extends SlimpParserBaseVisitor<Type> {
    private FunctionRegister functionRegister;
    private VariableScope variableScope;
    private CodeBuilder codeBuilder;
    private boolean shouldWriteCode = true;

    public ExpressionVisitor(FunctionRegister functionRegister, VariableScope variableScope, CodeBuilder codeBuilder) {
        this.functionRegister = functionRegister;
        this.variableScope = variableScope;
        this.codeBuilder = codeBuilder;
    }

	@Override 
    public Type visitIdentifierExpression(SlimpParser.IdentifierExpressionContext ctx) { 
        String identifier = ctx.IDENTIFIER().getText();
        Type expressionType = null;

        try {
            expressionType = variableScope.getType(identifier);
        } catch (VariableUndefined e) {
            SlimpLogger.logError(
                "Undefined variable `" + identifier + "`", 
                ctx.getStart().getLine(), 
                ctx.getStart().getCharPositionInLine()
            );
            System.exit(1);
        }

        if (shouldWriteCode) {
            codeBuilder.append(variableScope.getScopeId(identifier) + identifier);
        }

        return expressionType;
    }

    @Override
    public Type visitExpressionElements(SlimpParser.ExpressionElementsContext ctx) {
        return visitChildren(ctx);
    }

    @Override
    public Type visitLiteralExpression(SlimpParser.LiteralExpressionContext ctx) { 
        // TODO need to map literal somehow and get its type
        Type literalType = null;

        SlimpParser.LiteralContext literal = ctx.literal();
        String code = literal.getText();

        if (literal.INTEGER_LITERAL() != null) {
            literalType = IntBasicType;
        } else if (literal.FLOAT_LITERAL() != null) {
            literalType = FloatBasicType;
        } else if (literal.CHAR_LITERAL() != null) {
            literalType = CharBasicType;
        } else if (literal.STRING_LITERAL() != null) {
            literalType = new StringType(120);
        } else if (literal.KW_FALSE() != null || literal.KW_TRUE() != null) {
            literalType = BoolBasicType;
            if (literal.KW_TRUE() != null) code = "1";
            else code = "0";
        }

        // temporary TODO
        if (literalType == null) {
            System.err.print("Invalid literal expression");
            System.exit(1);
        }

        if (shouldWriteCode)
            codeBuilder.append(code);
        return literalType;
    }

	@Override 
    public Type visitFunctionCallExpression(SlimpParser.FunctionCallExpressionContext ctx) { 
        String identifier = ctx.IDENTIFIER().getText();

        Function function; 
        if (identifier.equals("print")) {
            handlePrintFunction(ctx);
            return new NoType();
        } else {
            try {
                function = functionRegister.get(identifier);
                codeBuilder.append(identifier);
                codeBuilder.append("(");

                List<SlimpParser.ExpressionContext> paramExpressions = ctx.expressionElements().expression();
                if (function.getParameters().size() != paramExpressions.size()) {
                    SlimpLogger.logError(
                        "Invalid number of arguments in function call, exprected: " + function.getParameters().size(), 
                        paramExpressions.get(0).getStart().getLine(), 
                        paramExpressions.get(0).getStart().getCharPositionInLine()
                    );
                    System.exit(1);
                }

                boolean first = true;
                for (int i = 0; i < paramExpressions.size(); ++i) {
                    if (!first) {
                        codeBuilder.append(", ");

                    } else first = false;
                    Type paramType = visit(paramExpressions.get(i));
                    if (!paramType.equals(function.getParameters().get(i).type)) {
                        SlimpLogger.logError(
                            "Invalid number of arguments in function call, exprected: " + function.getParameters().size(), 
                            paramExpressions.get(i).getStart().getLine(), 
                            paramExpressions.get(i).getStart().getCharPositionInLine()
                        );
                        System.exit(1);
                    }
                }

                codeBuilder.append(")");
                return function.getReturnType();

            } catch (FunctionDoesNotExist e) {
                SlimpLogger.logError(
                    "Undefined function `" + identifier + "`", 
                    ctx.getStart().getLine(), 
                    ctx.getStart().getCharPositionInLine()
                );
                System.exit(1);
            }
        }
        return null;
    }

    private void handlePrintFunction(SlimpParser.FunctionCallExpressionContext ctx) {
        shouldWriteCode = false;
        
        CodeBuilder stringArgument = new CodeBuilder("", false);
        CodeBuilder restArguments = new CodeBuilder("", false);

        ExpressionVisitor printVisitor = new ExpressionVisitor(functionRegister, variableScope, restArguments);

        List<SlimpParser.ExpressionContext> paramExpressions = ctx.expressionElements().expression();
        for (int i=0; i<paramExpressions.size(); ++i) {            
            Type paramType = printVisitor.visit(paramExpressions.get(i));
            if (i != paramExpressions.size() - 1) {
                restArguments.append(", ");
            }

            if (paramType.equals(IntBasicType) || paramType.equals(BoolBasicType)) {
                // bool is printed as an int :(
                stringArgument.append("%d ");
            } else if (paramType.equals(FloatBasicType)) {
                stringArgument.append("%f ");
            } else if (paramType.equals(CharBasicType)) {
                stringArgument.append("%c ");
            } else if (paramType.equals(new StringType(120))) {
                stringArgument.append("%s ");
            }
        }
        stringArgument.append("\"");
        codeBuilder.append("printf(\"");
        codeBuilder.append(stringArgument.getCode());
        codeBuilder.append(", ");
        codeBuilder.append(restArguments.getCode());
        codeBuilder.append(")");
        shouldWriteCode = true;
    }

    @Override
    public Type visitIndexingExpression(SlimpParser.IndexingExpressionContext ctx) {
        // TODO
        return visitChildren(ctx); 
    }

	@Override 
    public Type visitTypeCastExpression(SlimpParser.TypeCastExpressionContext ctx) { 
        TypeVisitor typeVisitor = new TypeVisitor();
        Type castType = typeVisitor.visit(ctx.type());

        codeBuilder.append("(");
        codeBuilder.append(castType.mapToCode());
        codeBuilder.append(")");

        Type expressionType = visit(ctx.expression());
        if (!(expressionType instanceof BasicType) && !(castType instanceof BasicType)) {
            SlimpLogger.logError(
                "Non basic types cannot be cast", 
                ctx.getStart().getLine(), 
                ctx.getStart().getCharPositionInLine()
            );
            System.exit(1);
        }

        return castType; 
    }

	@Override 
    public Type visitLogicalExpression(SlimpParser.LogicalExpressionContext ctx) { 
        Type expressionTypeFirst;

        if (ctx.NOT() != null) {
            if (shouldWriteCode)
                codeBuilder.append(ctx.NOT().getText());
            expressionTypeFirst = visit(ctx.expression(0));
        } else {
        
            expressionTypeFirst = visit(ctx.expression(0));

            if (shouldWriteCode)
                codeBuilder.append(ctx.logicalOperator().getText());

            Type expressionTypeSecond = visit(ctx.expression(1));

            if (!expressionTypeFirst.equals(expressionTypeSecond)) {
                SlimpLogger.logError(
                    "Logical expression types does not match", 
                    ctx.getStart().getLine(), 
                    ctx.getStart().getCharPositionInLine()
                );
                System.exit(1);
            }
        }

        if (!(expressionTypeFirst.equals(new BasicType(BasicTypeEnum.BOOL)) )) {
            SlimpLogger.logError(
                "Conditional variable in `while` loop must be of type `bool`", 
                ctx.getStart().getLine(), 
                ctx.getStart().getCharPositionInLine()
            );
            System.exit(1);
        }

        return BoolBasicType;
    }

    @Override 
    public Type visitComparisonExpression(SlimpParser.ComparisonExpressionContext ctx) { 
        Type expressionTypeFirst = visit(ctx.expression(0));
        if (shouldWriteCode)
            codeBuilder.append(ctx.comparisonOperator().getText());
        Type expressionTypeSecond = visit(ctx.expression(1));

        if (!expressionTypeFirst.equals(expressionTypeSecond)) {
            SlimpLogger.logError(
                "Comparison expression types does not match", 
                ctx.getStart().getLine(), 
                ctx.getStart().getCharPositionInLine()
            );
            System.exit(1);
        }

        if (!(expressionTypeFirst.equals(new BasicType(BasicTypeEnum.INT)) || expressionTypeFirst.equals(new BasicType(BasicTypeEnum.FLOAT)))) {
            SlimpLogger.logError(
                "Only numeric types can be used in comparison expression", 
                ctx.getStart().getLine(), 
                ctx.getStart().getCharPositionInLine()
            );
            System.exit(1);    
        }

        return BoolBasicType;
    }

	@Override 
    public Type visitArithmeticExpression(SlimpParser.ArithmeticExpressionContext ctx) {
        Type expressionTypeFirst;

        if (ctx.MINUS() != null) {
            if (shouldWriteCode)
                codeBuilder.append(ctx.MINUS().getText());
            expressionTypeFirst = visit(ctx.expression(0));
        } else {
        
            expressionTypeFirst = visit(ctx.expression(0));

            if (shouldWriteCode)
                codeBuilder.append(ctx.arithmeticOperator().getText());

            Type expressionTypeSecond = visit(ctx.expression(1));

            if (!expressionTypeFirst.equals(expressionTypeSecond)) {
                SlimpLogger.logError(
                    "Arithmetic expression types does not match", 
                    ctx.getStart().getLine(), 
                    ctx.getStart().getCharPositionInLine()
                );
                System.exit(1);
            }
        }

        if (!(expressionTypeFirst.equals(new BasicType(BasicTypeEnum.INT)) || expressionTypeFirst.equals(new BasicType(BasicTypeEnum.FLOAT)))) {
            SlimpLogger.logError(
                "Only numeric types can be used in arithmetic expression", 
                ctx.getStart().getLine(), 
                ctx.getStart().getCharPositionInLine()
            );
            System.exit(1);        
        }

        if (ctx.arithmeticOperator() != null && ctx.arithmeticOperator().SLASH() != null)
            return FloatBasicType;

        return expressionTypeFirst;
    }

	@Override 
    public Type visitRangeExpression(SlimpParser.RangeExpressionContext ctx) {
        int lowerBound = 0;
        int upperBound = 0;
        try {
            lowerBound = Integer.parseInt(ctx.expression().get(0).getText());
            upperBound = Integer.parseInt(ctx.expression().get(1).getText());
        } catch (NumberFormatException e) {
            SlimpLogger.logError(
                "Only numeric types can be used in arithmetic expression", 
                ctx.getStart().getLine(), 
                ctx.getStart().getCharPositionInLine()
            );
            System.exit(1);
        }

        codeBuilder.append("{");
        for (int i = lowerBound; i <= upperBound ; i++) {
            if (i == upperBound) {
                codeBuilder.append(Integer.toString(i));
            } else {
                codeBuilder.append(i + ", ");
            }
        }
        codeBuilder.append("}");

        return new ListType(IntBasicType, upperBound - lowerBound + 1);
    }

    @Override 
    public Type visitParenthesizedExpression(SlimpParser.ParenthesizedExpressionContext ctx) {
        codeBuilder.append("(");

        Type expressionType = visit(ctx.expression());
        
        codeBuilder.append(")");

        return expressionType;
    }

	@Override 
    public Type visitTupleExpression(SlimpParser.TupleExpressionContext ctx) {
        // TODO
        return visitChildren(ctx); 
    }

	@Override 
    public Type visitArrayExpression(SlimpParser.ArrayExpressionContext ctx) {
        return visitChildren(ctx);
    }

	@Override 
    public Type visitMapExpression(SlimpParser.MapExpressionContext ctx) {
        // TODO
        return visitChildren(ctx); 
    }

    @Override
    public Type visitParentIdentifierExpression(SlimpParser.ParentIdentifierExpressionContext ctx) {
        String identifier = ctx.IDENTIFIER().getText();
        Type expressionType = null;

        try {
            expressionType = variableScope.getParentType(identifier);
        } catch (VariableUndefined e) {
            System.out.println("Variable " + identifier + " undefined");
        }

        if (shouldWriteCode)
            codeBuilder.append(variableScope.getParentScopeId(identifier) + identifier);

        return expressionType;
    }

    @Override
    protected Type aggregateResult(Type aggregate, Type nextResult) {
        if (nextResult != null) return nextResult;
        return aggregate;
    }
}
