# Heartbridge: iOS Heart Rate Data Export

[![Build Status](https://travis-ci.com/mm/heartbridge.svg?token=yXBeMYKrVPs7F4WBmP1R&branch=master)](https://travis-ci.com/mm/heartbridge)

Combined with an Apple Watch, the iOS Health app contains a wealth of heart rate readings. I always found these readings a little difficult to play with in the Health app, and couldn't find a way to easily export them to a format I could manipulate/visualize the readings using (like a JSON or CSV file).

Fortunately with the [Shortcuts](https://apps.apple.com/us/app/shortcuts/id915249334) app, accessing this data is a lot easier. This combines a shortcut with a quick HTTP endpoint to transfer heart rate data from your iOS device to your Mac or PC. It was a fun little experiment for me to see how these two could work together. It has no dependencies besides what's already included in the Python standard library.

Heartbridge is a command-line program that can receive data from Shortcuts (via HTTP), automatically export it to the directory of your choosing (in CSV or JSON format) and automatically name files according to what date range they cover. Exported files contain a time stamp ("Start Date" in Health) and heart rate ("Value" in Health).

**_Note_**: This is designed to be run on your local computer! It wasn't made to be deployed to a server or anything and is not production ready. Only run if you trust the devices on your local network.

## Requirements

You will need two things:

* A computer with Python (>=3.6) installed
* An iPhone with [Shortcuts](https://apps.apple.com/us/app/shortcuts/id915249334) installed, on the same network

On the first run, the shortcut will prompt for access to your Health data (particularly heart rate data).

## Getting Started

1. Install heartbridge using [pip](https://pip.pypa.io/en/stable/) at a command line (or use the distribution packages under [releases](https://github.com/mm/heartbridge/releases)):

```bash
pip install heartbridge
```

2. Afterwards, run `heartbridge` at your command line:

```bash
heartbridge
```

This will save all exported files to the current working directory in CSV format. You can override both of these things with the `--directory` and `--type` arguments. If I wanted JSON files on my desktop instead, I could go with:

```bash
heartbridge --directory ~/Desktop --type json
```

You can also change the port heartbridge will listen for data on (by default 8888) by passing an argument to `port`. For a full list of arguments you can pass, type `heartbridge --help`.

3. Make note of the endpoint URL the script prints out, and ensure the script is allowed to accept incoming connections if your firewall prompts you. In this case, mine would be ```http://matt-mac.local:8888```:

![The line of terminal output "Waiting to receive heart rate sample data at http://matt-mac.local:8888" tells me that my endpoint URL is http://matt-mac.local:8888](https://raw.githubusercontent.com/mm/heartbridge/master/img/endpoint-image.png)

4. On your iPhone, [download the shortcut to extract Health samples](https://www.icloud.com/shortcuts/e4257a3986354ca79c8618c4e480bd5a). It will ask you what the HTTP endpoint URL you just noted is.

5. Run the shortcut! You will be prompted to select the date range you want to cover. The end date of the date range you specify is not included in the data returned. For example, to get all data for May 2nd, 2020:

![To select all data for May 2nd, 2020, you would select a date range between May 2nd and 3rd](https://raw.githubusercontent.com/mm/heartbridge/master/img/shortcut-iPhone.jpeg)

The script will output information about the data it receives from the shortcut to the console:

![Information about the data received by the script (number of samples and path of the file produced) is outputted to the console](https://raw.githubusercontent.com/mm/heartbridge/master/img/script-output.png)

6. The program will continue to run and listen for new data until stopped. Stop running the script (Ctrl-C) whenever you're finished exporting all the data you need. Enjoy exploring your heart rate data!

## All Command Line Options:

* ```--help```: Prints help text.
* ```--directory```: Set the output directory for exported files. Defaults to current directory. Will create directory if it doesn't already exist.
* ```--type```: Set the output file type. Can be csv or json. Defaults to csv.
* ```--port```: Set the port to listen for HTTP requests on. Defaults to 8888.

## Notes

### Shortcuts data format

This wasn't trivial to me, so I figured I'd write a quick bit on how the Health data is pulled using Shortcuts to begin with. The shortcut uses the "Find All Health Samples where" action:

![A screenshot of the "Find All Health Samples where" action](https://raw.githubusercontent.com/mm/heartbridge/master/img/find_action.jpeg)

This returns a result set of health samples including the start date of the reading, the value and the duration the reading was taken for. What I found difficult was exporting multiple attributes of this set's data at once -- I was only able to export the date into one array (an array of dates) and the actual heart rate value into one array (an array of values). Once these are tied into a dictionary, the resulting JSON the shortcut produces looks something like this:

```json
{
    "hrDates": ["2019-12-16 08:24:36","2019-12-16 08:26:39",...],
    "hrValues": ["74","72",...]
}
```

Both the ```hrDates``` and ```hrValues``` list is ordered in ascending order by start date. Doing it this way allowed me to avoid using a "Repeat with Each..." action on the health sample set which introduced a lot of slowness to the shortcut. 

Among other things, the Python script is used to combine those two arrays into a list of tuples. The above JSON would be transformed into ```[("2019-12-16 08:24:36", 74.0), ("2019-12-16 08:26:39", 72.0)]``` by the script, once it's received in an HTTP POST request. It's then converted to a CSV or JSON file. 