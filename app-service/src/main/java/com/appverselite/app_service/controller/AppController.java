package com.appverselite.app_service.controller;

import com.appverselite.app_service.dto.*;
import com.appverselite.app_service.service.AppService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;

import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/apps")
@RequiredArgsConstructor
public class AppController {

    private final AppService appService;

    @PostMapping
    public ResponseEntity<AppResponse> createApp(
            Authentication authentication,
            @Valid @RequestBody CreateAppRequest request) {
        String email = authentication.getName(); // Assuming the email is stored as the principal
        return ResponseEntity.ok(appService.createApp(email, request));
    }

    @PutMapping("/{id}")
    public ResponseEntity<AppResponse> updateApp(
            Authentication authentication,
            @PathVariable Long id,
            @Valid @RequestBody UpdateAppRequest request) {

        String email = authentication.getName();

        return ResponseEntity.ok(appService.updateApp(email, id, request));
    }

    @GetMapping
    public ResponseEntity<List<AppResponse>> getAllApps() {
        return ResponseEntity.ok(appService.getAllApps());
    }

    @GetMapping("/{id}")
    public ResponseEntity<AppResponse> getById(@PathVariable Long id) {
        return ResponseEntity.ok(appService.getById(id));
    }

    @PostMapping("/{id}/explain")
    public ResponseEntity<AiExplainResponse> explainApp(
            Authentication authentication,
            @PathVariable Long id) {

        String email = authentication.getName();

        return ResponseEntity.ok(appService.explainApp(email, id));
    }

}
