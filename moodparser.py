import json
from datetime import datetime
from pytz import timezone
import pytz
import operator


## This is a MoodParser for Moodtrack Diary JSON data ##

data = []
#first open json file
with open("mood_app_dump_5_18.json") as json_file:
	data = json.load(json_file)
#load json into a dict
print(len(data))
print(data[0])
#loop through dict and pull out just the rating_value, the description, the posted_at timestamp (which is 5 hours ahead: UTC time), and the mood_name
	#stick these into a dict and stick that into a dict with the timestamp as the key
filteredEntries = {}
skipCount = 0
for entry in data:
	date = entry['posted_at']
	theirRating = entry['rating_value']
	mood = entry['mood_name']
	description = entry['description']
	try:
		myRating = int(description)
		filteredEntries[date] = {'theirRating': theirRating, 'mood': mood, 'myRating': myRating}
	except ValueError:
		skipCount += 1
	except TypeError:
		skipCount += 1

print("This is the skip count: " + str(skipCount))
print('This is the number of filtered entries: ' + str(len(filteredEntries)))

numPerRating = [0,0,0,0,0,0,0,0,0,0,0]

local_timezone = timezone('America/Chicago')
utc = pytz.utc
moods = {}
#then create a file(tab delimited) that will hold the data
with open("compiled_data_5_18.dsv", 'w') as outFile:
	#first pull each value into a var
	for date, details in filteredEntries.items():
		starRating = details['theirRating']
		numRating = details['myRating']
		numPerRating[numRating] += 1
		mood = details['mood']

		if(mood in moods.keys()):
			moods[mood] += 1
		else:
			moods[mood] = 1

		utc_time = datetime.strptime(date[:len(date)-1], '%Y-%m-%dT%H:%M:%S')
		local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
		fixedDate = str(local_time.strftime('%m-%d-%Y %H:%M'))
		outFile.write(fixedDate + '\t' + str(starRating) + '\t' + str(numRating) + '\t' + mood + '\n')
	#if the description tab cannot be parsed to a number, then disregard that line (will eliminate the old entries for now)
		#into a list, 0-10 (size of 11) add 1 to whatever number it is
		#next convert the timestamp into CST timestamp that's more readable (a string basically)
		#write the line like so: timestamp tab rating_value tab description tab mood_name

#print out total number of entries
#just for funsies, print out the total number of each description number
for index, num in enumerate(numPerRating):
	print(str(index) + ' given ' + str(num) + ' times.\n')

sorted_moods = sorted(moods.items(), key=operator.itemgetter(1))
for i, (a,b) in enumerate(sorted_moods):
	print("Mood of " + a + ' was given ' + str(b) + ' times.')
