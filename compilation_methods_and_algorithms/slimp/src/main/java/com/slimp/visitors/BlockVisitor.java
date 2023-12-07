package com.slimp.visitors;

import com.slimp.CodeBuilder;
import com.slimp.generated.SlimpParser;
import com.slimp.generated.SlimpParserBaseVisitor;
import com.slimp.model.FunctionRegister;
import com.slimp.model.VariableScope;
import com.slimp.model.types.*;
import com.slimp.utils.SlimpLogger;

import static com.slimp.model.types.BasicType.BoolBasicType;

public class BlockVisitor extends SlimpParserBaseVisitor<Type> {
    private FunctionRegister functionRegister;
    private VariableScope variableScope;
    private CodeBuilder codeBuilder;

    public BlockVisitor(FunctionRegister functionRegister, VariableScope variableScope, CodeBuilder codeBuilder) {
        this.functionRegister = functionRegister;
        this.variableScope = variableScope;
        this.codeBuilder = codeBuilder;
    }

    @Override 
    public Type visitEmptyStatement(SlimpParser.EmptyStatementContext ctx) { 
        codeBuilder.append(";\n");
        return new NoType();
    }

    @Override 
    public Type visitAssignmentStatement(SlimpParser.AssignmentStatementContext ctx) { 
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
        
        return new NoType();
    }

    @Override 
    public Type visitExpressionStatement(SlimpParser.ExpressionStatementContext ctx) { 
        ExpressionVisitor expressionVisitor = new ExpressionVisitor(functionRegister, variableScope, codeBuilder);
        expressionVisitor.visit(ctx.expression());
        codeBuilder.append(";\n");

        return new NoType();
    }

    @Override 
    public Type visitReturnStatement(SlimpParser.ReturnStatementContext ctx) { 
        if (ctx.expression() == null) return new NoType();
        ExpressionVisitor expressionVisitor = new ExpressionVisitor(functionRegister, variableScope, codeBuilder);
        codeBuilder.append("return ");
        Type expressionType = expressionVisitor.visit(ctx.expression());
        codeBuilder.append(";\n");
        return expressionType;
    }

	@Override 
    public Type visitLoopControlStatement(SlimpParser.LoopControlStatementContext ctx) { 
        codeBuilder.append(ctx.getText() + ";\n");
        // TODO can only appear inside of a loop block
        return new NoType();
    }

    @Override 
    public Type visitIfStatement(SlimpParser.IfStatementContext ctx) { 
        codeBuilder.append("if (");

        ExpressionVisitor expressionVisitor = new ExpressionVisitor(functionRegister, variableScope, codeBuilder);
        Type expressionType = expressionVisitor.visit(ctx.expression());
        if (!expressionType.equals(new BasicType(BasicTypeEnum.BOOL))) {
            SlimpLogger.logError(
                "Conditional variable in `if` statement must be of type `bool`", 
                ctx.getStart().getLine(), 
                ctx.expression().getStart().getCharPositionInLine()
            );
            System.exit(1);
        }

        codeBuilder.append(")");

        codeBuilder.append("{\n");
        BlockVisitor blockVisitor = new BlockVisitor(functionRegister, new VariableScope(variableScope), codeBuilder);
        Type returnType = blockVisitor.visit(ctx.block(0));
        codeBuilder.append("}\n");

        if (ctx.KW_ELSE() != null) {
            codeBuilder.append(" else ");
            if (ctx.block().size() > 1 || ctx.ifStatement() != null) {
                codeBuilder.append("{\n");
                BlockVisitor elseBlockVisitor = new BlockVisitor(functionRegister, new VariableScope(variableScope), codeBuilder);
                Type elseReturnType = elseBlockVisitor.visit(ctx.block().size() > 1 ? ctx.block(1) : ctx.ifStatement());
                codeBuilder.append("}\n");
                if (
                    !(returnType.equals(new NoType()) ||
                    elseReturnType.equals(new NoType())) && 
                    !returnType.equals(elseReturnType) 
                    ) {
                        // TODO kinda hard to print nice error message without the knowledge of where the return statement is
                        SlimpLogger.logError(
                            "Multiple return statements with values of different types inside single function", 
                            ctx.block(1).getStart().getLine(),
                            ctx.block(1).getStart().getCharPositionInLine()
                        );
                        System.exit(1);
                }
                
                if (!elseReturnType.equals(new NoType())) return elseReturnType;
            }
        }

        // TODO if theres return in block, there must be a return outside of it as well
        return returnType;
    }

    @Override 
    public Type visitForLoop(SlimpParser.ForLoopContext ctx) {
        VariableScope newVariableScope = new VariableScope(variableScope);
        BlockVisitor blockVisitor = new BlockVisitor(functionRegister, newVariableScope, codeBuilder);

        CodeBuilder expressionCodeBuilder = new CodeBuilder("", false);
        ExpressionVisitor expressionVisitor = new ExpressionVisitor(functionRegister, variableScope, expressionCodeBuilder);
        Type expressionType = expressionVisitor.visit(ctx.expression());

        // my eyes hurt from looking at this
        if (ctx.expression().getText().startsWith("[")) {
            codeBuilder.append(expressionType.mapToCode());
            codeBuilder.append(" __FOR_LOOP_TEMP__[] = ");
            codeBuilder.append(expressionCodeBuilder.getCode());
            codeBuilder.append(";\n");
        } else {
            codeBuilder.append(expressionType.mapToCode());
            codeBuilder.append(" *__FOR_LOOP_TEMP__ = ");
            codeBuilder.append(expressionCodeBuilder.getCode());
            codeBuilder.append(";\n");
        }

        if (expressionType instanceof ListType) {
            // another awful hack
            String iteratorIdentifier = ctx.IDENTIFIER().getText();
            Type typeInList = ((ListType) expressionType).type;
            int length = ((ListType) expressionType).length;
            newVariableScope.declareInScope(iteratorIdentifier, typeInList);
            codeBuilder.append(typeInList.mapToCode());
            codeBuilder.append(" ");
            codeBuilder.append(newVariableScope.getScopeId(iteratorIdentifier) + iteratorIdentifier);
            codeBuilder.append(";\n");

            codeBuilder.append("for each (");
            codeBuilder.append(newVariableScope.getScopeId(iteratorIdentifier) + iteratorIdentifier);
            codeBuilder.append(",");
            codeBuilder.append("__FOR_LOOP_TEMP__");
            codeBuilder.append(",");
            codeBuilder.append(Integer.toString(length));
        } else {
            SlimpLogger.logError(
                "Expression must be enumerable",
                ctx.expression().getStart().getLine(),
                ctx.expression().getStart().getCharPositionInLine()
            );
            System.exit(1);
        }

        codeBuilder.append(")");

        codeBuilder.append("{\n");
        blockVisitor.visit(ctx.block());
        codeBuilder.append("}\n");

        return new NoType();
    }

    @Override 
    public Type visitWhileLoop(SlimpParser.WhileLoopContext ctx) {
        ExpressionVisitor expressionVisitor = new ExpressionVisitor(functionRegister, variableScope, codeBuilder);
        BlockVisitor blockVisitor = new BlockVisitor(functionRegister, new VariableScope(variableScope), codeBuilder);

        codeBuilder.append("while ");
        codeBuilder.append("(");
        Type expressionType = expressionVisitor.visit(ctx.expression());
        if (!expressionType.equals(BoolBasicType)) {
            SlimpLogger.logError(
                "Conditional variable in `while` loop must be of type `bool`", 
                ctx.getStart().getLine(), 
                ctx.expression().getStart().getCharPositionInLine()
            );
            System.exit(1);
        }
        codeBuilder.append(")");
        codeBuilder.append("{\n");
        blockVisitor.visit(ctx.block());
        codeBuilder.append("}\n");

        return new NoType();
    }

    protected Type defaultResult() {
		return new NoType();
	}

    protected Type aggregateResult(Type aggregate, Type nextResult) {
        // this method is used in default implementation of visitChildren
        // default aggregateResults simply returns nextResult
        // which is desired in this case, as the goal is to get type of last statement in block
        // but is is called also on opening and closing brackets which should be prevented
        if (!aggregate.equals(new NoType()) && !nextResult.equals(new NoType()) && !nextResult.equals(aggregate)) {
            // TODO better error message
            SlimpLogger.logError(
                "Multiple return statements with values of different types inside single function", 
                -1,
                -1
            );
            System.exit(1);
        }
        if (!nextResult.equals(new NoType())) return nextResult;

        return aggregate;
	}
}
