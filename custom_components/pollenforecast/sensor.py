# Sensor for scrape Weeronline.nl
import logging
import datetime
import json
import voluptuous as vol

from homeassistant.util import dt
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ATTRIBUTION, CONF_NAME, CONF_SCAN_INTERVAL, CONF_URL, CONF_TYPE)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.restore_state import RestoreEntity

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = 'Information provided by Weeronline.nl'

DEFAULT_NAME = 'Pollenforecast'

SCAN_INTERVAL = datetime.timedelta(seconds=300)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_URL): cv.string,
    vol.Optional(CONF_SCAN_INTERVAL, default=SCAN_INTERVAL):
        cv.time_period,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    url = config.get(CONF_URL)
    name = config.get(CONF_NAME)
    add_entities([PollenForecast(url, name)], True)

class PollenForecast(RestoreEntity):
    def __init__(self, url, name):
        # initialiseren sensor
        self._unique_id = "pollenforecastsensor"
        self._url = url
        self._name = name
        self._state = 0
        self._attributes = {}
        self.update()

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def name(self):
        return self._name

    @property
    def unit_of_measurement(self):
        # Return the unit of measurement of this entity, if any.
        return 

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        # Return the state attributes.
        return self._attributes

    @property
    def icon(self):
        return self._icon

    def update(self):
        import requests
        from bs4 import BeautifulSoup

        hayfever_ratings = list()
        # days = list()
        response = requests.get(self._url + '/hooikoorts')
        data = BeautifulSoup(response.text, 'html.parser')
        # Get hayfever ratings
        for div in data.find_all('div', class_="styled__Row-sc-109dtq6-2 styled__RowDouble-sc-109dtq6-3 jowMLg jFjPWB"):
            for span in div.find_all('span', class_="styled__Label-sc-109dtq6-4 gNjHjv"):
                if span.text == "Grassen":
                    for span2 in div.find_all('span', class_="Icon__Container-glcq76-0 ckAteM"):
                        for img in span2.find_all('img'):
                            hayfever_ratings.append(int((img['alt']).rsplit("_")[2]))

        # # Get days of hayfever ratings
        # for div in data.find_all('div', class_="styled__Row-sc-109dtq6-2 jowMLg"):
        #     for div2 in div.find_all('div', class_="styled__RowItem-sc-109dtq6-7 dTAJLg"):
        #         days.append(div2.text)
        #     break

        # pollenforecast = dict(zip(days, hayfever_ratings))
        forecast_mapping = {0: "zeer klein",
                  1: "klein",
                  2: "matig",
                  3: "groot",
                  4: "zeer groot"}
        day_mapping = {0: 'vandaag', 1: 'morgen', 2: 'overmorgen', 3: 'over 3 dagen', 4: 'over 4 dagen'}
        self._state = forecast_mapping[hayfever_ratings[0]]
        for i in range(4):
            self._attributes[day_mapping[i]] = forecast_mapping[hayfever_ratings[0]]

        self._icon = f'mdi:numeric-{hayfever_ratings[0]}-circle-outline'