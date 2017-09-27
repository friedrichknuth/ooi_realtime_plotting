# OOI Real Time Plotting
This toolbox is written in python 2 and contains scripts to stream data onto your local machine and plot in real time.


## Installation using conda

    > git clone git@github.com:ooi-data-review/ooi_realtime_plotting.git

    > cd ooi_realtime_plotting

    > conda create -n ooi_realtime_plotting python=2 matplotlib requests futures


## Use

Activate your new virtual environment called ooi_realtime_plotting

Open request_current_data.py or request_historic_data.py and modify the inputs. 

* request_current_data.py will plot real time data as soon as it is available
* request_historic_data.py will plot data starting at a historic point in time, specified by the user, and step forward in 3600 second increments.

After modifying the inputs, run the script from a linux or unix shell like this:

    $ python request_current_data.py &

or

    $ python request_historic_data.py &
    
The '&' will allow you to modify inputs in the .py file and fire up another plot alongside the existing plot. Terminating the bash shell will kill all processes fired up in the background. (Note: using '&' is not equivalent to nohup in this way)

* Optionally, you can specify to write the data to csv as it streams in from either script

## Note:
* When using request_historic_data.py, if there is no new historic data points within 3600 seconds from the last data point received, the script will not progress. For now, the increment can be increased in line 174 under functions/common.py to accomodate sparse datasets or to leap over expected gaps.

