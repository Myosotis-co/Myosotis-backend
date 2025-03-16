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
        print(messages)
        if not messages:
            print("No new messages.")
    except Exception as e:
        print(f"Error occured:{e}")
