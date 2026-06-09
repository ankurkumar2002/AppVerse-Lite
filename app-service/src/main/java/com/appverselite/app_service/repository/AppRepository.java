package com.appverselite.app_service.repository;

import com.appverselite.app_service.entity.AppEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AppRepository extends JpaRepository<AppEntity,Long>{}