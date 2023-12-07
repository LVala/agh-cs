package com.slimp.listeners;

import com.slimp.CodeBuilder;
import com.slimp.generated.SlimpParser;
import com.slimp.generated.SlimpParserBaseListener;
import com.slimp.model.Function;
import com.slimp.model.FunctionRegister;
import com.slimp.model.Function.Parameter;
import com.slimp.model.FunctionRegister.FunctionAlreadyDefined;
import com.slimp.model.types.NoType;
import com.slimp.utils.SlimpLogger;
import com.slimp.visitors.TypeVisitor;

import org.antlr.v4.runtime.tree.ParseTreeWalker;

public class FunctionDefListener extends SlimpParserBaseListener {
    private FunctionRegister register;
    private CodeBuilder codeBuilder;
    private boolean registrantPassValid = true;
    ParseTreeWalker walker = new ParseTreeWalker();
    SlimpParser parser;

    public FunctionDefListener(FunctionRegister register, CodeBuilder codeBuilder, SlimpParser parser) {
        this.register = register;
        this.codeBuilder = codeBuilder;
        this.parser = parser;
    }

    @Override
    public void enterFunction(SlimpParser.FunctionContext ctx) {
        Function function = new Function();
        registerFunction(ctx, function);
        setParameters(ctx, function);
        setReturnType(ctx, function);

        writeFunctionPrototypeCode(function);
    }

    private void setReturnType(SlimpParser.FunctionContext ctx, Function function) {
        TypeVisitor typeVisitor = new TypeVisitor();
        function.setReturnType(ctx.type() == null ? new NoType() : typeVisitor.visit(ctx.type()));
    }

    private void setParameters(SlimpParser.FunctionContext ctx, Function function) {
        SlimpParser.FunctionParamsContext functionParamsContext = ctx.functionParams();
        TypeVisitor typeVisitor = new TypeVisitor();
        
        if (functionParamsContext != null) {
            for (SlimpParser.FunctionParamContext functionParam : functionParamsContext.functionParam()) {

                    function.addToParameters(
                        functionParam.typedIdentifier().IDENTIFIER().getText(),
                        typeVisitor.visit(functionParam.typedIdentifier().type())
                );
            }
        }
    }

    private void registerFunction(SlimpParser.FunctionContext ctx, Function function) {
        String identifier = ctx.IDENTIFIER().getText();
        try {
            register.registerFunction(identifier, function);
            function.setIdentifier(identifier);
        } catch (FunctionAlreadyDefined e) {
            SlimpLogger.logError(
                "Function with id: " + identifier + " had been already defined", 
                ctx.getStart().getLine(), 
                ctx.getStart().getCharPositionInLine()
            );
            System.exit(1);
            registrantPassValid = false;
        }
    }

    private void writeFunctionPrototypeCode(Function function) {
        if (!function.getIdentifier().equals("main")) {
            boolean first = true;

            codeBuilder.append(function.getReturnType().mapToCode());
            codeBuilder.append(" ");
            codeBuilder.append(function.getIdentifier());
            codeBuilder.append("(");

            for (Parameter parameter: function.getParameters()) {
                if (first) {
                    first = false;
                } else {
                    codeBuilder.append(", ");
                }
                codeBuilder.append(parameter.type.mapToCode());
            };
            codeBuilder.append(");\n");
        }
    }

    public boolean isRegistrantPassValid() {
        return registrantPassValid;
    }
}
