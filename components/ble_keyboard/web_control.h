#pragma once
#include "esphome/core/defines.h"

#ifdef USE_BLE_KEYBOARD_WEB_CONTROL

#include "esphome/components/web_server_base/web_server_base.h"

namespace esphome {
namespace ble_keyboard {

class BleKeyboard;  // forward declaration

class BleKeyboardWebControl {
 public:
  BleKeyboardWebControl(web_server_base::WebServerBase *base, BleKeyboard *keyboard)
      : base_(base), keyboard_(keyboard) {}
  void setup();

 protected:
  web_server_base::WebServerBase *base_;
  BleKeyboard *keyboard_;
};

}  // namespace ble_keyboard
}  // namespace esphome

#endif  // USE_BLE_KEYBOARD_WEB_CONTROL
