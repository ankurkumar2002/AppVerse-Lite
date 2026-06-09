package com.appverselite.app_service.service;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import com.appverselite.app_service.dto.AiExplainResponse;
import com.appverselite.app_service.dto.ExplainRequest;

import java.util.Map;

@Service
@RequiredArgsConstructor
public class AiClientService {

    private final WebClient.Builder webClientBuilder;

    @Value("${ai.service.base-url}")
    private String aiServiceBaseUrl;

    public AiExplainResponse explainApp(ExplainRequest request) {

        return webClientBuilder.build()
                .post()
                .uri(aiServiceBaseUrl + "/ai/explain")   // ✅ FIXED
                .bodyValue(request)                      // ✅ FIXED
                .retrieve()
                .bodyToMono(AiExplainResponse.class)     // ✅ FIXED
                .block();
    }
}