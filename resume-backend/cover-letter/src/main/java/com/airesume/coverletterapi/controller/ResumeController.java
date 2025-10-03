package com.airesume.coverletterapi.controller;

import com.airesume.coverletterapi.dto.ResumeRequest;
import com.airesume.coverletterapi.dto.CoverLetterResumeResponse;
import com.airesume.coverletterapi.service.PythonScriptService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin(origins = "http://localhost:5173")
@RestController
@RequestMapping("/api")
public class ResumeController {

    @Autowired
    private PythonScriptService pythonScriptService;

    @PostMapping("/generate-cover-letter")
    public ResponseEntity<CoverLetterResumeResponse> generateCoverLetter(@RequestBody ResumeRequest request) {
        
        String generatedCoverLetter = pythonScriptService.runScript(
                request.getResume(),
                request.getJobDescription()
        );

        CoverLetterResumeResponse response = new CoverLetterResumeResponse();
        response.setGeneratedCoverLetter(generatedCoverLetter);

        return ResponseEntity.ok(response);
    }
}