# hackerrank-leaderboard-bot
This code will help perform the below tasks:
-   Send Top25 Hackerrank Leaderboard Daily via Slack Channel
-   Send News Update via Slack Channel
-   Export the Hackerrank Leaderboard

## Pre-Requisites
-   Python3
-   PIP Install the requirements.txt file by running the below command:

        pip install -r requirements.txt
-   Any IDE

## Steps to Run
-   Git Checkout this repository
-   Run the below command:

        python -u src/final.py

    This command will prompt as below:
    
        Welcome to Wissen Coding Challenge Console

            1. SEND TOP25 DAILY LEADERBOARD

            2. SEND NEWS UPDATE

            3. EXPORT LEADERBOARD

            0. EXIT

        Enter your command:

1. It will send Top25 Daiily Leaderboard to the Slack Channel
2. It will send news update to the Slack Channel
3. It will export the leaderboard and merge it with the last generated leaderboard file. Make sure you keep the last generated file from the GDrive to your local.
