package com.example.web.repository;

import com.example.web.model.Card;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CardRepository extends JpaRepository<Card, Integer> {
//    @Modifying
//    @Query(value = "INSERT INTO card (RFID_tag, employeeid, card_statusid) values (?1, ?2, ?3)",
//            nativeQuery = true)
//    void saveCard(String RFID_tag, int employeeid, int card_statusid);
}
