#! /usr/bin/env python

from functions import common

# Go to ooinet.oceanobservatories.org, log in and find your username under your user profile.
username = 'OOIAPI-9N9UMLHV9W5GOP'
token = 'SJN6HXHH116OZ8'


# # Specify your inputs for the data request. Use http://ooi.visualocean.net as a reference.
sub_site = 'RS03AXPS'
platform = 'SF03A'
instrument = '2A-CTDPFA302'
delivery_method = 'streamed'
stream = 'ctdpf_sbe43_sample'

# note that requests are sent for the entire stream, from which the parameter input here is parsed out for plotting. 
parameter = 'corrected_dissolved_oxygen'

# specify the date and time you want to begin replaying data from
year = 2016
month = 9
day = 14
hour = 1
minute = 0
second = 0

# set to true if you want to write data to a csv file in csv_output folder.
output_csv = True



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
