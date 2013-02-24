#!/usr/bin/env python
import urllib, urllib2 
from random import randint, uniform
import json
import time

useragents = [
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17'},
	{'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'},
	{'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 3.5.30729)'}
	]

def print_position(song):
	ua = useragents[randint(0,len(useragents)-1)]
	url = 'http://wsun.s.takeover.ldrhub.com/api/takeover_queuelist_ids/wsun/?'
	request = urllib2.Request(url, None, ua)
	response = urllib2.urlopen(request)
	ids = json.loads(response.read())['takeover_queuelist_ids']
	position = ids.index(song)
	print "Song: %d = #%d" % (song, position + 1),
	
def get_list(song):
	ua = useragents[randint(0,len(useragents)-1)]
	url = 'http://wsun.s.takeover.ldrhub.com/api/takeover_queuelist_ids/wsun/?'
	request = urllib2.Request(url, None, ua)
	response = urllib2.urlopen(request)
	ids = json.loads(response.read())['takeover_queuelist_ids']
	position = ids.index(song)
	print "Song: %d = #%d" % (song, position + 1),
	start = 0
	if position > 20:
		start = position - 20 #urllen > 2k 
	return ids[start:position]


def get_cookie(url, ua):
	request = urllib2.Request(url, None, ua)
	response = urllib2.urlopen(request)
	return response.headers.get('Set-Cookie')


def me_up_them_down(song, upcount):
	ids = get_list(song) 

	query = {
		'jsonp_callback':'',
		'uid':'null',
		}

	for c in range(upcount):
		query['votes[%d][id]' % c] = song
		query['votes[%d][direction]' % c] = '1'

	for i,id in enumerate(ids):
		query['votes[%d][id]' % (i + upcount)] = id
		query['votes[%d][direction]' % (i + upcount)] = '-1'

	return query

def me_up(song, upcount):
	query = {
		'jsonp_callback':'',
		'uid':'null',
		}

	for c in range(upcount):
		query['votes[%d][id]' % c] = song
		query['votes[%d][direction]' % c] = '1'

	return query
	
		

def vote(query):
	ua = useragents[randint(0,len(useragents)-1)]
	cookie_url = 'http://takeover.ldrhub.com/?key=wsun'
	url = 'http://wsun.s.takeover.ldrhub.com/api/takeover_register_vote/wsun/?' 

	url += urllib.urlencode(query)
	cookie = get_cookie(cookie_url, ua)
	
	request = urllib2.Request(url, None, ua)
	request.add_header('cookie',cookie)
	response = urllib2.urlopen(request)
	
	result = response.read()
	print result, cookie.split(';')[0]


def vote_up(song, duration, them_down=True):
	try:
		for i in range(duration):
			if them_down: 
				vote(me_up_them_down(song, 5))
			else:
				vote(me_up(song, 25))

	except KeyboardInterrupt:
		pass


if __name__ == '__main__':
	import sys
	song = int(sys.argv[1])
	try:
		duration = int(sys.argv[2])
	except:
		duration = 100

	vote_up(song, duration, them_down=True)
	vote_up(song, duration, them_down=False)


