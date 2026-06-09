package com.appverselite.app_service.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@FeignClient(name = "user-service", url = "http://user-service:8081")
public interface UserClient {

    @GetMapping("/users/internal/by-email")
    Long getUserIdByEmail(@RequestParam("email") String email);
}
