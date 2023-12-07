package com.slimp;

import com.slimp.generated.SlimpParser;
import com.slimp.listeners.FunctionDefListener;
import com.slimp.model.FunctionRegister;
import com.slimp.model.VariableScope;
import com.slimp.utils.SlimpErrorListener;
import com.slimp.utils.SlimpLogger;
import com.slimp.visitors.ProgramVisitor;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;

import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;

import org.apache.commons.cli.*;

public class Main {
    public static void main(String[] args) throws Exception {
        CommandLineParser cliParser = new DefaultParser();
        Options options = new Options();

        options.addOption("h", "help", false, "Show this help message");
        options.addOption("C", "ccode", false, "Output C code");
        options.addOption(Option.builder("o").longOpt("output").desc("Place output in <FILE>").hasArg().build());

        HelpFormatter helpFormatter = new HelpFormatter();
        helpFormatter.setArgName("FILE");
        String footer = "\nMore information on github.com/LVala/slimp";

        String inputFile = "";
        String outputFile = "a.out";
        boolean shouldCompile = true;

        try {
            CommandLine line = cliParser.parse(options, args);

            if (line.hasOption("help")) {
                System.out.println("Slimp compiler\n");
                helpFormatter.printHelp("slimp", "", options, footer, true);
                System.exit(0);
            }

            if (line.getArgs().length != 1) {
                System.out.println("Invalid argument: expected 1 positional argument - input file");
                System.exit(1);
            }

            inputFile = line.getArgs()[0];
            
            if (line.hasOption("output")) {
                outputFile = line.getOptionValue("output");
            }

            if (line.hasOption("ccode")) {
                shouldCompile = false;
            }
        } catch (ParseException exp) {
            System.out.println(exp.getMessage());
            System.out.println("Run 'slimp --help' to see a list of available options");
            System.exit(1);
        }

        InputStream inputStream = System.in;
        try {
            InputStream is = new FileInputStream(inputFile);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            is.transferTo(baos);
            SlimpLogger.setVariables(inputFile, new ByteArrayInputStream(baos.toByteArray()));
            inputStream = new ByteArrayInputStream(baos.toByteArray());
            is.close();
        } catch (FileNotFoundException exp) {
            SlimpLogger.logError(exp.getMessage(), -1, -1);
            SlimpLogger.logFailedMessage();
            System.exit(1);
        }
            
        CharStream input = CharStreams.fromStream(inputStream);

        com.slimp.generated.SlimpLexer lexer = new com.slimp.generated.SlimpLexer(input);
        lexer.removeErrorListeners();
        lexer.addErrorListener(new SlimpErrorListener());

        CommonTokenStream tokens = new CommonTokenStream(lexer);
        SlimpParser parser = new SlimpParser(tokens);
        parser.removeErrorListeners();
        parser.addErrorListener(new SlimpErrorListener());

        ParseTree tree = parser.program();
        
        CodeBuilder codeBuilder = new CodeBuilder(outputFile, true);
        FunctionRegister functionRegister = new FunctionRegister();
        VariableScope globalScope = new VariableScope(null);

        FunctionDefListener registrantListener = new FunctionDefListener(functionRegister, codeBuilder, parser);
        ParseTreeWalker walker = new ParseTreeWalker();
        walker.walk(registrantListener, tree);

        ProgramVisitor programVisitor = new ProgramVisitor(functionRegister, globalScope, codeBuilder);
        programVisitor.visit(tree);

        if (SlimpLogger.hasFailed()) {
            SlimpLogger.logFailedMessage();
            System.exit(1);
        }

        if (shouldCompile) {
            codeBuilder.compileToBinary();
        } else {
            codeBuilder.writeToFile();
        }
    }
}
