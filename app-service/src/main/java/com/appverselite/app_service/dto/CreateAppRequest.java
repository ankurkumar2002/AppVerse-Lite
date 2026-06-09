package com.appverselite.app_service.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class CreateAppRequest {

    @NotBlank
    private String name;

    @NotBlank
    private String description;

    @NotBlank
    private String category;
}