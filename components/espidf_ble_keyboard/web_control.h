#pragma once

#ifdef USE_BLE_KEYBOARD_WEB_CONTROL

#include "esphome/components/web_server_base/web_server_base.h"

namespace esphome {
namespace espidf_ble_keyboard {

class EspidfBleKeyboard;  // forward declaration

class BleKeyboardWebControl : public AsyncWebHandler {
 public:
  BleKeyboardWebControl(web_server_base::WebServerBase *base, EspidfBleKeyboard *keyboard);
  void setup();

  bool canHandle(AsyncWebServerRequest *request) override;
  void handleRequest(AsyncWebServerRequest *request) override;

 protected:
  void handle_page_(AsyncWebServerRequest *request);
  void handle_api_(AsyncWebServerRequest *request);

  web_server_base::WebServerBase *base_;
  EspidfBleKeyboard *keyboard_;
};

}  // namespace espidf_ble_keyboard
}  // namespace esphome

#endif  // USE_BLE_KEYBOARD_WEB_CONTROL
