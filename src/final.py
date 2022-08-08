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
    print("Enter ed:" + inp)
    # leaderboard_dict = get_leaderboard_data()
    # process_data(leaderboard_dict)
    if inp == "1":

        header = "*Rank*\t\t\t*Name*\t\t\t\t*Score*\n"
        message = header

        offset=0
        limit=100

        while offset < 400:
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

    #     message = """Hey Coders,

    # This yearly contest is one of the best learning platform and one of the important and key feature of Wissen Technology. 

    # We know that most of you are not a regular coder and we try to make the whole competition fair for you all so that you guys have a great learning experience through it. That's the reason you might see multiple problems of mixed difficulty level. We want everyone to atleast give a try & apply some logic to solve.
    
    # There are two announcements today:

    # 1. Inactive Participants: These are those participants who had signedup but had not submitted a single submissions. 
    
    # Below are the list of usernames who are falling as INACTIVE. We will be blocking these users from the challenge. In case, your account falls in this list and you don't want it to be blocked, reach out to us before 21st January 2022.

    # abhinku2, AK_hacks, akshay_prakash1, alfiya_khan, amit_thakur1, animesh_bhagwat, ankit13555, anoop_kashyap, anupama_alevoor, arjun_m2, ashish_khaparde, ashley_rodrigues, avinash_gurav, avinash_pandey1, chirag_hariya, dhanesh_ravi, gopalakrishna_k5, goutham_bongale, haripriya_venka2, hemant_singh8, himanshi_singh, ishan_patel1, ishanincubus, jainvinit7777, kalakambam_mahe1, Kapuluri_Rao, kapulurimaruthi1, kirti_shahi, kunal_motiani, malovika_mazumd1, manish_soni3, manojkumar_kuma3, mb_bitmesra, mitesh_rampariya, munish_grover, naveenprakash_s, nikhil_summi, nikunjbhai_vinc1, nilesh1004, nitish_kumar9, osr_aman_sharma, prachi_pandit1, pradnya_parab, pramodpatilaws, prashantha_n, priya781990, puja_khandelwal, rahul_yadav8, rajeev_kumar5, rajeevk, rajitchatterjee1, ramesh56, ramky_bommisetty, ravi_kumar22, ravindra_nalawa2, ravircit, rawatdeepak_dr34, rohansharma99601, rohit_puari, rohit2lohias, rohitg19388, sachinkumar_rath, saikat_paul1, saloni_madlani1, sanjay61919, sanjevi_naidu, sarita_kumari2, satish_neeli, selvakmar_nalas1, shalini_p3, shalinifarkya, shalu_kumari3, shashankgupta104, shivagwl46, shivani_chauhan9, shubham_jain26, shubham_singh27, siddharth_nambi1, siddharth_shar12, snehal_ghadge, sonali_dwivedi, sunny_tare, swapnil_mehta_1, sweta_soni, tejesh_chaudhary, thanushiya_y, vaddadi_pavanku1, vikas_sharma9, vinay_cikarambo1, Vinay0073, vishal_panchidi, yashok42


    # 2. As per our Comparator algorithm, we have come across multiple submissions of few participants which violates the plagiarism clause. We have sent the report to the administrator. They will evaluate this report with the findings and reach out each one of you personally.

    # We hope you are enjoying solving the problems and we wish you that your name doesn''t come in our next Comparator Report.

    # Happy Solving. Happy Coding.

    # Regards,
    # Wissen Coding Challenge Committee
    #     """

        msginp = input("\nWhich slack channel you want to send?\n1. code-challenge\n2. general\n\n")
        headerText = "Wissen Coding Challenge Season 3"
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

