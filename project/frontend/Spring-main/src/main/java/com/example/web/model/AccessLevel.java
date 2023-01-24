package com.example.web.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "access_level")
@Getter
@Setter
public class AccessLevel {
    @Id
    @Column(name = "id", nullable = false)
    private Integer id;

    @Column(name = "level")
    private String level;

}
