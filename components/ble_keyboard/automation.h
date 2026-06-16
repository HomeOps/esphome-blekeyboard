#pragma once
#include "esphome/core/automation.h"
#include "ble_keyboard.h"
#include <string>

namespace esphome {
namespace ble_keyboard {

class SendStringTrigger : public Trigger<> {
 public:
  explicit SendStringTrigger(BleKeyboard *parent, std::string str)
      : parent_(parent), str_(std::move(str)) {}
  void trigger() { parent_->send_string(str_); }
 protected:
  BleKeyboard *parent_;
  std::string str_;
};

class SendCtrlAltDelTrigger : public Trigger<> {
 public:
  explicit SendCtrlAltDelTrigger(BleKeyboard *parent) : parent_(parent) {}
  void trigger() { parent_->send_ctrl_alt_del(); }
 protected:
  BleKeyboard *parent_;
};

class RssiAboveTrigger : public Trigger<int> {
 public:
  RssiAboveTrigger(BleKeyboard *parent, int8_t threshold) {
    parent->add_rssi_above_callback([this, threshold](int8_t rssi) {
      if (rssi > threshold) this->trigger(rssi);
    });
  }
};

class RssiBelowTrigger : public Trigger<int> {
 public:
  RssiBelowTrigger(BleKeyboard *parent, int8_t threshold) {
    parent->add_rssi_below_callback([this, threshold](int8_t rssi) {
      if (rssi < threshold) this->trigger(rssi);
    });
  }
};

}  // namespace ble_keyboard
}  // namespace esphome
