package com.example.web.web;

import com.example.web.repository.*;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.sql.Timestamp;
import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.Map;

@Controller
@RequestMapping(value = "pages")
public class DashboardController {

    private EmployeeRepository employeeRepository;
    private AuthorizationMessageRepository authorizationMessageRepository;

    private CardRepository cardRepository;

    private AuthorizationMessageStatusRepository authorizationMessageStatusRepository;

    private DeviceRepository deviceRepository;

    public DashboardController(EmployeeRepository employeeRepository, AuthorizationMessageRepository authorizationMessageRepository, CardRepository cardRepository, AuthorizationMessageStatusRepository authorizationMessageStatusRepository, DeviceRepository deviceRepository) {
        this.employeeRepository = employeeRepository;
        this.authorizationMessageRepository = authorizationMessageRepository;
        this.cardRepository = cardRepository;
        this.authorizationMessageStatusRepository = authorizationMessageStatusRepository;
        this.deviceRepository = deviceRepository;
    }

    @GetMapping(value = "dashboard")
    public ModelMap mmDashboard() {
        Timestamp ts = Timestamp.from(Instant.now().minusSeconds(864000000));
        ModelMap mm = new ModelMap();
        mm.addAttribute("totalEmployees", employeeRepository.count());
        mm.addAttribute("devices", deviceRepository.count());
        mm.addAttribute("card", cardRepository.count());
        mm.addAttribute("visits", authorizationMessageRepository.findAllByAuthorizationMessageStatusAndDateAfter(authorizationMessageStatusRepository.findByStatus("accepted"),ts ).size());
        mm.addAttribute("authMesses", authorizationMessageRepository.findAllOrderByDate());
        mm.addAttribute("message", "Heloooo");

        Map<String, Integer> data = new LinkedHashMap<String, Integer>();
        //["2013", "2014", "2014", "2015", "2016", "2017"],
        data.put("2013", 50);
        data.put("2014", 20);
        data.put("2014", 30);
        data.put("2015", 20);
        data.put("2016", 30);
        data.put("2017", 30);

        mm.addAttribute("data", data);
        return mm;
    }

}
