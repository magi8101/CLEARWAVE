// Simple ESP32-CAM (AI Thinker) test: no WiFi. Open serial monitor at 115200.
#include "esp_camera.h"

#define FLASH 4  // onboard white LED

void setup() {
  Serial.begin(115200);
  pinMode(FLASH, OUTPUT);

  camera_config_t c = {};
  c.ledc_channel = LEDC_CHANNEL_0;
  c.ledc_timer = LEDC_TIMER_0;
  c.pin_d0 = 5; c.pin_d1 = 18; c.pin_d2 = 19; c.pin_d3 = 21;
  c.pin_d4 = 36; c.pin_d5 = 39; c.pin_d6 = 34; c.pin_d7 = 35;
  c.pin_xclk = 0; c.pin_pclk = 22; c.pin_vsync = 25; c.pin_href = 23;
  c.pin_sccb_sda = 26; c.pin_sccb_scl = 27;
  c.pin_pwdn = 32; c.pin_reset = -1;
  c.xclk_freq_hz = 20000000;
  c.pixel_format = PIXFORMAT_JPEG;
  c.frame_size = FRAMESIZE_QVGA;  // small = works even without PSRAM
  c.jpeg_quality = 12;
  c.fb_count = 1;

  esp_err_t err = esp_camera_init(&c);
  Serial.println(err == ESP_OK ? "CAMERA OK" : "CAMERA FAILED");
  if (err != ESP_OK) Serial.printf("error 0x%x\n", err);
}

void loop() {
  digitalWrite(FLASH, HIGH); delay(100); digitalWrite(FLASH, LOW);
  camera_fb_t *fb = esp_camera_fb_get();
  if (fb) {
    Serial.printf("frame %dx%d, %u bytes\n", fb->width, fb->height, fb->len);
    esp_camera_fb_return(fb);
  } else {
    Serial.println("no frame");
  }
  delay(1000);
}
