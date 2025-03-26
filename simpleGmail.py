from simplegmail import Gmail
import re

gmail = Gmail('secrets/credentials.json')

def cleanMessageHTML(message):
    message = message.replace('</td>', '##SPLIT##')
    message = re.sub(regex, '', message)
    message = message.replace('\n', '')
    return message


messages = gmail.get_unread_inbox()
regex = re.compile('<.*?>')
all_messages_list = []
for message in messages:
    message_html = cleanMessageHTML(message.html)
    message_list = message_html.split('##SPLIT##')
    message_list = [line for line in message_list if line]
    all_messages_list.append(message_list)
    #print(message_list)
    ##print(repr(message_html))

message_dict_list = []
for message in all_messages_list:
    message_dict = {}
    for index, item in enumerate(message):
        if index % 2 == 0:
            if index < len(message) -1:
                message_dict[item] = message[index + 1]
    #print(message_dict)
    message_dict_list.append(message_dict)

    print(message_dict_list)





    # message_html.replace('<body><table>', '')
    # message_html.replace('<tr>', '')
    # message_html.replace('<<td valign="top">', '')

    #print(f'HTML: {message.html}')

    # if message.attachments:
    #     for attm in message.attachments:
    #         print(f'Attachment: {attm.filename}')
    #         attm.save(filepath=f'message{message_count}.csv')

