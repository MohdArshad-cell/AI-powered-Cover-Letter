package com.airesume.tailorapi.controller;

import com.airesume.tailorapi.dto.ResumeRequest;
import com.airesume.tailorapi.dto.TailoredResumeResponse;
import com.airesume.tailorapi.service.PythonScriptService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.CrossOrigin;

@CrossOrigin(origins = "http://localhost:5173")
@RestController
@RequestMapping("/api")
public class ResumeController {

    @Autowired
    private PythonScriptService pythonScriptService;

    @PostMapping("/tailor-resume")
    public ResponseEntity<TailoredResumeResponse> tailorResume(@RequestBody ResumeRequest request) {
        
        String tailoredResumeFromPython = pythonScriptService.runScript(
                request.getResume(),
                request.getJobDescription()
        );

        TailoredResumeResponse response = new TailoredResumeResponse();
        response.setTailoredResume(tailoredResumeFromPython);

        return ResponseEntity.ok(response);
    }
}