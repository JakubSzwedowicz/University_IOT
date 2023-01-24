package com.example.web.model.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class CardDto {
    private Integer RFIDTag;


    private String employeeLastName;

    private String cardStatus;

    public CardDto(Integer RFIDTag, String employeeLastName, String cardStatus) {
        this.RFIDTag = RFIDTag;
        this.employeeLastName = employeeLastName;
        this.cardStatus = cardStatus;
    }

    public CardDto() {
    }
}
