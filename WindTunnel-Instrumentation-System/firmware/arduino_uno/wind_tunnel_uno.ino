
#define P Serial.print
#define P2(x,y) P(x);P(y)
#define P3(x,y,z) P(x);P(y);P(z)
#define P4(w,x,y,z) P(w);P(x);P(y);P(z)
#define PL Serial.println
#define FLAG() P("Flag Triggered at line ");PL(__LINE__)

/*============================================================
MAV LABS WIND TUNNEL DASHBOARD
FINAL COMPLETE VERSION
Arduino UNO + SSD1306 OLED

Displays:
- Scrolling header
- Lift (grams)
- Speed (m/s)
- Temperature
- Humidity
- Pressure
- Trend arrows (up / down)

Author: Final Integrated Version
============================================================
*/
/*
  ============================================================
  MAV LABS IISc Bangalore — Single-screen OLED Layout
  ============================================================
  Layout (128×64 SSD1306):

  ┌────────────────────────────┐
  │  MAV LABS IISc Bangalore   │  ← header (row 0–9)
  ├──────────────┬─────────────┤  ← divider (y=10)
  │  Lift        │  Speed      │
  │  1209 g      │  10 m/s     │  ← main data (y=12–50)
  ├──────────────┴─────────────┤  ← divider (y=51)
  │  T 28°C      1013 hPa      │  ← bottom bar (y=53–63)
  └────────────────────────────┘

  Libraries needed:
    Adafruit BMP085 Library
    Adafruit SSD1306
    Adafruit GFX Library
    DHT sensor library  (Adafruit)
    HX711 Arduino Library  (Bogdan Necula)
  ============================================================
*/

#include <Wire.h>
#include <Adafruit_BMP085.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>
#include <HX711.h>

// ── OLED ──────────────────────────────────────────────────
#define SCREEN_W  128
#define SCREEN_H   64
Adafruit_SSD1306 display(SCREEN_W, SCREEN_H, &Wire, -1);

// ── BMP180 ────────────────────────────────────────────────
Adafruit_BMP085 bmp;

// ── DHT11 ─────────────────────────────────────────────────
#define DHT_PIN  4
DHT dht(DHT_PIN, DHT11);
// ── HX711 ─────────────────────────────────────────────────
#define DOUT_PIN  2
#define SCK_PIN   3
#define DOUT_PIN2  4
#define SCK_PIN2   5
HX711 scale,scale2;
float CALIB_FACTOR = 2280.0;  // ← paste your calibration value

// // ── MS4525DO ──────────────────────────────────────────────
// #define MS4525_ADDR  0x28
// ── Pitot tube ──────────────────────────────────────────────

#define PITOT_I2C_ADDRESS 0x36  // I2C device address
#define NUM_BYTES 4       // Number of bytes to read from the device
#define AVG_SAMPLE_COUNT 10


// ── Sensor readings ───────────────────────────────────────
float bmp_temp     = 0;
float bmp_pressure = 0;
float dht_temp     = 0;
float dht_hum      = 0;
float diff_press   = 0;
float airspeed     = 0;
float weight_g     = 0;
float drag     = 0;

bool bmp_ok = false;
bool pitot_ok = false;

// ─────────────────────────────────────────────────────────
//  PITOT TUBE read
// ─────────────────────────────────────────────────────────
double getVelocity(uint16_t pressure) {
  double a = 2.4782, b = -16.5289;//calibration parameters
  if (pressure >= 8192) {
    return (sqrt((double)(pressure - 8192)) * -a) +b;
  }
  return sqrt((double)(8192 - pressure)) * a + b;
}

double velocityReadings[AVG_SAMPLE_COUNT] = { 0 };
double velocitySum = 0;
int velocityReadingsIndex = -1;
void insertVelocityReading(double reading) {
  if (velocityReadingsIndex == -1) {
    for (int i = 0; i < AVG_SAMPLE_COUNT; i++) {
      velocityReadings[i] = 0;
    }
    velocityReadingsIndex = 0;
  }
  velocitySum += reading - velocityReadings[velocityReadingsIndex];
  velocityReadings[velocityReadingsIndex] = reading;
  velocityReadingsIndex = (velocityReadingsIndex + 1) % AVG_SAMPLE_COUNT;
}
double getAvgVelocity() {
  return velocitySum / AVG_SAMPLE_COUNT;
}
bool readPitot(){
  // FLAG();
  uint8_t data[NUM_BYTES];

    int i = 0;
    Wire.requestFrom(PITOT_I2C_ADDRESS, NUM_BYTES);
    while (Wire.available() && i < NUM_BYTES) {
      data[i] = Wire.read();
      i++;
    }

    if (i == NUM_BYTES) {
      uint16_t status_ = (data[0] >> 6) & 0x03;
      uint16_t pres_cnts_ = static_cast<uint16_t>(data[0] & 0x3F) << 8 | data[1];
      uint16_t temp_cnts_ = static_cast<uint16_t>(data[2]) << 3 | data[3] & 0xE0 >> 5;
      double reading = getVelocity(pres_cnts_);
      insertVelocityReading(reading);
      airspeed=getAvgVelocity();
      return true;
    }
  return false;
}

// ─────────────────────────────────────────────────────────
//  Draw the MAV LABS layout
// ─────────────────────────────────────────────────────────
void drawMAVScreen() {
  display.clearDisplay();

  // ── HEADER ──────────────────────────────────────────────
  // Centered "MAV LAB IISc Bangalore" in size-1 text (6px/char)
  const char* title = "MAV LAB IISc Blr";   // 17 chars = 102px — fits in 128
  int16_t tx = (SCREEN_W - (int16_t)strlen(title) * 6) / 2;
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(tx, 1);
  display.print(title);

  // Divider under header
  display.drawFastHLine(0, 10, SCREEN_W, SSD1306_WHITE);

  // ── MAIN SECTION labels ─────────────────────────────────
  display.setTextSize(1);
  display.setCursor(2, 13);   display.print(F("Lift/Drag"));
  display.setCursor(66, 13);  display.print(F("Speed"));

  // Vertical separator between Lift and Speed columns
  display.drawFastVLine(SCREEN_W / 2, 11, 39, SSD1306_WHITE);

  // ── LIFT value (weight) ─────────────────────────────────
  char wBuf[10];
  weight_g/=-5.738;
  drag/=5.862;
  P4("l:",weight_g,",d:",drag);
  if(weight_g>100){
    dtostrf(weight_g, 5, 1, wBuf);   // e.g. " 1209"
  }
  else if(weight_g>10){
    dtostrf(weight_g, 5, 2, wBuf);   // e.g. " 1209"
  }
  else if(weight_g>0){
    dtostrf(weight_g, 5, 3, wBuf);   // e.g. " 1209"
  }
  else{
    dtostrf(weight_g, 5, 1, wBuf);   // e.g. " 1209"
  }

  display.setTextSize(1);           // 12×16 px per char
  display.setCursor(5, 24);
  display.print("L:");
  display.print(wBuf);
  if(drag>100){
    dtostrf(drag, 5, 1, wBuf);   // e.g. " 1209"
  }
  else if(drag>10){
    dtostrf(drag, 5, 2, wBuf);   // e.g. " 1209"
  }
  else if(drag>0){
    dtostrf(drag, 5, 3, wBuf);   // e.g. " 1209"
  }
  else{
    dtostrf(drag, 5, 1, wBuf);   // e.g. " 1209"
  }
  display.setTextSize(1);           // 12×16 px per char
  display.setCursor(5, 33);
  display.print("D:");
  display.print(wBuf);
  display.setTextSize(1);
  display.setCursor(5, 42);
  display.print(F("   grams"));

  // ── SPEED value (airspeed) ──────────────────────────────
  char sBuf[8];
  dtostrf(airspeed, 4, 1, sBuf);    // e.g. "10.3"

  display.setTextSize(2);
  display.setCursor(66, 24);
  display.print(sBuf);
  display.setTextSize(1);
  display.setCursor(66, 44);
  display.print(F("m/s"));

  // ── Divider above bottom bar ────────────────────────────
  display.drawFastHLine(0, 51, SCREEN_W, SSD1306_WHITE);

  // ── BOTTOM BAR: T xx°C   xxxx hPa ───────────────────────
  // Use BMP temp if available, fall back to DHT
  float dispTemp = bmp_ok ? bmp_temp : dht_temp;

  char tBuf[8], pBuf[8];
  dtostrf(dispTemp,     4, 1, tBuf);   // "28.0"
  dtostrf(bmp_pressure, 5, 0, pBuf);   // " 1013"

  display.setTextSize(1);
  display.setCursor(0, 54);
  display.print(F("T "));
  display.print(tBuf);
  display.print(F("\xF7""C"));          // degree symbol + C

  // Pressure on right side of bottom bar
  char fullP[12];
  snprintf(fullP, sizeof(fullP), "%shPa", pBuf);
  int16_t px2 = SCREEN_W - (int16_t)strlen(fullP) * 6;
  display.setCursor(px2, 54);
  display.print(fullP);
  P2(",p:",bmp_pressure);
  P2(",t:",dispTemp);
  P2(",s:",airspeed);
  display.display();
  PL();
}

// ─────────────────────────────────────────────────────────
//  SETUP
// ─────────────────────────────────────────────────────────
void setup() {
  Serial.begin(9600);
  Wire.begin();
  delay(1000);
  P("Started Arduino\n");

  // OLED init
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("OLED fail"));
    while (true);
  }
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);

  // Boot splash
  display.setTextSize(1);
  display.setCursor(10, 0);  display.println(F("MAV LABS IISc Blr"));
  display.drawFastHLine(0, 10, 128, SSD1306_WHITE);
  display.setCursor(0, 14);

  display.print(F("BMP180    .. "));  display.display();
  bmp_ok = bmp.begin();
  // bmp_ok = myBMP.begin();
  display.println(bmp_ok ? F("OK") : F("FAIL"));  display.display(); delay(200);

  // display.print(F("DHT11     .. "));  display.display();
  // dht.begin();
  // display.println(F("OK"));  display.display(); delay(200);

  display.print(F("HX711     .. "));  display.display();
  scale.begin(DOUT_PIN, SCK_PIN);
  scale.set_scale(CALIB_FACTOR);
  scale.tare();
  scale2.begin(DOUT_PIN2, SCK_PIN2);
  scale2.set_scale(CALIB_FACTOR);
  scale2.tare();
  display.println(F("tared"));  display.display(); delay(200);

  display.print(F("Pitot Tube.. "));  display.display();
  pitot_ok = readPitot();
  display.println(pitot_ok ? F("OK") : F("FAIL"));  display.display(); delay(800);

  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(16, 22);
  display.println(F("Starting"));
  display.display();
  delay(600);
}

// ─────────────────────────────────────────────────────────
//  LOOP
// ─────────────────────────────────────────────────────────
void loop() {
  // FLAG();
  // ── Read sensors ───────────────────────────────────────
  if (bmp_ok) {
    bmp_temp     = bmp.readTemperature();
    // bmp_temp     = myBMP.getTemperature();
    bmp_pressure = bmp.readPressure();
  }

  // float h = dht.readHumidity();
  // float t = dht.readTemperature();
  // if (!isnan(h)) dht_hum  = h;
  // if (!isnan(t)) dht_temp = t;

  pitot_ok = readPitot();

  if (scale.is_ready())
    weight_g = scale.get_units(1);
  if (scale2.is_ready())
    drag = scale2.get_units(1);

  // ── Serial dump ────────────────────────────────────────
  // Serial.println(F("=== SENSORS ==="));
  // Serial.print(F("Lift (weight): ")); Serial.print(weight_g, 1);    Serial.println(F(" g"));
  // Serial.print(F("Speed:         ")); Serial.print(airspeed, 2);    Serial.println(F(" m/s"));
  // Serial.print(F("Temp (BMP):    ")); Serial.print(bmp_temp, 1);    Serial.println(F(" C"));
  // Serial.print(F("Pressure:      ")); Serial.print(bmp_pressure,1); Serial.println(F(" hPa"));
  // // Serial.print(F("Temp (DHT):    ")); Serial.print(dht_temp, 1);    Serial.println(F(" C"));
  // // Serial.print(F("Humidity:      ")); Serial.print(dht_hum, 1);     Serial.println(F(" %"));
  // Serial.println();
  // FLAG();
  // ── Draw screen ────────────────────────────────────────
  drawMAVScreen();
  // FLAG();

  // FLAG();
  delay(30);
}
