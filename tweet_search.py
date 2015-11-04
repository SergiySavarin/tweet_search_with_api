#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import oauth2
import sys

from datetime import date, timedelta


def date_range():
	date_range = []
	for i in range(7):
		date_range.append((date.today() - 
			timedelta(i)).strftime('%Y-%m-%d'))
	date_range.reverse()
	return date_range


def get_token_data():
	token = []
	for i in open('tk.txt', 'r'):
		token.append(i.rstrip())
	return token


def get_request(date, method='GET'):
	consumer = oauth2.Consumer(key=get_token_data()[0], 
							secret=get_token_data()[1])
	client = oauth2.Client(consumer)
	resp, content = client.request((search_tweets_url(get_phrase()) + date), method)
	return content


def search_tweets_url(phrase):
	api_url = 'https://api.twitter.com/1.1/'
	search_url = api_url + 'search/tweets.json?q=' + phrase + \
				'&result_type=mixed&count=50&until='
	return search_url


def get_phrase():
	if len(sys.argv) != 2:
		print 'Enter your phrase or word in terminal like:'
		print '$ python', sys.argv[0], 'your phrase'
		sys.exit()
	else:
		phrase = str(sys.argv[1])
	return phrase


def colect_user_data(tweets_data, users_data):
	for user in tweets_data:
		user_data = []
		user_profile_data = user['user']
		user_data.append(user['id_str'].encode('utf-8'))
		user_data.append(user['text'].encode('utf-8'))
		user_data.append(user_profile_data['location'].encode('utf-8'))
		user_data.append(user_profile_data['lang'].encode('utf-8'))
		try:
			user_data.append(user_profile_data['time_zone'].encode('utf-8'))
		except:
			user_data.append(user_profile_data['time_zone'])
		if user_data not in users_data:
			users_data.append(user_data)
	return users_data


def colect_users_data_for_last_7_days():
	users_data = []
	for date in date_range():
		content = json.loads(get_request(date))
		tweets_data = content['statuses']
		users_data = colect_user_data(tweets_data, users_data)
	return users_data


def show_data():
	data = colect_users_data_for_last_7_days()
	for line in data:
		print line


def write_data_to_file(file_name):
	data = colect_users_data_for_last_7_days()
	data_file = open('%s' % file_name, 'w')
	for line in data:
		data_file.write(line)
	data_file.close()
	print 'Your data saved to %s' % file_name


def sort_data(sort_by=1):
	data = colect_users_data_for_last_7_days()
	list_for_sort = [x[sort_by + 1] for x in data]
	sorted_dict = {}
	for phrase in list_for_sort:
		if phrase in sorted_dict:
			sorted_dict[phrase] += 1
		else:
			sorted_dict[phrase] = 1
	values = [sorted_dict[x] for x in sorted_dict]
	values = sorted(values, reverse=True)
	values = values[0:3]
	sorted_list = [(x, y) for x in values for y in sorted_dict if sorted_dict[y] == x]
	return sorted_list

print sort_data(3)
# show_data()
# print colect_users_data_for_last_7_days(), len(colect_users_data_for_last_7_days())
