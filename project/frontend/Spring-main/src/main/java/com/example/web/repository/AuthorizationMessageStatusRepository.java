package com.example.web.repository;

import com.example.web.model.AuthorizationMessageStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AuthorizationMessageStatusRepository extends JpaRepository<AuthorizationMessageStatus, Integer> {
    AuthorizationMessageStatus findByStatus(String status);
}
