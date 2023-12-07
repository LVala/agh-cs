package com.slimp;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;

public class CodeBuilder {
    private String name;
    private StringBuilder programCode = new StringBuilder();
    
    public CodeBuilder(String name, boolean appendMacros) {
        this.name = name;
        if (appendMacros) {
            programCode.append("#include <stdio.h>\n");
            programCode.append("#define each(item, array, length) \\\n" +
                    "(typeof(*(array)) *p = (array), (item) = *p; p < &((array)[length]); p++, (item) = *p)\n");
        }
    }

    public void append(String str) {
        programCode.append(str);
    }

    public String getCode() {
        return programCode.toString();
    }

    public void writeToFile() {
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter(name + ".c"));
            writer.write(programCode.toString());
            writer.close();
        } catch (IOException e) {
            System.err.println("Unable to write C code to file: " + e);
            System.exit(1);
        }
    }

    public void compileToBinary() {
        ProcessBuilder pBuilder = new ProcessBuilder();
        // pBuilder.redirectError(Redirect.INHERIT);
        pBuilder.command("gcc", "-x", "c", "-O", "-Wall", "-Wextra", "-o", name, "-");

        try {
            Process process = pBuilder.start();
            OutputStream pos = process.getOutputStream();
            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(pos));
            writer.write(programCode.toString());
            writer.flush();
            pos.close();
            if (process.waitFor() != 0) throw new IOException("GCC finished with non-0 exit code");
        } catch (IOException|InterruptedException e) {
            System.err.println("C compilation failed: " + e.toString());
            System.exit(1);
        }
    }
}
