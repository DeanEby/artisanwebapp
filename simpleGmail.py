from simplegmail import Gmail
import re
import mysql.connector
import json

with open('secrets/mysql_credentials.json', 'r') as f:
    mysql_credentials = json.load(f)


mydb = mysql.connector.connect(
    host=mysql_credentials['host'],
    user=mysql_credentials['user'],
    password=mysql_credentials['password'],
    database=mysql_credentials['database']
)

def test_mysql_connection(mycursor):
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        print(x)

gmail = Gmail('secrets/credentials.json')

def cleanMessageHTML(message):
    regex = re.compile('<.*?>')
    message = message.replace('</td>', '##SPLIT##')
    message = message.replace(':', '')
    message = re.sub(regex, '', message)
    message = message.replace('\n', '')
    message = message.replace('\r', ' ')
    return message


def getUnreadMessagesAsDict(gmail):
    messages = gmail.get_unread_inbox()
    all_messages_list = []
    for message in messages:
        message_html = cleanMessageHTML(message.html)
        message_list = message_html.split('##SPLIT##')
        message_list = [line for line in message_list if line]
        all_messages_list.append(message_list)

    message_dict_list = []
    for message in all_messages_list:
        message_dict = {}
        for index, item in enumerate(message):
            if index % 2 == 0:
                if index < len(message) -1:
                    message_dict[item] = message[index + 1]
        message_dict_list.append(message_dict)

        
    return message_dict_list
    
#output = getUnreadMessagesAsDict(gmail)

#print(output)
mycursor = mydb.cursor()
test_mysql_connection(mycursor)


