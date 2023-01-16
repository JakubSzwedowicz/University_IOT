#pragma once

#include "Arduino.h"

void log(const char* functionName, String msg);
void log(const char* functionName, int value);
void log(const char* functionName, double value);

struct RGBPercentage {
  int red;
  int green;
  int blue;
};

class PWM {
public:
  const static int s_maxPWM = 255;
  const static int s_minPWM = 0;
  static int changePWMToPercentage(int pwm);
  static int changePercentageToPWM(int percentage);
};

class LED {
public:
  LED(int ledPin, int pinMode, int pwm, bool isOn = false);
  void init();
  bool switchOnOff();
  bool switchOff();
  bool switchOn();
  bool setBrightnessPWM(int pwm);
  bool setBrightnessPercentage(int percentage);
  String getLedMsg() const;
  String getLedErrorMsg(const char* functionName, const char* message) const;
  int getPin() const;
  int getBrightnessPercentage() const;
  bool getIsOn() const;
private:
  int m_ledPin;
  int m_pinMode;
  int m_currentPWM;
  bool m_isOn;
};

class LEDRGB {
public:
  LEDRGB(int redPin, int greenPin, int bluePin);
  void init();
  bool ChangeColorPWM(int redPWM, int greenPWM, int bluePWM);
  bool ChangeColorPercentage(int red, int green, int blue);
  bool switchOnColor(char rgb);
  bool switchOffColor(char rgb);
  bool switchOnOff();
  bool switchOn();
  bool switchOff();
private:
  static int getIndexOfLED(char ledColor);
  void foo(RGBPercentage a);
  LED m_leds[3];
  RGBPercentage m_currentActiveColor;
  RGBPercentage m_previousActiveColor;
  static const int s_redIndex = 0;
  static const int s_greenIndex = 1;
  static const int s_blueIndex = 2;
  static const int s_ledMode = OUTPUT;
};
