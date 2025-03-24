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
