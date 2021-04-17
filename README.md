# Heartbridge: iOS Health Data Export

![Python Package Tests](https://github.com/mm/heartbridge/actions/workflows/python-package.yml/badge.svg)

Heartbridge is a command-line tool that exports health data from your iOS device to your local computer, with the help of an iOS Shortcut. It supports exporting many types of data from the Health app, including:

- Heart Rate
- Resting Heart Rate
- Heart Rate Variability
- Steps
- Flights Climbed
- Cycling Distance

Heartbridge receives data from the [Shortcuts](https://apps.apple.com/us/app/shortcuts/id915249334) app (via HTTP), automatically exports it to the directory of your choosing (in CSV or JSON format) and automatically names files according to the health data type and date range they cover. Exported files contain a time stamp ("Start Date" in Health) and reading ("Value" in Health). To read more about how the file exports look depending on the data type, check out [Data Type Support](#data-type-support).

If you don't want to use the built-in CLI or server, you can also use Heartbridge to parse data from Shortcuts directly-- for example, if you wanted to automatically push data to a database on your own server.

**_Note_**: The CLI is designed to be run on your local computer! It's not production ready; only run if you trust the devices on your local network.

## Getting Started

You will need:
* A computer with Python (>=3.8) installed
* An iPhone with [Shortcuts](https://apps.apple.com/us/app/shortcuts/id915249334) installed, on the same network

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

    ```shell
    ➜ ~ heartbridge
    ⚡ Waiting to receive health data at http://matt-mac.local:8888... (Press Ctrl+C to stop)
    ```

4. On your iPhone, [download the shortcut to extract Health samples](https://www.icloud.com/shortcuts/22bb56e73c354d9aa76a3678548dfe3a). It will ask you what the HTTP endpoint URL you just noted is.

5. Open up the Shortcut. In the first step, you can change "Type" to be whatever data you're trying to export (Heart Rate is selected by default).

6. Run the shortcut! You will be prompted to select the date range you want to cover. The end date of the date range you specify is not included in the data returned. For example, to get all data for May 2nd, 2020:

    ![To select all data for May 2nd, 2020, you would select a date range between May 2nd and 3rd](https://raw.githubusercontent.com/mm/heartbridge/master/img/shortcut-iPhone.jpeg)

    The script will output information about the data it receives from the shortcut to the console:

    ```shell
    ➜ ~ heartbridge
    ⚡ Waiting to receive health data at http://matt-mac.local:8888... (Press Ctrl+C to stop)
    💛 Detected Heart Rate data with 8429 samples.
    ✅ Successfully exported data to /Users/mattmascioni/heart-rate-Apr01-2021-Apr16-2021.csv
    ```

7. The program will continue to run and listen for new data until stopped. Stop running the server (Ctrl-C) whenever you're finished exporting all the data you need. Enjoy exploring your health data!

## All Command Line Options

```shell
Usage: heartbridge [OPTIONS]

  Opens a temporary HTTP endpoint to send health data from Shortcuts to your
  computer.

Options:
  --directory DIRECTORY  Set the output directory for exported files. Defaults
                         to current directory. Will create directory if it
                         doesn not already exist.

  --type [csv|json]      Set the output file type. Can be csv or json.
                         Defaults to csv.

  --port INTEGER RANGE   Set the port to listen for HTTP requests on. Defaults
                         to 8888.
```

## Using Heartbridge without the CLI

Typing `heartbridge` in a shell opens up a temporary server to send data from the shortcut to your computer. If you don't want this behaviour (for example, if you already have a server that can accept the JSON data Shortcuts sends), you can use Heartbridge's Shortcuts data parsing tools directly, which are contained in the `Health` class. Say your endpoint stores the incoming request JSON in the `incoming_shortcuts_json` dict, you could then do things with the readings using: 

```python
>>> from heartbridge import Health

>>> health = Health()
>>> health.load_from_shortcuts(data=incoming_shortcuts_json)
>>> health.reading_type_slug
'heart-rate'
>>> first_reading = health.readings[0]
>>> first_reading.timestamp
datetime.datetime(2021, 4, 17, 14, 16, 31, 780731)
>>> first_reading.get_value()
40
>>> first_reading.to_dict()
{'timestamp': '2021-04-17 14:16:31', 'heart_rate': 40}
```

`health.readings` is a list of `BaseHealthReading`-subclassed data objects. Depending on the health data passed in, the class may be one of:

- Heart Rate: `HeartRateReading`
- Resting Heart Rate: `RestingHeartRateReading`
- Heart Rate Variability: `HeartRateVariabilityReading`
- Steps: `StepsReading`
- Flights Climbed: `FlightsClimbedReading`
- Cycling Distance: `CyclingDistanceReading`
- All others: `GenericHealthReading`

No matter what the class is, you can always access the `record.get_value()` and `record.to_dict()` methods to get the health sample value/dictionary representation respectively, and `.timestamp` property to get the health "Start Date" of the reading as a datetime.

## Notes

### Data Type Support

Heartbridge supports pretty much any Health record exported by Shortcuts. For some health records, there's built in support for adding relevant headers/keys in the resulting CSV/JSON file:

| Data Type              | Start Date Header/Key | Value Header/Key         |
|------------------------|-----------------------|--------------------------|
| Heart Rate             | `timestamp`           | `heart_rate`             |
| Resting Heart Rate     | `timestamp`           | `resting_heart_rate`     |
| Heart Rate Variability | `timestamp`           | `heart_rate_variability` |
| Steps                  | `timestamp`           | `step_count`             |
| Flights Climbed        | `timestamp`           | `climbed`                |
| Cycling Distance       | `timestamp`           | `distance_cycled`        |
| All other records      | `timestamp`           | `reading`                |

For example, if Steps data was sent, the resulting CSV file would have `timestamp, step_count` headers.

### Motivation for this project

Combined with an Apple Watch, the iOS Health app contains a wealth of heart rate and other health readings. I always found these readings a little difficult to play with in the Health app, and couldn't find a way to easily export them to a format I could manipulate/visualize the readings using (like a JSON or CSV file).

Fortunately with the [Shortcuts](https://apps.apple.com/us/app/shortcuts/id915249334) app, accessing this data is a lot easier. This combines a shortcut with a quick HTTP endpoint to transfer heart rate data from your iOS device to your Mac or PC. It was a fun little experiment for me to see how these two could work together. The original version of Heartbridge was for heart rate data only, but now it can work with more sample types!

### Shortcuts data format

The shortcut uses the "Find All Health Samples where" action:

![A screenshot of the "Find All Health Samples where" action](https://raw.githubusercontent.com/mm/heartbridge/master/img/find_action.jpeg)

This returns a result set of health samples including the start date of the reading, the value and the duration the reading was taken for. What I found difficult was exporting multiple attributes of this set's data at once -- I was only able to export the date into one array (an array of dates) and the actual heart rate value into one array (an array of values). Once these are tied into a dictionary, the resulting JSON the shortcut produces looks something like this:

```json
{
    "type": "Heart Rate",
    "dates": ["2019-12-16 08:24:36","2019-12-16 08:26:39",...],
    "values": ["74","72",...]
}
```

Both the ```dates``` and ```values``` list is ordered in ascending order by start date. Doing it this way allowed me to avoid using a "Repeat with Each..." action on the health sample set which introduced a lot of slowness to the shortcut. 

Among other things, the Python script is used to combine those two arrays into a list of tuples. The above JSON would be transformed into ```[("2019-12-16 08:24:36", 74), ("2019-12-16 08:26:39", 72)]``` by the script, once it's received in an HTTP POST request. It's then converted to a CSV or JSON file. 