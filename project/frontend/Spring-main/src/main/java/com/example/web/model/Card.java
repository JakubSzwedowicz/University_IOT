package com.example.web.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

@Entity
@Table(name = "card")
@Getter
@Setter
//@SequenceGenerator(name="card_id_seq", initialValue=47, allocationSize=100)
public class Card {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
//   @GeneratedValue(strategy=GenerationType.SEQUENCE, generator="card_id_seq")
    private Integer id;

    @Column(name = "RFID_tag")
    private Integer RFIDTag;

    @ManyToOne(optional = false)
    @JoinColumn(name = "employeeid", nullable = false)
    private Employee employee;

    @ManyToOne(optional = false)
    @JoinColumn(name = "card_statusid", nullable = false)
    private CardStatus card_status;

}
