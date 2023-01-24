package com.example.web.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

@Entity
@Table(name = "door")
@Getter
@Setter
public class Door {
    @Id
    @Column(name = "id", nullable = false)
    private Integer id;

    private String description;

    @ManyToOne(optional = false)
    @JoinColumn(name = "deviceid", nullable = true)
    private Device device;

    @ManyToOne(optional = false)
    @JoinColumn(name = "access_levelid", nullable = false)
    private com.example.web.model.AccessLevel accessLevel;
}
