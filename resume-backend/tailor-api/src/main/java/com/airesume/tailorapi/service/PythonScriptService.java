package com.airesume.tailorapi.service;

import org.springframework.stereotype.Service;
import org.springframework.util.ResourceUtils;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

@Service
public class PythonScriptService {

    public String runScript(String resume, String jobDescription) {
        try {
            String pythonExecutable = "python";
            File scriptFile = ResourceUtils.getFile("classpath:scripts/tailor.py");
            String scriptPath = scriptFile.getAbsolutePath();

            ProcessBuilder processBuilder = new ProcessBuilder(pythonExecutable, scriptPath, resume, jobDescription);
            
            Process process = processBuilder.start();

            // Reads the standard output (contains the result OR the real error message)
            String output = new BufferedReader(
                new InputStreamReader(process.getInputStream()))
                .lines()
                .collect(Collectors.joining("\n"));

            // Reads the error stream (contains low-level warnings we want to ignore)
            String errorOutput = new BufferedReader(
                new InputStreamReader(process.getErrorStream()))
                .lines()
                .collect(Collectors.joining("\n"));

            if (!process.waitFor(5, TimeUnit.MINUTES)) {
                process.destroy();
                throw new RuntimeException("Python script execution timed out.");
            }

            int exitCode = process.exitValue();
            if (exitCode != 0) {
                // This is the key line: it shows the 'output' stream on an error.
                throw new RuntimeException("Python script exited with error code " + exitCode + ". Error: " + output);
            }

            // If successful, return the main output and ignore the error stream.
            return output;

        } catch (Exception e) {
            e.printStackTrace();
            return "Error: Could not process the resume. " + e.getMessage();
        }
    }
}