package com.appverselite.app_service.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.util.List;

@Data
public class AiExplainResponse {

    private String summary;

    @JsonProperty("use_cases")
    private List<String> useCases;

    private List<String> benefits;
}