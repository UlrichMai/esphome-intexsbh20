import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate, sensor, binary_sensor, switch, text_sensor
from esphome.const import CONF_ID

DEPENDENCIES = ['climate', 'sensor', 'binary_sensor', 'switch', 'text_sensor']

AUTO_LOAD = []

CONF_CLIMATE = 'climate'
CONF_POWER = 'power'
CONF_FILTER = 'filter'
CONF_BUBBLE = 'bubble'
CONF_WATER_TEMPERATURE = 'water_temperature'
CONF_ERROR_TEXT = 'error_text'

sbh_ns = cg.esphome_ns.namespace('sbh20')

IntexSBH20 = sbh_ns.class_('IntexSBH20', cg.PollingComponent)
SBHClimate = sbh_ns.class_('SBHClimate', climate.Climate)
SBHSwitch = sbh_ns.class_('SBHSwitch', switch.Switch)

CONFIG_SCHEMA = cv.polling_component_schema('5s').extend({
	cv.GenerateID(): cv.declare_id(IntexSBH20),
	cv.Optional(CONF_CLIMATE): climate.CLIMATE_SCHEMA.extend({
		cv.GenerateID(): cv.declare_id(SBHClimate),
	}),
	cv.Optional(CONF_BUBBLE): switch.SWITCH_SCHEMA.extend({
		cv.GenerateID(): cv.declare_id(SBHSwitch),
	}),
	cv.Optional(CONF_WATER_TEMPERATURE): sensor.sensor_schema().extend(),
	cv.Optional(CONF_POWER): binary_sensor.binary_sensor_schema().extend(),
	cv.Optional(CONF_FILTER): binary_sensor.binary_sensor_schema().extend(),
	cv.Optional(CONF_ERROR_TEXT): text_sensor.text_sensor_schema().extend(),
})

async def to_code(config):
	var = cg.new_Pvariable(config[CONF_ID])
	await cg.register_component(var, config)

	if CONF_CLIMATE in config:
		clim = cg.new_Pvariable(config[CONF_CLIMATE][CONF_ID])
		await climate.register_climate(clim, config[CONF_CLIMATE])
		cg.add(var.set_climate(clim))

	if CONF_POWER in config:
		tx = await binary_sensor.new_binary_sensor(config[CONF_POWER])
		cg.add(var.set_switch_power(tx))

	if CONF_FILTER in config:
		tx = await binary_sensor.new_binary_sensor(config[CONF_FILTER])
		cg.add(var.set_switch_filter(tx))

	if CONF_BUBBLE in config:
		sw = cg.new_Pvariable(config[CONF_BUBBLE][CONF_ID])
		await switch.register_switch(sw, config[CONF_BUBBLE])
		cg.add(sw.set_type("bubble"))
		cg.add(var.set_switch_bubble(sw))

	if CONF_ERROR_TEXT in config:
		tx = await text_sensor.new_text_sensor(config[CONF_ERROR_TEXT])
		cg.add(var.set_error_text_sensor(tx))

	if CONF_WATER_TEMPERATURE in config:
		tx = await sensor.new_sensor(config[CONF_WATER_TEMPERATURE])
		cg.add(var.set_water_temperature_sensor(tx))
