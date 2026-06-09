package com.appverselite.app_service.repository;

import com.appverselite.app_service.entity.InteractionLog;
import org.springframework.data.jpa.repository.JpaRepository;

public interface InteractionLogRepository extends JpaRepository<InteractionLog, Long> {
}