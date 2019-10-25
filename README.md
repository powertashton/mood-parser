**MoodParser**

This is a tool to parse a file of JSON that is pulled from Moodtrack Social Diary, since it doesn't provide exports.
It then creates a .csv file (comma separated) of the creation timestamp, the mood, the star rating, and the description. 

You need to first get the URL and code of your diary, which you can get from sharing your diary to an email. You 
need to put both the URL and the code into the moodparser.properties file, for which I have provided the 
template for you to fill in with your info. Just remove the _template part of the filename and you'll be good to go, 
provided that the properties file is in the same directory as your script.

Command to run: 
python moodparser.py *start_date* *end_date*

*start_date* and *end_date* are both in the format of MM-DD-YYYY





