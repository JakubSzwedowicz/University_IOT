#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <util/atomic.h>


void log(const char* functionName, int value);
void log(const char* functionName, double value);
void initLCD();
void initRGB();
void setupButtons();
void setup();

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

void initRGB() {
  s_ledRGB.init();
}

void log(const char* functionName, String msg) {
  Serial.print(functionName);
  Serial.print(", message = ");
  Serial.println(msg);
}

void log(const char* functionName, int value) {
  Serial.print(functionName);
  Serial.print(", ivalue = ");
  Serial.println(value);
}

void log(const char* functionName, double value) {
  Serial.print(functionName);
  Serial.print(", dvalue = ");
  Serial.println(value);
}

void setup() {
  initRGB();
  s_ledRGB.switchOn();
}

int PWM::changePWMToPercentage(int pwm) {
  return (pwm * 100. / s_maxPWM);
}

int PWM::changePercentageToPWM(int percentage) {
  return (percentage / 100.) * s_maxPWM;
}

LED::LED(int ledPin, int pinMode, int pwm, bool isOn)
  : m_ledPin(ledPin), m_pinMode(pinMode), m_isOn(isOn), m_currentPWM(pwm) {
}
void LED::init() { 
  pinMode(m_ledPin, m_pinMode);
  if (m_isOn) {
    switchOn();
  } else {
    switchOff();
  }
}

bool LED::switchOnOff() {
  if (m_isOn) {
    return switchOff();
  } else {
    return switchOn();
  }
}
bool LED::switchOff() {
  m_isOn = false;
  analogWrite(m_ledPin, PWM::s_minPWM);
  log(__func__, m_isOn);
  return true;
}

bool LED::switchOn() {
  m_isOn = true;
  analogWrite(m_ledPin, m_currentPWM);
  log(__func__, m_isOn);
  log("current led pwm=", m_currentPWM);
  return true;
}

bool LED::setBrightnessPWM(int pwm) {
  if (pwm < PWM::s_minPWM || pwm > PWM::s_maxPWM) {
    // Serial.print(getLedErrorMsg(__func__, "brightness out of range"));
    return false;
  }

  if (m_currentPWM != pwm) {
    m_currentPWM = pwm;
    if (m_isOn) {
      analogWrite(m_ledPin, pwm);
    }
  }
  log(__func__, pwm);
  return true;
}
bool LED::setBrightnessPercentage(int percentage) {
  int pwm = PWM::changePercentageToPWM(percentage);
  log(__func__, percentage);
  return setBrightnessPWM(pwm);
}

String LED::getLedMsg() const {
  String msg = String("LED pin[") + m_ledPin + "]";
  return msg;
}
String LED::getLedErrorMsg(const char* functionName, const char* message) const {
  // const char* msg = strcat(strcat(strcat(strcat(getLedMsg().c_str(), "::"), functionName), "() - "), message);
  String msg = getLedMsg() + "::" + functionName + "() - " + message;
  return msg;
}

int LED::getPin() const {
  return m_ledPin;
}

int LED::getBrightnessPercentage() const {
  return PWM::changePWMToPercentage(m_currentPWM);
}

bool LED::getIsOn() const {
  return m_isOn;
}

LEDRGB::LEDRGB(int redPin, int greenPin, int bluePin)
  : m_currentActiveColor({ 100, 0, 0 }), m_previousActiveColor({ 0, 0, 0 }),
    m_leds({ { redPin, s_ledMode, 255, m_currentActiveColor.red != 0 }, { greenPin, s_ledMode, PWM::changePercentageToPWM(m_currentActiveColor.green), m_currentActiveColor.green != 0 }, { bluePin, s_ledMode, PWM::changePercentageToPWM(m_currentActiveColor.blue), m_currentActiveColor.blue != 0 } }) {
}

void LEDRGB::init() {
  for (auto& led : m_leds) {
    led.init();
  }
}

bool LEDRGB::ChangeColorPWM(int redPWM, int greenPWM, int bluePWM) {
  int redPerc = PWM::changePWMToPercentage(redPWM);
  int greenPerc = PWM::changePWMToPercentage(greenPWM);
  int bluePerc = PWM::changePWMToPercentage(bluePWM);
  return ChangeColorPercentage(redPerc, greenPerc, bluePerc);
}
bool LEDRGB::ChangeColorPercentage(int red, int green, int blue) {
  if (m_currentActiveColor.red != red) m_leds[s_redIndex].setBrightnessPercentage(red);
  if (m_currentActiveColor.green != green) m_leds[s_greenIndex].setBrightnessPercentage(green);
  if (m_currentActiveColor.blue != blue) m_leds[s_blueIndex].setBrightnessPercentage(blue);

  RGBPercentage temp = m_currentActiveColor;
  m_currentActiveColor = { red, green, blue };
  m_previousActiveColor = temp;
  return true;
}

bool LEDRGB::switchOnColor(char rgb) {
  int index = getIndexOfLED(rgb);
  m_leds[index].switchOn();
}

bool LEDRGB::switchOffColor(char rgb) {
  int index = getIndexOfLED(rgb);
  m_leds[index].switchOff();
}

bool LEDRGB::switchOnOff() {
  for (auto& led : m_leds) {
    if (!led.getIsOn()) {
      led.switchOn();
    } else {
      led.switchOff();
    }
  }
}

bool LEDRGB::switchOn() {
  for (auto& led : m_leds) {
    led.switchOn();
  }
}

bool LEDRGB::switchOff() {
  for (auto& led : m_leds) {
    led.switchOff();
  }
}

int LEDRGB::getIndexOfLED(char ledColor) {
  switch (ledColor) {
    case 'r':
      return s_redIndex;
    case 'g':
      return s_greenIndex;
    case 'b':
      return s_blueIndex;
  }
}

