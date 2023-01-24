package com.example.web.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.sql.Timestamp;

@Entity
@Table(name = "authorization_message")
@Getter
@Setter
public class AuthorizationMessage {
    @Id
    @Column(name = "id", nullable = false)
    private Integer id;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    private Timestamp date;

    @ManyToOne(optional = false)
    @JoinColumn(name = "cardid", nullable = false)
    private Card card;

    @ManyToOne(optional = false)
    @JoinColumn(name = "deviceid", nullable = false)
    private Device device;

    @ManyToOne(optional = false)
    @JoinColumn(name = "authorization_message_statusid", nullable = false)
    private AuthorizationMessageStatus authorizationMessageStatus;
}
