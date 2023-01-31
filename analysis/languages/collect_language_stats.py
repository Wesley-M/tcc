# Setting the github client

load_dotenv()

PERSONAL_TOKEN = os.getenv('PERSONAL_TOKEN')

g = Github(PERSONAL_TOKEN)

