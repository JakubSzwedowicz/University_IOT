package com.example.web.repository;

import com.example.web.model.AccessLevel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AccessLevelRepository extends JpaRepository<AccessLevel, Integer> {

    AccessLevel findAllByLevel(String level);
}
