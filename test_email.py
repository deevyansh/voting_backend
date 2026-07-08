from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("GMAIL_ADDRESS"))
print(os.getenv("GMAIL_APP_PASSWORD"))