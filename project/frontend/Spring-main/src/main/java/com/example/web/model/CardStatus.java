package com.example.web.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "card_status")
@Getter
@Setter
public class CardStatus {
    @Id
    @Column(name = "id", nullable = false)
    private Integer id;

    private String status;

}
