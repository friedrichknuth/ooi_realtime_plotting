#! /usr/bin/env python

from functions import common

# Go to ooinet.oceanobservatories.org, log in and find your username under your user profile.
username = 'YOUR-API-USERNAME'
token = 'YOUR-API-PASSWORD'


# Specify your inputs. Use http://ooi.visualocean.net/ as a reference.
sub_site = 'CE02SHBP'
platform = 'LJ01D'
instrument = '06-CTDBPN106'
delivery_method = 'streamed'
stream = 'ctdbp_no_sample'
parameter = 'ctdbp_no_seawater_pressure'

# specify the date and time you want to begin replaying data from
year = 2016
month = 12
day = 1
hour = 22
minute = 8
second = 0

# set to true if you want to write data to a csv file in csv_output folder.
output_csv = False 



historic_date = dict(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

common.requestHistoric(
						username, 
						token, 
						sub_site, 
						platform, 
						instrument, 
						delivery_method, 
						stream, 
						parameter, 
						historic_date,
						write_csv=output_csv)

# Run the script from a linux or unix shell $ python request_historic_data.py &
# The & will allow you to modify parameters in the script and fire up another plot alongside the existing plot.




# sub_site = 'CE02SHBP'
# platform = 'LJ01D'
# instrument = '06-CTDBPN106'
# delivery_method = 'streamed'
# stream = 'ctdbp_no_sample'
# parameter = 'seawater_temperature'
# parameter = 'ctdbp_no_seawater_pressure'
# parameter = 'ctdbp_no_seawater_conductivity'
# parameter = 'ctdbp_no_practical_salinity'
# parameter = 'ctdbp_no_seawater_density'
# parameter = 'ctdbp_no_abs_oxygen'




# sub_site = 'CE02SHBP'
# platform = 'LJ01D'
# instrument = '07-VEL3DC108'
# delivery_method = 'streamed'
# stream = 'vel3d_cd_velocity_data'
# parameter = 'vel3d_c_eastward_turbulent_velocity'
# parameter = 'vel3d_c_northward_turbulent_velocity'
# parameter = 'vel3d_c_upward_turbulent_velocity'
