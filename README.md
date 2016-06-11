**MoodParser**

This is a tool to parse a file of JSON that is pulled from Moodtrack Diary, since it doesn't provide exports.
It then creates a .dsv file (tab delimited) of the creation timestamp, the mood, the star rating, 
and the number I put in the description. 

You need to first get the URL of your diary, which you can get from sharing your diary to an email. You also need to 
find your AUTH token, which as far as I know is only found by going to the URL, using Dev Tools or Firebug to view the 
Network requests, and from the entries request (the 2nd one), one of the request parameters is your AUTH token. You 
need to put both the URL and the AUTH token into the moodparser.properties file, for which I have provided the 
template for you to fill in with your info. Just remove the _template part of the filename and you'll be good to go, 
provided that the properties file is in the same directory as your script.

Command to run: 
python moodparser.py *start_date* *end_date*

*start_date* and *end_date* are both in the format of MM-DD-YYY

**Latest addition**
Have modified the date filtering, where it now pulls the start and end dates from the commandline as the first and 
second arguments respectively in the format of (MM-DD-YYYY). The script also now requests the entries directly from 
the API Moodtrack Diary currently uses. You just need to provide your URL and AUTH token as described above into the 
new properties file, which I committed as a template.  

**Note**: This tool is definitely still in progress as right now I'm running the script to generate multiple tab 
delimited files and then pulling data from them into Excel sheets to make graphs.

**Goal of project** 
My hope is to get this tool to the point where it has a GUI of some sort and hopefully less setup work with the 
properties file for fetching.


