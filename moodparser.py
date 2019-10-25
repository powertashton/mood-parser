import json
from datetime import date
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import operator
import sys
import requests

## This is a MoodParser for Moodtrack Diary JSON data ##
## sys.argv[1] contains the date to start from and sys.argv[2] the last date to include.
## If not specified, the end date will be today's date.

props = {}

def storeProps(propFile):
	with open(propFile) as f:
		for line in f:
			if '=' in line:
				# Find the name and value by splitting the string
				name, value = line.split("=", 1)
				# Assign key value pair to dict
				# strip() removes white space from the ends of strings
				props[name.strip()] = value.strip()
	print(props)

def getToken():
	URL = props["REFERER_URL"]
	endPart = URL.split("com/",1)[1]
	payload = {"code": props["keyCode"]}
	headers = {"Referer": URL, "Origin": "http://e.moodtrack.com"}
	r = requests.post((props["REQUEST_URL"]+endPart), headers=headers, params=payload)
	if("token" in r.json().keys()):
		return r.json()["token"]
	else:
		return None

def fetchEntries(token):
	headers = {"Referer": props["REFERER_URL"], "Auth-Token": token} 
	r= requests.get(props["ENTRIES_URL"], headers=headers)
	jsonObj = r.json()
	return jsonObj

def parseEntries(filteredEntries):
	skipCount = 0
	for entry in data:
		date = entry['posted_at']
		theirRating = entry['rating_value']
		mood = entry['mood_name']
		description = entry['description']
			
		try:
			myRating = str(description)
			filteredEntries[date] = {'theirRating': theirRating, 'mood': mood, 'myRating': myRating}
		except ValueError:
			try:
				myRating = str(mood)
				filteredEntries[date] = {'theirRating': theirRating, 'mood': "N/A", 'myRating': myRating}
			except ValueError:
				skipCount += 1
			except TypeError:
				skipCount += 1
		except TypeError:
			try:
				myRating = str(mood)
				filteredEntries[date] = {'theirRating': theirRating, 'mood': "N/A", 'myRating': myRating}
			except ValueError:
				skipCount += 1
			except TypeError:
				skipCount += 1
	return skipCount

def printWeekCounts(items):
	for item, numTimes in items.items():
		print(str(item) + '\t' + str(numTimes))

storeProps("moodparse.properties")

dateStr = str(date.today().strftime('%m_%d_%Y'))
#Hardcoded timezone
local_timezone = timezone('Asia/Hong_Kong')
#TO DO: Soft code timezone
utc = pytz.utc
endDate = date.today()
if(len(sys.argv) == 3):
	endDate = datetime.strptime(sys.argv[2],'%m-%d-%Y').replace(tzinfo=local_timezone)
	print(endDate)

token = getToken()
data = []
if(token != None):
	data = fetchEntries(getToken())
else:
	print("Unable to fetch data due to not finding authentication token.")

#loop through dict and pull out just the rating_value, the description, the posted_at timestamp (which is 5 hours ahead of CST: UTC time), and the mood_name
filteredEntries = {}
numSkipped = parseEntries(filteredEntries)

print("This is the skip count: " + str(numSkipped))
print('This is the number of filtered entries: ' + str(len(filteredEntries)))

#numPerRating = [0,0,0,0,0,0,0,0,0,0,0]
numPerRating = {}
moods = {}
weekMoods = {}
weekNums = {}

startDate = datetime.strptime(sys.argv[1],'%m-%d-%Y').replace(tzinfo=local_timezone)
print(startDate)
#create a file just for the week (or time period since the start date passed in)
weekFile = open("week_entries_" + dateStr + ".csv", 'w')


#create a file for all filtered entry data, comma separated
#additionally counts the moods and the ratings (not the star rating, but the number pulled from the description [or mood, depending on the entry format])
#writes to the all file everytime and if the entry's date is after the start date then writes to the weekFile as well.
with open("compiled_data_" + dateStr + ".csv", 'w') as outFile:
	#first pull each value into a var
	for date, details in filteredEntries.items():
		starRating = details['theirRating']
		numRating = details['myRating']
		numRating = numRating.replace(',', '.') #Replaces commas with periods in description
		numRating = numRating.replace('\n', ' ') #Replaces new lines with a space
		if(numRating not in numPerRating.keys()):
			numPerRating[numRating] = 1
		else:
			numPerRating[numRating] += 1
			
		mood = details['mood']
		mood = mood.replace(',', ' ') #Removes commas from mood labels 
		#TO DO: Less janky comma fixes
		if(mood in moods.keys()):
			moods[mood] += 1
		else:
			moods[mood] = 1
			
		#converts the time to local timezone hardcoded previously from UTC
		utc_time = datetime.strptime(date[:len(date)-1], '%Y-%m-%dT%H:%M:%S')
		local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
		fixedDate = str(local_time.strftime('%m-%d-%Y %H:%M'))
		outFile.write(fixedDate + ', ' + str(starRating) + ', ' + mood + ', ' + str(numRating) + '\n')

		if(local_time.date() >= startDate.date() and local_time.date() <= endDate.date()):
			if(mood in weekMoods.keys()):
				weekMoods[mood] += 1
			else:
				weekMoods[mood] = 1
			if(numRating in weekNums.keys()):
				weekNums[numRating] += 1
			else:
				weekNums[numRating] = 1
			weekFile.write(fixedDate + ', ' + mood + ', ' + str(numRating) + '\n')
			
weekFile.close()

#print out the total counts for each rating number
# for index, num in enumerate(numPerRating):
# 	print(str(index) + ' given ' + str(num) + ' times.\n')

for rating, count in numPerRating.items():
	print(str(rating) + " given " + str(count) + " times.")

#print out the count for each mood specified
sorted_moods = sorted(moods.items(), key=operator.itemgetter(1))
for i, (a,b) in enumerate(sorted_moods):
	print("Mood of " + a + ' was given ' + str(b) + ' times.')

#counts for mood and rating from last_date to last entry date.
printWeekCounts(weekMoods)
printWeekCounts(weekNums)