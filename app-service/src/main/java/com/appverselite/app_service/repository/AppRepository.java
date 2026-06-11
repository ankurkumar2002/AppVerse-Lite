package com.appverselite.app_service.repository;


import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.appverselite.app_service.entity.AppEntity;

public interface AppRepository extends JpaRepository<AppEntity, Long> {

    List<AppEntity> findByCategoryIgnoreCase(String category); 
}
