#! /usr/bin/env python

from functions import common

# Go to ooinet.oceanobservatories.org, log in and find your username under your user profile.
username = 'YOUR_API_USER'
token = 'YOUR_API_TOKEN'


# Specify your inputs. Use https://ooi.visualocean.net/ as a reference.
sub_site = 'CE02SHBP'
platform = 'LJ01D'
instrument = '06-CTDBPN106'
delivery_method = 'streamed'
stream = 'ctdbp_no_sample'
parameter = 'seawater_temperature'

# Don't change this
common.requestRealtime(username, token, sub_site, platform, instrument, delivery_method, stream, parameter)

# Run the script from a unix shell $ python CE02SHBP.py &
# The & will allow you to modify parameters in the script and fire up another plot alongside the existing plot.




### Other parameters for the example listed above
## ctdbp_no_sample
# seawater_temperature
# ctdbp_no_seawater_pressure
# ctdbp_no_seawater_conductivity
# ctdbp_no_practical_salinity
# ctdbp_no_seawater_density
# ctdbp_no_abs_oxygen