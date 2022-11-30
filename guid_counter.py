#!/usr/bin/python3
# -*- coding: utf-8 -*-

from mastodon import Mastodon
from datetime import date, datetime
import json, logging, schedule, time

_client: Mastodon = None  # type: ignore

# load values from json formatted .config file
config = json.load(open(".config", 'r'))
current = json.load(open("guid.json", 'r'))

def create() -> Mastodon:
	client: Mastodon
	try:
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
	logging.info("Starting client...")
	if _client is None:
		_client = create()
	logging.info("Started client.")

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

def save_progress():
  global current
  with open('guid.json', "w") as guid_file:
    guid_file.write(json.dump(current))

def guid_count_post():
	logging.info(datetime.now().isoformat())
	# get display formatted guid
	toot_text = get_display()
	logging.info(toot_text)
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
	logging.basicConfig(filename='guid_counter.log',level=logging.DEBUG)
	logging.info(datetime.now().isoformat())
	logging.info("GUIDs!")

	client_start()
	scheduler_start()

if __name__ == "__main__":
	main()
