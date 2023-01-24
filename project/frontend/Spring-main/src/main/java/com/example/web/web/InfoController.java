package com.example.web.web;

import com.example.web.repository.CardRepository;
import com.example.web.repository.EmployeeRepository;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping(value = "pages")
public class InfoController {
    private String infoPage= "layout";
    private String dashboardPage= "pages/dashboard";

    private CardRepository cardRepository;

    private EmployeeRepository employeeRepository;

    public InfoController(CardRepository cardRepository, EmployeeRepository employeeRepository) {
        this.cardRepository = cardRepository;
        this.employeeRepository = employeeRepository;
    }

    @GetMapping(value = "cards")
    public ModelMap mmFormElements() {
        ModelMap model = new ModelMap();
        model.addAttribute("cards", cardRepository.findAll());

        return model;
    }

    @GetMapping(value = "employee")
    public ModelMap mmEmployee() {
        ModelMap model = new ModelMap();
        model.addAttribute("employees", employeeRepository.findAll());

        return model;
    }

}
