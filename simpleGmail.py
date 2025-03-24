from simplegmail import Gmail

gmail = Gmail()

messages = gmail.get_unread_inbox()
message_count = 0
for message in messages:
    message_count += 1
    print(f'Subject: {message.html}')

    print(f'Message Body: {message.plain}')

    if message.attachments:
        for attm in message.attachments:
            print(f'Attachment: {attm.filename}')
            attm.save(filepath=f'message{message_count}.csv')

