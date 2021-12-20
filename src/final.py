import os
import urllib.request
import json
import sys
import csv
import requests
import pandas as pd
import config
from datetime import date


def get_leaderboard_data(offset=0, limit=500):
    headers = {'User-Agent': 'PostmanRuntime/7.26.2'}
    url = config.hackerrankInfo["url"] + "?offset=" + str(offset) + "&limit=" + str(limit)

    request = urllib.request.Request(url, headers=headers)

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        # ...
        print('HTTPError: {}'.format(e.code))
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        # ...
        print('URLError: {}'.format(e.reason))
    else:
        # 200
        # ...
        print('Connection Established')
        contestsr = response.read()

    leaderboard_dict = json.loads(contestsr)
    return leaderboard_dict


def write_data(data_dict):
    with open("temp-leaderboard-data.csv", 'a', newline='') as lbf:
        fieldnames = ['username','score']
        writer = csv.DictWriter(lbf, fieldnames=fieldnames)
        # writer.writeheader()
        for lb_entry in data_dict['models']:
            writer.writerow({
                'username': lb_entry['hacker'],
                'score': lb_entry['score']
            })

def merge_file(tempFile, finalFile):
    # reading csv files
    if os.path.isfile(finalFile):
        final = pd.read_csv(finalFile)
        final = final[(final["username"] != "[deleted]")]
        temp = pd.read_csv(tempFile)
        temp = temp[(temp["username"] != "[deleted]")]

        # using merge function by setting how='left'
        output2 = pd.merge(final, temp, 
                        on='username', 
                        how='outer')

        #output2 = final.set_index('username').combine_first(temp.set_index('username')).reset_index()
        output2.sort_values(by=['username']).to_csv(finalFile, header=True, index=False)
    else:
        final = pd.read_csv(tempFile)
        final = final[(final["username"] != "[deleted]")]

        final.to_csv(finalFile, header=True, index=False)


    
    
    

def process_data(leaderboard_dict):
    pass


def sendSlackMessage(message,slackConfig,headerText):
    url = slackConfig["url"]
    #message = '1' + '\t\t\t' + 'SS' + '\t\t\t\t' + '150' + '\n'
    #message += '2' + '\t\t\t' + 'Soumen' + '\t\t\t\t' + '100' + '\n'
    title = f"New Incoming Message :zap:"
    slack_data = {
        #"username": config.slackInfo["username"],
        #"icon_emoji": ":robot_face:",
        "attachments": [
		{
			"blocks": [
				{
					"type": "header",
					"text": {
						"type": "plain_text",
						"text": ":point_right: " + headerText + ":clap: :point_left:"
					}
				},
				{
					"type": "divider"
				},
                {
					"type": "context",
					"elements": [
						{
							"type": "mrkdwn",
							"text": "Date: " + date.today().strftime("%d/%m/%Y")
						}
					]
				},
				{
					"type": "context",
					"elements": [
						{
							"type": "mrkdwn",
							"text": message
						}
					]
				},
				{
					"type": "divider"
				},
				{
					"type": "context",
					"elements": [
						{
							"type": "mrkdwn",
							"text": "*_Programming is a skill best acquired by practice and example rather than from books. Keep Coding._*"
						}
					]
				}
			]
		}
	]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)


def createMessage(leaderboard_dict,message):
    for lb_entry in leaderboard_dict['models']:
        message += str(lb_entry['rank']) + "\t\t\t" + lb_entry['hacker'] + "\t\t\t\t" + str(lb_entry['score']) + "\n"
    return message

if __name__ == "__main__":
    inp = input("""\nWelcome to Wissen Coding Challenge Console \n
    1. SEND DAILY LEADERBOARD\n
    2. SEND NEWS UPDATE\n
    3. EXPORT LEADERBOARD\n
    0. EXIT\n
    Enter your command: """)
    print("Entered:" + inp)
    # leaderboard_dict = get_leaderboard_data()
    # process_data(leaderboard_dict)
    if inp == "1":

        header = "*Rank*\t\t\t*Name*\t\t\t\t*Score*\n"
        message = header

        offset=0
        limit=100

        while offset < 300:
            print("Offset:"+str(offset))
            leaderboard100 = get_leaderboard_data(offset,limit)
            message = createMessage(leaderboard100,message)
            offset=offset+100
        
        #leaderboard_top25 = get_leaderboard_data(0,25)
        #message = createMessage(leaderboard_top25,message)
        print(message)
        
        msginp = input("\nWhich slack channel you want to send?\n1. code-challenge\n2. general\n\n")
        headerText = "Wissen Coding Challenge Season 3 Leaderboard"
        if msginp == "1":          
            sendSlackMessage(message,config.slackInfoCC,headerText)
        elif msginp == "2":
            sendSlackMessage(message,config.slackInfoGen,headerText)
        
        print("Message Sent")
    elif inp == "2":
        message = """Hey Coders,

        New Problems have just been added to the challenge. Happy Coding :technologist:\n"""

#        message = """Hey Coders,
        
#        We have noticed that few participants have being changing their usernames. This will lead to data and progress loss. It's mandatory that participant has to have a single username. Please avoid changing your usernames else your progress will not be captured.

#        Defaulter Users:
#            shashank_gupta8 -> shashank0106
#            sushant_saurav1 -> saurav_sushant
        
 #       Thanks
 #       """

        msginp = input("\nWhich slack channel you want to send?\n1. code-challenge\n2. general\n\n")
        headerText = "Important Announcement"
        #headerText = "Comparator Bot Report"
        if msginp == "1":
            sendSlackMessage(message,config.slackInfoCC,headerText)
        elif msginp == "2":
            sendSlackMessage(message,config.slackInfoGen,headerText)

        print("Message Sent")
    elif inp == "3":
        print("Exporting Started")

        if os.path.isfile("temp-leaderboard-data.csv"):
            os.remove("temp-leaderboard-data.csv")

        offset=0
        limit=100

        while offset < 300:
            print("Offset:"+str(offset))
            leaderboard100 = get_leaderboard_data(offset,limit)
            write_data(leaderboard100)
            offset=offset+100
        
        headerList = ['username', date.today().strftime("%d-%m-%Y")]
        file = pd.read_csv("temp-leaderboard-data.csv",header=None)
        print(file.values)
        file.to_csv("temp-leaderboard-data.csv", header=headerList, index=False)

        print("Initiating Leaderboard Data Merging")
        merge_file("temp-leaderboard-data.csv","leaderboard-data.csv")
        print("Data Merging Completed")

    elif inp == "0":
        print("Exiting")
        exit

