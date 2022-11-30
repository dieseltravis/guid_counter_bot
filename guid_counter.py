#!/usr/bin/python3
# -*- coding: utf-8 -*-

from mastodon import Mastodon
from datetime import date, datetime
import json, logging, schedule, time

_client: Mastodon = None  # type: ignore

# load values from json formatted .config file
config = json.load(open(".config", 'r'))
guidObject = json.load(open("guid.json", 'r'))
current = guidObject["guid"]

def create() -> Mastodon:
	client: Mastodon
	try:
		logging.info("Creating client...")
		client = Mastodon(
				client_id = config["key"],
				client_secret = config["secret"],
				access_token = config["token"],
				api_base_url = config["api_base_url"],
				user_agent = "GUID Counter v1.0 (using mastodonpy)"
			)
	except Exception as error:
		logging.error(repr(error))
		exit()
	return client

def client_start():
	global _client
	if _client is None:
		_client = create()

def get_display() -> str:
	global current
	formatted = ""
	index = 0
	for d in current:
		if index in (8, 12, 16, 20):
			formatted += "-"
		# display single digit in hex
		formatted += format(d, "1X")
		index += 1
	return formatted

def increment():
	global current
	logging.info("before: %s", current)
	digitLength = len(current)
	last = digitLength - 1
	# start at the right-most digit
	indeces = range(last, -1, -1)
	# increment smallest digit
	current[last] += 1
	carry = 0
	for i in indeces:
		# if 1 is carried, increment and reset carry
		if carry == 1:
			current[i] += 1
			carry = 0
		# if current digit is over, reset and carry the 1
		if current[i] > 15:
			current[i] = 0
			carry = 1
	logging.info("after: %s", current)

def save_progress():
  global guidObject
  global current
  guidObject["guid"] = current
  with open('guid.json', "w") as guid_file:
    guid_file.write(json.dumps(guidObject))

def guid_count_post():
	# get display formatted guid
	logging.info("formatting: %s", current)
	toot_text = get_display()
	logging.info("formatted: %s", toot_text)

	# make sure client exists
	client_start()
	_client.status_post(toot_text)
	# increment guid
	increment()
	# write to JSON file
	save_progress()

def scheduler_start():
	logging.info("Starting scheduler")
	schedule.every().day.at('12:00').do(guid_count_post)
	# use listener to read user stream
	while True:
		schedule.run_pending()
		time.sleep(1)

def main():
	global current
	logging.basicConfig(filename='guid_counter.log',
                     	format='%(asctime)s %(message)s',
											level=logging.DEBUG)
	logging.info("GUIDs!")
	logging.info("initial: %s", current)
	logging.info("formatted: %s", get_display())
	logging.info("json: %s", json.dumps(current))
	scheduler_start()

if __name__ == "__main__":
	main()
