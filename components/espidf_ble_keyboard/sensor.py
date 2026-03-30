import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    DEVICE_CLASS_SIGNAL_STRENGTH,
    STATE_CLASS_MEASUREMENT,
    UNIT_DECIBEL_MILLIWATT,
)
from . import EspidfBleKeyboard, espidf_ble_keyboard_ns

DEPENDENCIES = ["espidf_ble_keyboard"]

CONF_KEYBOARD_ID = "keyboard_id"

CONFIG_SCHEMA = sensor.sensor_schema(
    unit_of_measurement=UNIT_DECIBEL_MILLIWATT,
    accuracy_decimals=0,
    device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
    state_class=STATE_CLASS_MEASUREMENT,
).extend(
    {
        cv.Required(CONF_KEYBOARD_ID): cv.use_id(EspidfBleKeyboard),
        cv.Optional("update_interval", default="10s"): cv.update_interval,
    }
)


async def to_code(config):
    var = await sensor.new_sensor(config)
    parent = await cg.get_variable(config[CONF_KEYBOARD_ID])
    cg.add(parent.set_rssi_sensor(var))
    interval_ms = int(config["update_interval"].total_milliseconds)
    cg.add(parent.set_rssi_update_interval(interval_ms))
