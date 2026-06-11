package com.appverselite.app_service.service;

import com.appverselite.app_service.client.UserClient;
import com.appverselite.app_service.dto.*;
import com.appverselite.app_service.entity.AppEntity;
import com.appverselite.app_service.entity.EventType;
import com.appverselite.app_service.repository.AppRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class AppService {

        private final AppRepository appRepository;
        private final AiClientService aiClientService;
        private final InteractionLogService interactionLogService;
        private final UserClient userRepository;

        public AppResponse createApp(String email, CreateAppRequest request) {

                Long userId = getUserIdFromEmail(email);

                AppEntity app = new AppEntity();
                app.setName(request.getName());
                app.setDescription(request.getDescription());
                app.setCategory(request.getCategory());
                app.setCreatedBy(userId);

                AppEntity saved = appRepository.save(app);

                interactionLogService.log(
                                userId,
                                EventType.APP_CREATED,
                                "App created with id=" + saved.getId() + ", name=" + saved.getName());

                // ✅ use builder (because your DTO has no setters)
                return AppResponse.builder()
                                .id(saved.getId())
                                .name(saved.getName())
                                .description(saved.getDescription())
                                .category(saved.getCategory())
                                .createdBy(saved.getCreatedBy())
                                .createdAt(saved.getCreatedAt())
                                .updatedAt(saved.getUpdatedAt())
                                .build();
        }

        private Long getUserIdFromEmail(String email) {
                Long userId = userRepository.getUserIdByEmail(email);

                if (userId == null) {
                        throw new RuntimeException("User not found");
                }

                return userId;
        }

        public AppResponse updateApp(String email, Long appId, UpdateAppRequest request) {
                Long userId = getUserIdFromEmail(email);

                AppEntity app = appRepository.findById(appId)
                                .orElseThrow(() -> new RuntimeException("App not found"));

                if (!app.getCreatedBy().equals(userId)) {
                        throw new RuntimeException("You can update only your own app");
                }

                app.setName(request.getName());
                app.setDescription(request.getDescription());
                app.setCategory(request.getCategory());

                AppEntity updated = appRepository.save(app);
                return mapToResponse(updated);
        }

        public List<AppResponse> getAllApps() {
                return appRepository.findAll()
                                .stream()
                                .map(this::mapToResponse)
                                .toList();
        }

        public AppResponse getById(Long appId) {
                AppEntity app = appRepository.findById(appId)
                                .orElseThrow(() -> new RuntimeException("App not found"));

                return mapToResponse(app);
        }

        public AiExplainResponse explainApp(String email, Long appId) {
                Long userId = getUserIdFromEmail(email);

                AppEntity app = appRepository.findById(appId)
                                .orElseThrow(() -> new RuntimeException("App not found"));

                ExplainRequest request = new ExplainRequest(
                                app.getName(),
                                app.getDescription(),
                                app.getCategory());

                AiExplainResponse aiResponse = aiClientService.explainApp(request);

                interactionLogService.log(userId, EventType.EXPLAIN_APP,
                                "Explained app id=" + appId);

                return aiResponse;
        }

        private AppResponse mapToResponse(AppEntity app) {
                return AppResponse.builder()
                                .id(app.getId())
                                .name(app.getName())
                                .description(app.getDescription())
                                .category(app.getCategory())
                                .createdBy(app.getCreatedBy())
                                .createdAt(app.getCreatedAt())
                                .updatedAt(app.getUpdatedAt())
                                .build();
        }

        public List<AppResponse> getAppsByCategory(String category) {
            return appRepository.findByCategoryIgnoreCase(category)
                    .stream()
                    .map(this::mapToResponse)
                    .toList();
        }
}
