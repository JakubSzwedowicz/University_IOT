package com.example.web.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "device")
@Getter
@Setter
public class Device {

    @Id
    @Column(name = "id", nullable = false)
    private Integer id;

    @Column(name = "mac_address")
    private String macAddress;
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }
}
