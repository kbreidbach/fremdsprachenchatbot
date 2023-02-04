# Chatbot "Québec" by Group 5 of Cognitive Science Seminar "Schreiben im Fremdsprachenunterricht Französisch und Spanisch"

Universität Osnabrück, Wintersemester 2022/2023

## Installation

The framework uses Python >= 3.8 and Django.
All other relevant libraries are specified in requirements.txt.


## Licence

The Code is distributed under a GPL V3 licence.

It contains code from others:
- the french lexicon in the data folder is also taken from https://elizia.net/cerveau/ (GPL V3) --> however, this is not used in the current version of the chatbot

## Use-Case of Chatbot

The chatbot is aimed at students in grade 9 who have been learning French for three/four years.
The scenario is that the German student gets to know their Québecian exchange partner and together they try to find shared interests/activities that they will do during the week of exchange in Québec.
At the end of the conversation a schedule for that week can be obtained. Ideally, the students should try to first scan the conversation again and create their own schedule to practice their language understanding. The printed schedule by the chatbot can then be used for self-checking.
Because the chatbot is designed for juvenile students, a detector for common cursewords is implemented. Upon cursing the students are reminded to stay friendly and asked to answer the previous question asked.
Once the conversation is over the green icon will turn red and the chatbot's status will read "Québec is offline". If the student continues to write a message will tell them to restart the chat in order to start a new conversation.

## Architecture of Chatbot

The chatbot uses states to navigate through the conversation.
For NLU regexes or spacy are used.

## Chatbot Identity

The chatbot is assigned a random identity upon starting the chatsession. This identity is comprised of a name, gender and certain preferences and dislikes (activity-wise).
The preferences are relevant since the chatbot suggests activities on several occasions. The dislikes become relevant in one particular state where the student is asked to suggest an activity. If their suggestion is one of the dislikes of the chatbot, the bot will decline the student's proposal and suggest another activity. 
