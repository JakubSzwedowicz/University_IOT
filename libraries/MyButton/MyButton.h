#pragma once
#include "Arduino.h"

class Button {
  public:
    Button(int buttonPin);
    void setup() const;
    bool onHold();
    bool onRelease();
    bool onHoldFor(unsigned long requiredHoldTimeInMilis);
    bool onHoldOnceFor(unsigned long requiredHoldTimeInMilis);
    int getButtonPin() const;
    bool isPressed() const;
  private:
    const static int s_debouncePeriod = 10;
    const int m_buttonPin;
    bool m_isPressed = false;
    bool m_previousIsHeld = false;
    bool m_onHoldOnceFor_activated = false;
    int m_previousReading = HIGH;
    unsigned long m_lastChangeTime = 0;
    unsigned int m_alreadyHoldTime = 0;
    unsigned long m_startTime = 0;
};
