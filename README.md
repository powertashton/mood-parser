**MoodParser**

This is a tool to parse a file of JSON that is pulled from Moodtrack Diary, since it doesn't provide exports.
It then creates a .dsv file (tab delimited) of the creation timestamp, the mood, the star rating, 
and the number I put in the description. 

**Latest addition**
Have modified the date filtering, where it now pulls the start date from the commandline as the first argument in the format of (MM-DD-YYYY).
Also, the current date is now appended automaically to the base filename instead of being hardcoded.
Did some cleanup of the code and added in comments that match the code.

**Note**: This tool is definitely still in progress as right now I'm manually pulling the data from the Moodtrack Diary 
website, saving it to a file, then running the script to generate multiple tab delimited files, and finally, pulling 
data from them into Excel sheets to make graphs.

**Goal of project** 
My hope is to get this tool to the point where all of this is automated and with a GUI of some sort. 


