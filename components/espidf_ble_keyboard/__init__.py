import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID

DEPENDENCIES = ["esp32"]

# Define configuration keys
CONF_DEVICE_NAME = "device_name"
CONF_KEY_DELAY_MS = "key_delay_ms"
CONF_PASSKEY = "passkey"
CONF_PASSKEY_MODE = "passkey_mode"
CONF_WEB_CONTROL = "web_control"
CONF_HOST_SLOTS = "host_slots"
CONF_HOSTS = "hosts"
CONF_SLOT = "slot"
PASSKEY_MODE_LEGACY = "legacy"
PASSKEY_MODE_SECURE_CONNECTIONS = "secure_connections"

espidf_ble_keyboard_ns = cg.esphome_ns.namespace("espidf_ble_keyboard")
EspidfBleKeyboard = espidf_ble_keyboard_ns.class_("EspidfBleKeyboard", cg.Component)


def _web_control_schema(config):
    """When web_control is true, require web_server_base."""
    if config.get(CONF_WEB_CONTROL):
        from esphome.components import web_server_base
        from esphome.components.web_server_base import CONF_WEB_SERVER_BASE_ID
        config = cv.Schema({
            cv.GenerateID(CONF_WEB_SERVER_BASE_ID): cv.use_id(
                web_server_base.WebServerBase
            ),
        }, extra=cv.ALLOW_EXTRA)(config)
    return config


HOST_SCHEMA = cv.Schema({
    cv.Required(CONF_SLOT): cv.int_range(min=0, max=9),
    cv.Optional(CONF_PASSKEY): cv.int_range(min=0, max=999999),
    cv.Optional(CONF_PASSKEY_MODE, default=PASSKEY_MODE_LEGACY): cv.one_of(
        PASSKEY_MODE_LEGACY,
        PASSKEY_MODE_SECURE_CONNECTIONS,
        lower=True,
    ),
})

CONFIG_SCHEMA = cv.All(
    cv.Schema({
        cv.GenerateID(): cv.declare_id(EspidfBleKeyboard),
        cv.Optional(CONF_DEVICE_NAME, default="ESP32 BLE KB"): cv.All(cv.string, cv.Length(max=29)),
        cv.Optional(CONF_KEY_DELAY_MS, default=80): cv.int_range(min=2, max=10000),
        cv.Optional(CONF_PASSKEY): cv.int_range(min=0, max=999999),
        cv.Optional(CONF_PASSKEY_MODE, default=PASSKEY_MODE_LEGACY): cv.one_of(
            PASSKEY_MODE_LEGACY,
            PASSKEY_MODE_SECURE_CONNECTIONS,
            lower=True,
        ),
        cv.Optional(CONF_WEB_CONTROL, default=False): cv.boolean,
        cv.Optional(CONF_HOST_SLOTS, default=4): cv.int_range(min=1, max=10),
        cv.Optional(CONF_HOSTS): cv.All(cv.ensure_list(HOST_SCHEMA)),
    }).extend(cv.COMPONENT_SCHEMA),
    _web_control_schema,
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    cg.add(var.set_device_name(config[CONF_DEVICE_NAME]))
    cg.add(var.set_key_delay_ms(config[CONF_KEY_DELAY_MS]))

    if CONF_PASSKEY in config:
        cg.add(var.set_passkey(config[CONF_PASSKEY]))

    cg.add(var.set_passkey_secure_connections(
        config[CONF_PASSKEY_MODE] == PASSKEY_MODE_SECURE_CONNECTIONS
    ))

    cg.add(var.set_host_slots(config[CONF_HOST_SLOTS]))

    if CONF_HOSTS in config:
        for host in config[CONF_HOSTS]:
            if CONF_PASSKEY in host:
                sc = host[CONF_PASSKEY_MODE] == PASSKEY_MODE_SECURE_CONNECTIONS
                cg.add(var.set_host_slot_passkey(host[CONF_SLOT], host[CONF_PASSKEY], sc))

    if config[CONF_WEB_CONTROL]:
        cg.add_define("USE_BLE_KEYBOARD_WEB_CONTROL")
        from esphome.components.web_server_base import CONF_WEB_SERVER_BASE_ID
        base = await cg.get_variable(config[CONF_WEB_SERVER_BASE_ID])
        BleKeyboardWebControl = espidf_ble_keyboard_ns.class_("BleKeyboardWebControl", cg.Component)
        web_control = cg.Pvariable(cg.ID("ble_keyboard_web_control", True, BleKeyboardWebControl),
                               cg.RawExpression(f"new esphome::espidf_ble_keyboard::BleKeyboardWebControl({base}, {var})"))
        cg.add(cg.App.register_component(web_control))

    # set_setup_priority() removed in ESPHome 2026.x
    # Priority is now set via get_setup_priority() override in the C++ header

    try:
        from esphome.components.esp32 import include_builtin_idf_component
        include_builtin_idf_component("bt")
        include_builtin_idf_component("nvs_flash")
    except ImportError:
        pass