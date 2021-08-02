# Weeronline activity ratings
This platform scrapes the pollen forecast for the next 5 days from https://www.weeronline.nl/.

## HACS Installation
1. Make sure you've installed [HACS](https://hacs.xyz/docs/installation/prerequisites)
2. In the integrations tab, search for pollenforecast.
3. Install the Integration.
4. Go to https://www.weeronline.nl/, search your city and copy the url
4. Add weatherratings entry to configuration (see below)

## Configuration
```yaml
sensor:
  - platform: pollenforecast
    url: 'https://www.weeronline.nl/Europa/Frankrijk/Parijs/4266446'
    name: 'pollenforecast'
```

- url: weeronline url of the location (required)
- name: name of the sensor  (optional) default=pollenforecast

