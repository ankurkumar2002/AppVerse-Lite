package com.appverselite.app_service.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class ExplainRequest {
    private String name;
    private String description;
    private String category;
}
