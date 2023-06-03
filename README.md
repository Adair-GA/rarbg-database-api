# rarbg-database-api
Since the rarbg website has been deleted but there's a database available, I thought to make a small API mocking tool that queries the sqlite db as if it were the real API, so that apps which rely on it can still be used.
At the moment, it's only compatible with radarr.

## How to use:
You need the aformentioned database, I can't provide it directly, but it shouldn't be too hard to find
1. Clone this project
2. Run ```pip install -r requirements.txt```
3. Run ```python app.py``` (it uses port 80 so you may need to run it as root)
4. Set the IP address in Radarr's indexer settings to point to the IP of the device that is running this script

## Disclaimer
It's a very basic project that I've built in an afternoon, so it probably won't support a lot of things. The RARBG API wasn't very well documented, so it's more of an approximation.
There will probably be some things that will crash it, but contributions are welcomed
