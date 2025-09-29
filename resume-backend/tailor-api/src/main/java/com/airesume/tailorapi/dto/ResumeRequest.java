package com.airesume.tailorapi.dto;

import lombok.Data;

@Data
public class ResumeRequest {
    private String resume;
    private String jobDescription;
}