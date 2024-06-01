#include "SBHClimate.h"

namespace esphome {
namespace sbh20 {

void SBHClimate::update()
{
	SBH20IO *sbh = get_parent()->sbh();

    if (sbh->isHeaterOn())
      if (sbh->isHeaterStandby())
        this->action = esphome::climate::CLIMATE_ACTION_IDLE;
      else
        this->action = esphome::climate::CLIMATE_ACTION_HEATING;
    else if (sbh->isFilterOn()) 
      this->action = esphome::climate::CLIMATE_ACTION_FAN;
    else if (!sbh->isPowerOn()) 
      this->action = esphome::climate::CLIMATE_ACTION_OFF;
    else  
      this->action = esphome::climate::CLIMATE_ACTION_IDLE;

    if (sbh->isHeaterOn())
      this->mode = esphome::climate::CLIMATE_MODE_HEAT;
    else if (sbh->isFilterOn()) 
      this->mode = esphome::climate::CLIMATE_MODE_FAN_ONLY;
    else
      this->mode = esphome::climate::CLIMATE_MODE_OFF;

	this->current_temperature = sbh->getCurrentTemperature();

	int targetTemp = sbh->getTargetTemperature();

	this->target_temperature = (targetTemp != SBH20IO::UNDEF::USHORT) ? targetTemp : SBH20IO::WATER_TEMP::SET_MIN;

	if (targetTemp == SBH20IO::UNDEF::USHORT)
	{
		ESP_LOGD("SBHClimate", "Target temp is undef, pressing the down button...");
		sbh->forceReadTargetTemperature(); // we'll learn the real target temp in near future...
	}

	publish_state();
}

void SBHClimate::control(const esphome::climate::ClimateCall &call)
{
	auto tt = call.get_target_temperature();
	if (tt)
	{
		if (!get_parent()->sbh()->isPowerOn()) {
			get_parent()->sbh()->setPowerOn(true);
			delay(1000);
		}
		get_parent()->sbh()->setTargetTemperature(*tt);
	}

	auto mode = call.get_mode();
	if (mode)
	{
		if (*mode == climate::CLIMATE_MODE_OFF) {
			get_parent()->sbh()->setPowerOn(false);
		}
		else if (*mode == climate::CLIMATE_MODE_HEAT){
			get_parent()->sbh()->setHeaterOnEx(true);
		}
		else if (*mode == climate::CLIMATE_MODE_FAN_ONLY){
			get_parent()->sbh()->setHeaterOnEx(false);
			get_parent()->sbh()->setFilterOnEx(true);
      }
	}
}

esphome::climate::ClimateTraits SBHClimate::traits()
{
	esphome::climate::ClimateTraits rv;

	rv.set_visual_min_temperature(SBH20IO::WATER_TEMP::SET_MIN);
	rv.set_visual_max_temperature(SBH20IO::WATER_TEMP::SET_MAX);
	rv.set_visual_temperature_step(1);
	rv.set_supports_current_temperature(true);
	rv.set_supports_action(true);
	rv.set_supported_modes(
		{climate::CLIMATE_MODE_OFF, climate::CLIMATE_MODE_HEAT, climate::CLIMATE_MODE_FAN_ONLY});

	return rv;
}

}}
