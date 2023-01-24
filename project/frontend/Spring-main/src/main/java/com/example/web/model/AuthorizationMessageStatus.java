package com.example.web.model;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "authorization_message_status")
@Getter
@Setter
public class AuthorizationMessageStatus {
    @Getter(AccessLevel.NONE)
    @Setter(AccessLevel.NONE)
    @Id
    @Column(name = "id", nullable = false)
    private Integer id;

    private String status;
}
