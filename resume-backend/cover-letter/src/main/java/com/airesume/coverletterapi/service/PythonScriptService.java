package com.airesume.coverletterapi.service;

import org.springframework.stereotype.Service;
import org.springframework.util.ResourceUtils;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

@Service
public class PythonScriptService {

    public String runScript(String resume, String jobDescription) {
        File resumeFile = null;
        File jdFile = null;
        try {
            // Create temporary files to hold the resume and job description
            resumeFile = File.createTempFile("resume-", ".txt");
            jdFile = File.createTempFile("jd-", ".txt");

            // Write the string content to the temporary files
            try (FileWriter resumeWriter = new FileWriter(resumeFile);
                 FileWriter jdWriter = new FileWriter(jdFile)) {
                resumeWriter.write(resume);
                jdWriter.write(jobDescription);
            }

            String pythonExecutable = "python";
            File scriptFile = ResourceUtils.getFile("classpath:scripts/coverletter.py");
            String scriptPath = scriptFile.getAbsolutePath();

            // *** CRITICAL CHANGE: Pass the file paths instead of the raw strings ***
            ProcessBuilder processBuilder = new ProcessBuilder(
                pythonExecutable, 
                scriptPath, 
                resumeFile.getAbsolutePath(), 
                jdFile.getAbsolutePath()
            );
            
            Process process = processBuilder.start();

            String output = new BufferedReader(new InputStreamReader(process.getInputStream()))
                .lines()
                .collect(Collectors.joining("\n"));

            if (!process.waitFor(5, TimeUnit.MINUTES)) {
                process.destroy();
                throw new RuntimeException("Python script execution timed out.");
            }

            int exitCode = process.exitValue();
            if (exitCode != 0) {
                String errorOutput = new BufferedReader(new InputStreamReader(process.getErrorStream()))
                    .lines()
                    .collect(Collectors.joining("\n"));
                throw new RuntimeException("Python script exited with error code " + exitCode + ". Stderr: " + errorOutput + " Stdout: " + output);
            }

            return output;

        } catch (Exception e) {
            e.printStackTrace();
            return "Error: Could not process the request. " + e.getMessage();
        } finally {
            // Clean up the temporary files after execution
            if (resumeFile != null) resumeFile.delete();
            if (jdFile != null) jdFile.delete();
        }
    }
}