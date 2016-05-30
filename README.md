*MoodParser*

This is a tool to parse a file of JSON that is pulled from Moodtrack Diary, since it doesn't provide exports.
It then creates a .dsv file (tab delimited) of the creation timestamp, the mood, the star rating, 
and the number I put in the description. 

*Latest addition*
Have added a *hardcoded* date filtering, where it separately creates a file containing data from the specified
date until the most recent entry. 

*Note*: This tool is definitely still in progress as right now I'm manually pulling the data from the Moodtrack Diary 
website, saving it to a file, then running the script to generate multiple tab delimited files, and finally, pulling 
data from them into Excel sheets to make graphs. Not to mention that currently most of the filenames and any date information
is hardcoded. I'm working on that as well.

*Goal of project* 
My hope is to get this tool to the point where all of this is automated and with a GUI of some sort. 
