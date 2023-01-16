#include "MyButton.h"

Button::Button(int buttonPin)
  : m_buttonPin(buttonPin) {
}

void Button::init() const {
  pinMode(m_buttonPin, INPUT_PULLUP);
}

bool Button::onHold() {
  m_isPressed = false;
  int currentReading = digitalRead(m_buttonPin);

  if (m_previousReading != currentReading) {
    m_lastChangeTime = millis();
  }
  if (millis() - m_lastChangeTime > s_debouncePeriod) {  // debouncing
    if (currentReading == LOW) {
      m_isPressed = true;
      log(__func__, m_isPressed);
    }
  }
  m_previousReading = currentReading;
  return m_isPressed;
}

bool Button::onRelease() {
  bool wasReleased = false;
  bool currentIsHeld = onHold();
  if (currentIsHeld == false && m_previousIsHeld == true) {
    wasReleased = true;
    log(__func__, wasReleased);
  }
  m_previousIsHeld = currentIsHeld;
  return wasReleased;
}

bool Button::onHoldFor(unsigned long requiredHoldTimeInMilis) {
  bool onHoldFor = false;
  if (onHold()) {
    if (m_startTime == 0) {
      m_startTime = millis();
    } else {
      m_alreadyHoldTime = millis() - m_startTime;
    }

    if (m_alreadyHoldTime >= requiredHoldTimeInMilis) {
      onHoldFor = true;
    }
  } else {
    m_startTime = 0;
    m_alreadyHoldTime = 0;
  }
  // log(__func__, m_alreadyHoldTime - requiredHoldTimeInMilis);
  return onHoldFor;
}

bool Button::onHoldOnceFor(unsigned long requiredHoldTimeInMilis) {
  bool onHoldForOnce = false;
  if (onHoldFor(requiredHoldTimeInMilis)) {
    if (!m_onHoldOnceFor_activated) {
      onHoldForOnce = true;
      m_onHoldOnceFor_activated = true;
      log(__func__, onHoldForOnce);
    }
  } else {
    m_onHoldOnceFor_activated = false;
  }
  return onHoldForOnce;
}

int Button::getButtonPin() const {
  return m_buttonPin;
}

bool Button::isPressed() const {
  return digitalRead(m_buttonPin) == LOW;
}