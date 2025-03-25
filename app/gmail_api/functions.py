from googleapiclient.discovery import build


def gmail_read_messages(creds: str = None):
    try:
        service = build("gmail", "v1", credentials=creds)
        results = (
            service.users()
            .messages()
            .list(userId="me", labelIds=["INBOX"], q="is:unread")
            .execute()
        )
        messages = results.get("messages", [])
        if not messages:
            return None
        return messages
    except Exception as e:
        print(f"Error occured:{e}")


def gmail_get_formatted_messages(creds: str = None, format="minimal"):
    try:
        service = build("gmail", "v1", credentials=creds)
        results = (
            service.users()
            .messages()
            .list(userId="me", labelIds=["INBOX"], q="is:unread",maxResults=2)
            .execute()
        )
        thread_ids = results.get("messages", [])
        # TODO need to go for loop and see by thread ID how to get message body
        for message in thread_ids:
            message_id = message["id"]
            message_metadata = (
                service.users()
                .messages()
                .get(userId="me", id=message_id, format=format)
                .execute()
            )
           

    except Exception as e:
        print(f"Error occured: {e}")
