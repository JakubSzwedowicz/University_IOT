package com.example.web.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

@Entity
@Table(name = "employee")
@Getter
@Setter
//@SequenceGenerator(name="employee_id_seq", initialValue=20, allocationSize=100)
public class Employee {
    @Id
    @Column(name = "id", nullable = false)
   // @GeneratedValue(strategy=GenerationType.SEQUENCE, generator="employee_id_seq")
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "first_name")
    private String firstName;
    @Column(name = "Last_name")
    private String lastName;

    @ManyToOne(optional = false)
    @JoinColumn(name = "access_levelid", nullable = false)
    private AccessLevel accessLevel;
}
