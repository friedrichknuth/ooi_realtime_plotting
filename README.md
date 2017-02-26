# OOI Real Time Plotting
This toolbox contains scripts to set up a real time display of OOI data.


#Installation

    > git clone git@github.com:ooi-data-review/ooi_realtime_plotting.git

    > cd ooi_realtime_plotting

    > pip insall -r requirements.txt


#Use

Open request_current_data.py or request_historic_data.py and modify the inputs. 

* request_current_data.py will plot real time data as soon as it is available
* request_historic_data.py will plot data starting at a historic point in time, specified by the user, and just forward in 10 second leaps.
* Optionally, you can specify to write the data to csv as it streams in from either script

After modifying the inputs, run the script from a linux or unix shell like this:

    $ python request_current_data.py &

or

    $ python request_historic_data.py &
    
The '&' will allow you to modify inputs in the script.py and fire up another plot alongside the existing plot. Terminating the bash shell will kill all processes fired up in the background. In this way, using '&' is not equivalent to nohup.
