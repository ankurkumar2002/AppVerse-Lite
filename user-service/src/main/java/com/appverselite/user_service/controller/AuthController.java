package com.appverselite.user_service.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import com.appverselite.user_service.dto.AuthResponse;
import com.appverselite.user_service.dto.LoginRequest;
import com.appverselite.user_service.dto.RegisterRequest;
import com.appverselite.user_service.dto.UserProfileResponse;
import com.appverselite.user_service.service.AuthService;

@RestController
@RequestMapping("/users")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("/auth/register")
    public ResponseEntity<AuthResponse> register(@Valid @RequestBody RegisterRequest request) {
        return ResponseEntity.ok(authService.register(request));
    }

    @PostMapping("/auth/login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }

    @GetMapping("/me")
    public ResponseEntity<UserProfileResponse> me(Authentication authentication) {
        return ResponseEntity.ok(authService.currentUser(authentication.getName()));
    }

    @GetMapping("/internal/by-email")
    public Long getUserIdByEmail(@RequestParam String email) {
        return authService.getUserIdByEmail(email);
    }

}