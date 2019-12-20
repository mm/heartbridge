# iOS Heart Rate Data Export

Combined with an Apple Watch, the iOS Health app contains a wealth of heart rate readings. I always found these readings a little difficult to play with in the Health app, and couldn't find a way to easily export them to a format I could manipulate/visualize the readings using (like a JSON or CSV file).

Fortunately with the [Shortcuts](https://apps.apple.com/us/app/shortcuts/id915249334) app, accessing this data is a lot easier. This combines a shortcut with a REST endpoint (using [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)) to capture and store the data the shortcut exports. 