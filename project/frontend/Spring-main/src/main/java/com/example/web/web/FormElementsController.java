package com.example.web.web;

import com.example.web.model.AccessLevel;
import com.example.web.model.Card;
import com.example.web.model.CardStatus;
import com.example.web.model.Employee;
import com.example.web.model.dto.CardDto;
import com.example.web.model.dto.EmployeeDto;
import com.example.web.repository.AccessLevelRepository;
import com.example.web.repository.CardRepository;
import com.example.web.repository.CardStatusRepository;
import com.example.web.repository.EmployeeRepository;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping(value = "pages")
public class FormElementsController {
    private EmployeeRepository employeeRepository;
    private CardStatusRepository cardStatusRepository;

    private CardRepository cardRepository;

    private AccessLevelRepository accessLevelRepository;

    public FormElementsController(EmployeeRepository employeeRepository, CardStatusRepository cardStatusRepository, CardRepository cardRepository, AccessLevelRepository accessLevelRepository) {
        this.employeeRepository = employeeRepository;
        this.cardStatusRepository = cardStatusRepository;
        this.cardRepository = cardRepository;
        this.accessLevelRepository = accessLevelRepository;
    }

    @GetMapping(value = "form-elements")
    public ModelMap mmFormElements() {
        ModelMap mm = new ModelMap();
        mm.addAttribute("employees", employeeRepository.findAll());
        mm.addAttribute("cardStatuses", cardStatusRepository.findAll() );
        mm.addAttribute("levels", accessLevelRepository.findAll());
        mm.addAttribute("formCard", new CardDto());
        mm.addAttribute("formEmployee", new EmployeeDto());
        return mm;
    }

    @GetMapping(value = "form-elements1")
    public ModelMap mmFormElements1() {
        return new ModelMap();
    }

    @PostMapping("/addNewCard")
    public String registration(@ModelAttribute("formCard") CardDto cardDto, BindingResult bindingResult) {

        Employee employee = employeeRepository.findByLastName(cardDto.getEmployeeLastName());
        CardStatus cardStatus = cardStatusRepository.findByStatus(cardDto.getCardStatus());
        Card card = new Card();
        card.setCard_status(cardStatus);
        card.setRFIDTag(cardDto.getRFIDTag());
        card.setEmployee(employee);
        cardRepository.save(card);
        return "redirect:/pages/form-elements";
    }

    @PostMapping("/addNewEmployee")
    public String registration(@ModelAttribute("formEmployee")EmployeeDto employeeDto, BindingResult bindingResult) {

        AccessLevel accessLevel = accessLevelRepository.findAllByLevel(employeeDto.getLevel());
        Employee employee = new Employee();
        employee.setFirstName(employeeDto.getFirstName());
        employee.setLastName(employeeDto.getLastName());
        employee.setAccessLevel(accessLevel);
        employeeRepository.save(employee);
        return "redirect:/pages/form-elements";
    }

}
