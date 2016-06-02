import json
from datetime import date
from datetime import datetime
from pytz import timezone
import pytz
import operator
import sys

## This is a MoodParser for Moodtrack Diary JSON data ##
## sys.argv[1] contains the date to start from
## currently the date to end with is the last entry's date and time.

dateStr = str(date.today().strftime('%m_%d_%Y'))
data = []

#first open json file that contains the entries data pulled from the site and load into dict
with open("mood_app_dump_" + dateStr + ".json") as json_file:
	data = json.load(json_file)

#loop through dict and pull out just the rating_value, the description, the posted_at timestamp (which is 5 hours ahead of CST: UTC time), and the mood_name
filteredEntries = {}
skipCount = 0
for entry in data:
	date = entry['posted_at']
	theirRating = entry['rating_value']
	mood = entry['mood_name']
	description = entry['description']

	#current mode of entry depends on the description containing only an int, otherwise skip the entry
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

#my timezone is CST, hardcoded currently
local_timezone = timezone('America/Chicago')
utc = pytz.utc
moods = {}
weekMoods = {}
weekNums = {}

last_date = datetime.strptime(sys.argv[1],'%m-%d-%Y').replace(tzinfo=local_timezone)
print(last_date)

#create a file just for the week (or time period since the start date passed in)
weekFile = open("week_entries_" + dateStr + ".dsv", 'w')

#create a file for all filtered entry data, tab-delimited
#additionally counts the moods and the ratings (not the star rating, but the number pulled from the description)
#converts the time to CST from UTC
#writes to the all file everytime and if the entry's date is after the start date then writes to the weekFile as well.
with open("compiled_data_" + dateStr + ".dsv", 'w') as outFile:
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

		if(local_time > last_date):
			if(mood in weekMoods.keys()):
				weekMoods[mood] += 1
			else:
				weekMoods[mood] = 1
			if(numRating in weekNums.keys()):
				weekNums[numRating] += 1
			else:
				weekNums[numRating] = 1
			weekFile.write(fixedDate + '\t' + str(numRating) + '\t' + mood + '\n')
weekFile.close()

#just for funsies, print out the total number of each description number
for index, num in enumerate(numPerRating):
	print(str(index) + ' given ' + str(num) + ' times.\n')

#print out the count for each mood specified
sorted_moods = sorted(moods.items(), key=operator.itemgetter(1))
for i, (a,b) in enumerate(sorted_moods):
	print("Mood of " + a + ' was given ' + str(b) + ' times.')

#counts for mood and rating from last_date to last entry date.
for mood, numTimes in weekMoods.items():
	print(mood + '\t' + str(numTimes))

for rating, numTimes in weekNums.items():
	print(str(rating) + '\t' + str(numTimes))
