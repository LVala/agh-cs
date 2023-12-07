package com.slimp.utils;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

public class SlimpLogger {
    private static final String ANSI_RED = "\033[1;91m";
    private static final String ANSI_YELLOW = "\033[1;93m";
    private static final String ANSI_BOLD = "\033[1m";
    private static final String ANSI_BOLD_RESET = "\033[22m";
    private static final String ANSI_RESET_COLOR = "\033[0m";

    private static String name;
    private static String[] lines;
    private static int errorNo = 0;
    private static int warningNo = 0;

    public static void setVariables(String fileName, InputStream is) {
        name = fileName;
        lines = new BufferedReader(new InputStreamReader(is)).lines().toArray(String[]::new);
    }

    private static void logMessage(String message, int lineNum, int colNum, String colorStart, String colorReset) {
        int whitespaces = String.valueOf(lineNum).length() + colNum + 6;
        
        System.err.print(colorStart + "error: " + colorReset);
        System.err.println(ANSI_BOLD + message + ANSI_BOLD_RESET);
        if (lineNum >= 0 && colNum >= 0) {
            System.err.println("  --> " + name + ":" + lineNum + ":" + colNum);
            System.err.println("   " + lineNum + " | " + lines[lineNum-1]);
            System.err.format("%1$"+whitespaces+"s" + colorStart + "^here" + colorReset + "\n", "", "");
        }
    }

    public static void logError(String message, int lineNum, int colNum) {
        logMessage(message, lineNum, colNum, ANSI_RED, ANSI_RESET_COLOR);
        ++errorNo;
    }

    public static void logWarning(String message, int lineNum, int colNum) {
        logMessage(message, lineNum, colNum, ANSI_YELLOW, ANSI_RESET_COLOR);
        ++warningNo;
    }

    public static boolean hasFailed() {
        return (errorNo != 0);
    }

    public static void logFailedMessage() {
        System.out.println("\nCompilation failed: " + errorNo + " error(s), " + warningNo + " warning(s)");
    }
}
