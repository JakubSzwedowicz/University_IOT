#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3
#define RED_BUTTON_PIN 2
#define GREEN_BUTTON_PIN 4
#define POTENTIOMETER A0
#define ENCODER1 A2
#define ENCODER2 A3

void log(const char* functionName, int value);
void initLCD();
void initRGB();
void initButtons();
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

class Encoder {
  public:
    Encoder(int pin1, int pin2);
    void init() const;
    bool isChanged() const;
    bool isRight();
    bool isLeft(); 
  private:
    bool m_turnedLeft;
    bool m_turnedRight;
    int m_counter;
    int m_clkPin1;
    int m_clkPin2;
};

class Button {
  public:
    Button(int buttonPin);
    void init() const;
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
    LED m_leds[3];
    RGBPercentage m_currentActiveColor;
    RGBPercentage m_previousActiveColor;
    static const int s_redIndex = 0;
    static const int s_greenIndex = 1;
    static const int s_blueIndex = 2;
    static const int s_ledMode = OUTPUT;
};

class SerialHandler {
  public:
    void checkInput();
  private:
    bool isSetPercentageOfLEDRGB(const String& command) const;
    void setPercentageOfLEDRGB(String);
};

class MyADC {
  public:
    MyADC(int adcPin);
    int getRead() const;
    float getReadVoltage() const;
  private:
    const int m_adcPin;
    static const int s_maxRead = 1023;
    static const int s_minRead = 0;
    static const int s_trimmed = 10;

};

// ATTRIBUTES
static LiquidCrystal_I2C s_lcd(0x27, 16, 2);

constexpr int c_BUTTONS_SIZE = 2;
constexpr int c_RED_BUTTON_INDEX = 0;
constexpr int c_GREEN_BUTTON_INDEX = 1;
static Button s_buttons[c_BUTTONS_SIZE] = { { RED_BUTTON_PIN }, { GREEN_BUTTON_PIN } };

static LEDRGB s_ledRGB(LED_RED, LED_GREEN, LED_BLUE);

static SerialHandler s_serialHandler;

static MyADC s_MyADC(POTENTIOMETER);

static bool isGreenPressed;
static bool isRedPressed;
void task_1() {

  s_lcd.print("Zadanie 1");

  bool isGreenPressed = s_buttons[c_GREEN_BUTTON_INDEX].isPressed();
  bool isRedPressed = s_buttons[c_RED_BUTTON_INDEX].isPressed();

  Serial.println(String("Green button isPressed = ") + isGreenPressed + ", red is pressed = " + isRedPressed);

  s_lcd.setCursor(0, 0);
}

void task_2() {
  static RGBPercentage task1_currentColour = { 0, 0, PWM::s_maxPWM };


  s_lcd.print("Zadanie 2");

  s_serialHandler.checkInput();

  s_lcd.setCursor(0, 0);
}


// int brightness = 0;
// void task_2() {
//   uint8_t step = 10;

//   delay(100);
//   if (digitalRead(GREEN_BUTTON) == LOW) {
//     brightness = (brightness + step) >= 255 ? 255 : (brightness + step);
//   }
//   if (digitalRead(RED_BUTTON) == LOW) {
//     brightness = (brightness - step) <= 0 ? 0 : (brightness - step);
//   }
//   Serial.println(brightness);
//   analogWrite(LED_GREEN, brightness);
// }

// int prev = LED_RED;
// int prev_color = 0;
// int curr = LED_GREEN;
// int curr_color = 255;

static int adc = 0;
void task_3() {
  adc = s_MyADC.getRead();
  float volt = s_MyADC.getReadVoltage();

  s_lcd.print(String("ADC = ") + adc + "  ");
  s_lcd.setCursor(0, 1);
  s_lcd.print(String("Voltage = ") + volt + "   ");
  Serial.print(adc);

  s_lcd.setCursor(0, 0);
}

void loop() {
  // task_1();
  // task_2();
  task_3();
}


void initLCD() {
  s_lcd.init();
  s_lcd.clear();
  s_lcd.backlight();
}

void initRGB() {
  s_ledRGB.init();
}

void initButtons() {
  for (const auto& button : s_buttons) {
    button.init();
  }
}

void log(const char* functionName, String msg) {
  Serial.print(functionName);
  Serial.print(", message = ");
  Serial.println(msg);
}

void log(const char* functionName, int value) {
  Serial.print(functionName);
  Serial.print(", value = ");
  Serial.println(value);
}

void setup() {
  Serial.begin(9600);
  initRGB();
  initButtons();
  initLCD();
  s_ledRGB.switchOn();
}

int PWM::changePWMToPercentage(int pwm) {
  return (pwm / s_maxPWM) * 100;
}

int PWM::changePercentageToPWM(int percentage) {
  return (percentage / 100) * s_maxPWM;
}

Encoder::Encoder(int pin1, int pin2) : m_turnedLeft(false), m_turnedRight(false), m_counter(0), m_clkPin1(pin1), m_clkPin2(pin2)
{

}

void Encoder::init() const
{
  pinMode(ENCODER1, INPUT_PULLUP);
  pinMode(ENCODER2, INPUT_PULLUP);

}

    bool Encoder::isChanged() const
    {
      return m_turnedLeft || m_turnedRight;
    }
    bool Encoder::isRight()
    {
      bool ret = m_turnedRight;
      m_turnedRight = false;
      return ret;

    }
    bool Encoder::isLeft()
    {
      bool ret = m_turnedRight;
      m_turnedLeft = false;
      return ret;
    } 
    

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
  : m_currentActiveColor( {
  0, 0, 0
}), m_previousActiveColor({ 0, 0, 0 }),
m_leds({ { redPin, s_ledMode, m_currentActiveColor.red }, { greenPin, s_ledMode, m_currentActiveColor.green }, { bluePin, s_ledMode, m_currentActiveColor.blue } }) {}

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

void SerialHandler::checkInput() {
  if (!Serial.available()) return;

  String command = Serial.readStringUntil('\n');
  command.trim();
  command.toLowerCase();

  log(__func__, command);
  if (isSetPercentageOfLEDRGB(command)) {
    setPercentageOfLEDRGB(command);
  }
}

bool SerialHandler::isSetPercentageOfLEDRGB(const String& command) const {
  return command.startsWith("setrgb");
}
void SerialHandler::setPercentageOfLEDRGB(String command) {
  int beforeRedCol = command.indexOf(';');
  int beforeGreenCol = command.indexOf(';', beforeRedCol + 1);
  int beforeBlueCol = command.indexOf(';', beforeGreenCol + 1);
  log(__func__, String("redCol=") + beforeRedCol + ", greenCol=" + beforeGreenCol + ", blueCol=" + beforeBlueCol);

  int redPercentage = command.substring(beforeRedCol + 1, beforeGreenCol).toInt();
  int greenPercentage = command.substring(beforeGreenCol + 1, beforeBlueCol).toInt();
  int bluePercentage = command.substring(beforeBlueCol + 1).toInt();

  log(__func__, String("red=") + redPercentage + ", green=" + greenPercentage + ", blue=" + bluePercentage);
  s_ledRGB.ChangeColorPercentage(redPercentage, greenPercentage, bluePercentage);
}

MyADC::MyADC(int adcPin)
  : m_adcPin(adcPin) {}

int MyADC::getRead() const {
  int value = analogRead(m_adcPin);
  return value;
}
float MyADC::getReadVoltage() const {
  float value = getRead();
  int lowRange = s_minRead + s_trimmed;
  int highRange = s_maxRead - s_trimmed;
  value = max(lowRange, min(highRange, value));
  float voltage = (value / (s_maxRead - 2 * s_trimmed) ) * 5.0;
  return voltage;
}
