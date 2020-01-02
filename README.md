# iOS Heart Rate Data Export

Combined with an Apple Watch, the iOS Health app contains a wealth of heart rate readings. I always found these readings a little difficult to play with in the Health app, and couldn't find a way to easily export them to a format I could manipulate/visualize the readings using (like a JSON or CSV file).

Fortunately with the [Shortcuts](https://apps.apple.com/us/app/shortcuts/id915249334) app, accessing this data is a lot easier. This combines a shortcut with a quick API endpoint (using [Flask](http://flask.palletsprojects.com/en/1.1.x/)) to capture and store the data the shortcut exports. 

This Python script can receive data from Shortcuts, automatically export it to the directory of your choosing (in CSV or JSON format) and automatically name files according to what date range it covers. Exported files contain a time stamp ("Start Date" in Health) and heart rate ("Value" in Health).

## Requirements

You will need two things:

* A computer with Python (>=3.5) installed
* An iPhone with [Shortcuts](https://apps.apple.com/us/app/shortcuts/id915249334) installed

On the first run, the shortcut will prompt for access to your Health data (particularly heart rate data).

## How to use

Clone this repository to your computer, and install required packages:

Afterwards, run `app.py`, specifying where you want export files stored and in what format you want them exported to (JSON/CSV). For example, this command:

```bash
python3 app.py --directory ~/Desktop --type csv
```

... will save all exported files to the desktop in CSV format. If no arguments are specified, the script will output files in CSV format to the current working directory. Please make sure the folder exists before running the script.

Make note of the REST endpoint URL the script prints out, and ensure the script is allowed to accept incoming connections if your firewall prompts you. In this case, mine would be ```http://Matt-Mac-mini.local:5000/heartrate```.

On your iPhone, [download the shortcut to extract Health samples](https://www.icloud.com/shortcuts/2d24033f74bb493c8017e4986e6233bf). It will ask you what the REST endpoint URL you noted in (3) is. 

Run the shortcut, select the date range you want to cover, and the data will export! Stop running the script whenever you're finished exporting all the data you need. 

