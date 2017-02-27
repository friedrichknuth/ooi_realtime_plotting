#! /usr/bin/env python

import os
import datetime
import warnings
import csv
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import requests
from concurrent.futures import ThreadPoolExecutor

warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")


BASE_URL = 'https://ooinet.oceanobservatories.org/api/m2m/12576/sensor/inv/'
pool = ThreadPoolExecutor(1)

ntp_epoch = datetime.datetime(1900, 1, 1)
unix_epoch = datetime.datetime(1970, 1, 1)
ntp_ordinal = ntp_epoch.toordinal()
ntp_delta = (unix_epoch - ntp_epoch).total_seconds()

max_points = 10000

def create_output_dir(new_dir):
    # Check if dir exists.. if it doesn't... create it.
    if not os.path.isdir(new_dir):
        try:
            os.makedirs(new_dir)
        except OSError:
            if os.path.exists(new_dir):
                pass
            else:
                raise

def prune_data(n, max_points=max_points, write_csv = False):
    # print a warning if csv file begins to exceed msx_points
    if write_csv == True:
        if len(n) >= max_points:
            print "WARNING - csv file beginning to exceed " + str(max_points) + ' points.'
    
    return n[-max_points:]


def extract_keys(data, keys, min_time):
    rdict = {key: [] for key in keys}
    for record in data:
        if record['time'] <= min_time:
            continue
        for key in keys:
            rdict[key].append(record[key])
    # print 'Found %d data points after filtering' % len(rdict['time'])
    return rdict


def ntp_seconds_to_datetime(ntp_seconds):
    return datetime.datetime.utcfromtimestamp(ntp_seconds - ntp_delta).replace(microsecond=0)


def get_future_data(url, params, username, token):
    auth = (username, token)
    return pool.submit(requests.get, url, params=params, auth=auth)



def requestHistoric(username, token, sub_site, platform, instrument, delivery_method, stream, parameter, historic_date, write_csv = False):
    
    # TODO add end time as an input that specifies when the routine will end and save a plot
    # TODO make step forward timedelta a input and set according to expected sampling rate
    # TODO allow for multi-parameter input
    # TODO create plotting routines for 2-D datasets, depth profiles etc.

    request_url = '/'.join((BASE_URL, sub_site, platform, instrument, delivery_method, stream))
    params = {
        'beginDT': None,
        'endDT': None,
        'limit': 1000,
        'user': 'realtime',
    }

    begin_time = datetime.datetime(**historic_date) - datetime.timedelta(seconds=10)
    end_time = datetime.datetime(**historic_date)

    last_time = 10
    yvals = []
    time = []

    if write_csv == True:
        create_output_dir('csv_output')
        output = {}
        output_filename = './csv_output/' + parameter + '_' + begin_time.strftime('%Y-%m-%dT%H%M00') + '.csv'
        with open(output_filename, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(['time',parameter])

    plt.ion()
    plt.grid()  # Turn on the plot grid
    plt.title(sub_site + '-' + platform + '-' + instrument + '-' + stream, y=1.02)
    plt.ylabel(parameter)
    plt.plot(time, yvals, linestyle='None', marker='.')
    df = mdates.DateFormatter('%Y-%m-%dT%H:%M:%S')  # Format the date axis

    ax = plt.gca()
    fig = plt.gcf()

    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.xaxis.set_major_formatter(df)
    fig.autofmt_xdate()

    while True:
        # Update params for this request
        begin_time_str = begin_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        params['beginDT'] = begin_time_str

        end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        params['endDT'] = end_time_str

        # TODO parse out data requests as a sepearte function to write data to csv and save a plot

        # Send request in thread, polling until complete
        data_future = get_future_data(request_url, params, username, token)
        while not data_future.done:
            # Request not complete, yield control to event loop
            plt.pause(.1)

        # Request complete, if not 200, log error and try again
        response = data_future.result()
        if response.status_code != 200:
            print 'Error fetching data', response.text
            plt.pause(1)
            continue

        # Data is valid, extract the requested parameters for all data points
        # not already received.
        data = response.json()
        data = extract_keys(data, ['time', parameter], min_time=last_time)
        

        # write data to csv
        if write_csv == True:
            output.update(data)
            for key, value in output.iteritems():
                if key == 'time':
                    x = [x for x in value]
                if key == parameter:
                    y = [y for y in value]

            rows = zip(x,y)
            with open(output_filename, 'a') as f:
                writer = csv.writer(f)
                for row in rows:
                    writer.writerow(row)


        # It's possible to receive a response containing only already plotted data
        # If so, try again.
        if not data['time']:
            plt.pause(1)
            continue

        # Grab the last time so that we can filter out any previously received data
        # from the next request. Update begin_time to match.
        last_time = data['time'][-1]
        begin_time = ntp_seconds_to_datetime(last_time)
        end_time = ntp_seconds_to_datetime(last_time) + datetime.timedelta(seconds=10)

        # Add this data to our existing dataset, prune if over our max points
        time.extend((t / (24 * 3600) + ntp_ordinal for t in data['time']))
        yvals.extend(data[parameter])
        time = prune_data(time, write_csv = write_csv)
        yvals = prune_data(yvals)

        # reset our limits and plot the data
        ax.lines[0].set_xdata(time)
        ax.lines[0].set_ydata(yvals)
        ax.relim()
        ax.autoscale_view()

        plt.tight_layout()
        plt.pause(1)




def requestNow(username, token, sub_site, platform, instrument, delivery_method, stream, parameter, write_csv = False):
    request_url = '/'.join((BASE_URL, sub_site, platform, instrument, delivery_method, stream))
    params = {
        'beginDT': None,
        'limit': 1000,
        'user': 'realtime',
    }

    begin_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=10)
    last_time = 0
    yvals = []
    time = []
   

    if write_csv == True:
        create_output_dir('csv_output')
        output = {}
        output_filename = './csv_output/' + parameter + '_' + begin_time.strftime('%Y-%m-%dT%H%M00') + '.csv'
        with open(output_filename, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(['time',parameter])

    plt.ion()
    plt.grid()  # Turn on the plot grid
    plt.title(sub_site + '-' + platform + '-' + instrument + '-' + stream, y=1.02)
    plt.ylabel(parameter)
    plt.plot(time, yvals, linestyle='None', marker='.')
    df = mdates.DateFormatter('%m-%dT%H:%M:%S')  # Format the date axis

    ax = plt.gca()
    fig = plt.gcf()

    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.xaxis.set_major_formatter(df)
    fig.autofmt_xdate()

    while True:
        # Update params for this request
        begin_time_str = begin_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        params['beginDT'] = begin_time_str

        # Send request in thread, polling until complete
        data_future = get_future_data(request_url, params, username, token)
        while not data_future.done:
            # Request not complete, yield control to event loop
            plt.pause(.1)

        # Request complete, if not 200, log error and try again
        response = data_future.result()
        if response.status_code != 200:
            print 'Error fetching data', response.text
            plt.pause(1)
            continue

        # Data is valid, extract the requested parameters for all data points
        # not already received.
        data = response.json()
        data = extract_keys(data, ['time', parameter], min_time=last_time)
        
        # write data to csv
        if write_csv == True:
            output.update(data)
            for key, value in output.iteritems():
                if key == 'time':
                    x = [x for x in value]
                if key == parameter:
                    y = [y for y in value]

            rows = zip(x,y)
            with open(output_filename, 'a') as f:
                writer = csv.writer(f)
                for row in rows:
                    writer.writerow(row)

        # It's possible to receive a response containing only already plotted data
        # If so, try again.
        if not data['time']:
            plt.pause(1)
            continue

        # Grab the last time so that we can filter out any previously received data
        # from the next request. Update begin_time to match.
        last_time = data['time'][-1]
        begin_time = ntp_seconds_to_datetime(last_time)

        # Add this data to our existing dataset, prune if over our max points
        time.extend((t / (24 * 3600) + ntp_ordinal for t in data['time']))
        yvals.extend(data[parameter])
        time = prune_data(time, write_csv = write_csv)
        yvals = prune_data(yvals)

        # reset our limits and plot the data
        ax.lines[0].set_xdata(time)
        ax.lines[0].set_ydata(yvals)
        ax.relim()
        ax.autoscale_view()

        plt.tight_layout()
        plt.pause(1)