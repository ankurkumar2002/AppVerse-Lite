package com.appverselite.app_service.service;

import com.appverselite.app_service.entity.EventType;
import com.appverselite.app_service.entity.InteractionLog;
import com.appverselite.app_service.repository.InteractionLogRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class InteractionLogService {

    private final InteractionLogRepository interactionLogRepository;

    public void log(Long userId, EventType eventType, String payload) {
        InteractionLog log = InteractionLog.builder()
                .userId(userId)
                .eventType(eventType)
                .eventPayload(payload)
                .build();

        interactionLogRepository.save(log);
    }
}