from datetime import datetime
import requests, json, config

# post-processing function used to evaluate the mode of the input list
def getMode(inputList):
	# create a dictionary of week numbers and their respective number of occurences
	dictOfCounts = {}
	# list of times each week number has occured
	listOfCounts = []
	# iterating through list of week numbers
	for i in inputList:
		# counter is number of times i occurs in inputList
		counter = inputList.count(i)
		# adds the number of times i appears in inputList to the list of counts
		listOfCounts.append(counter)
		# adds week number to dictionary and assignes counted value to week number
		dictOfCounts[i] = counter
	# takes the maximum value in list and assigns it to the variable maxCount
	maxCount = max(listOfCounts)
	if maxCount == 1:
		print "There is no mode for the dataset"
	else:
		# list of modes for week numbers data set
		modeList = []
		# iterates over each key value pair in the dicOfCounts dictionary
		for key, item in dictOfCounts.iteritems():
			# if the week number's number of occurences is equal to the maximum number of occurences
			if item == maxCount:
				# converts week number to a string and adds week number to mode list
				modeList.append(str(key))
				# prints the mode or mulitple modes if they exist
		print "The modes are:", ' and '.join(modeList)
		return modeList

# get commit history from D3 repo by passing the request module's get function 
# github's api url and basic authentication parameters located in a config
# file to keep my login credentials private
url = "https://api.github.com/repos/d3/d3/commits?page=1&per_page=100"
r = requests.get(url,auth=config.auth)

# convert the response object to json in order to parse through the retrieved
# list of commits
raw = r.json()

# create lists to track commits committed in the year 2017 and the week number
# associated with each commit to assess the week with the highest activity
lastYearsList = []
weeksWithCommits = []

# iterate through every commit object within the created json list
# convert the date string to a datetime object in order to more easily work
# with each commit's date which was returned as a string through github's api.
for commit in raw:
	# Convert date from unicode returned from github to a datetime object using datetime's
	# strptime function by passing strptime the strcture that github returned the date in 
	commitDate = datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
	# Check to see if commit was committed in 2017.
	if commitDate.year == 2017:
		# Adds commit to lastYearsList list
		lastYearsList.append(commit)
		# Identifying the week number associated with each commit using datetime's isocalendar
		# function and adding to a list to be used in post proccessing
		weeksWithCommits.append(commitDate.isocalendar()[1])

# iterate over every page of data that github has to offer by comparing  to see if the next page's url
# equals the last page's url. if it does, we are done. If not, we iterate.
while r.links['next']['url'] != r.links['last']['url']:
	# creates a new response by using the next page's url and same authentication parameters
	r = requests.get(r.links['next']['url'], auth=config.auth) 
	# more json data cleaning
	raw = r.json()

	# iterating through each commit in the json list of commits
	for commit in raw:
		# clean the date string to easily interact with the commit's date
		commitDate = datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
		# check year equals 2017 again
		if commitDate.year == 2017:
			# adds commit object equal to lastYearsList list again
			lastYearsList.append(commit)
			# adds week number to weeksWithCommits list again
			weeksWithCommits.append(commitDate.isocalendar()[1])

# calls the getMode post-processing function in order to assess the weeks with the highest
# commit history on the D3 github repository
getMode(weeksWithCommits)

# creates a text file of the commits to the D3 repository during the year 2017
# that was created as the lastYearsList list
#with open('lastYearsList.txt', 'w') as outfile:
#	json.dump(lastYearsList, outfile)