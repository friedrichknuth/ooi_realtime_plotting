#! /usr/bin/env python

from functions import common_pete

username = 'OOIAPI-9N9UMLHV9W5GOP'
token = 'SJN6HXHH116OZ8'

sub_site = 'CE02SHBP'
platform = 'LJ01D'
instrument = '06-CTDBPN106'
delivery_method = 'streamed'
stream = 'ctdbp_no_sample'
parameter = 'ctdbp_no_seawater_pressure'


common.requestRealtime(username, token, sub_site, platform, instrument, delivery_method, stream, parameter)






	
## ctdbp_no_sample
# seawater_temperature
# ctdbp_no_seawater_pressure
# ctdbp_no_seawater_conductivity
# ctdbp_no_practical_salinity
# ctdbp_no_seawater_density
# ctdbp_no_abs_oxygen