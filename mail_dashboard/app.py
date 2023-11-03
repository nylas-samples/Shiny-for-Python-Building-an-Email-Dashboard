# Import your dependencies
from dotenv import load_dotenv
from shiny import App, render, ui
from shiny.types import ImgData
import pandas as pd
from nylas import Client
import os
import seaborn as sns
from wordcloud import WordCloud
from nylas.models.messages import ListMessagesQueryParams

# Load your env variables
load_dotenv()

# Initialize your Nylas API client
nylas = Client(
    api_key = os.environ.get("V3_API_KEY")
)

# Auxiliar variables
from_messages = []
to_messages = []
text = ""

# Create query parameters
f_query_params = ListMessagesQueryParams(
	{'in' : "inbox",
	'limit': 100}
)

# Create query parameters
t_query_params = ListMessagesQueryParams(
	{'in' : "sent",
	'limit': 100}
)

# Get emails from your inbox folder
f_messages, _, _ = nylas.messages.list(os.environ.get("GRANT_ID"), f_query_params)
# Get emails from your sent folder
t_messages, _, _ = nylas.messages.list(os.environ.get("GRANT_ID"), t_query_params)

# Loop through your inbox emails
for msg in f_messages:
	# Get the name of the person emailing you
	if(msg.from_[0].email != ""):
		from_messages.append(msg.from_[0].email.split()[0])
	# Concatate the subjects of all emails
	text = text + " " + msg.subject
# Turn the array into a data frame	
f_df = pd.DataFrame(from_messages, columns=['Names'])
# Aggregate values, get the top 3 and a name to the new column
top_3_from = f_df["Names"].value_counts().head(5).reset_index(name="count")
top_3_from.columns = ['person', 'count']

# Loop through your sent emails
for msg in t_messages:
	# Get the name of the person you're emailing	
	if(msg.to[0].email != ""):	
		to_messages.append(msg.to[0].email.split()[0])
# Turn the array into a data frame		
t_df = pd.DataFrame(to_messages, columns=['Names'])
# Aggregate values, get the top 3 and a name to the new column
top_3_to = t_df["Names"].value_counts().head(3).reset_index(name="count")
top_3_to.columns = ['person', 'count']

# Using all the email subjects, generate a wordcloud
wordcloud = WordCloud(width=800, height=300).generate(text)
# Download the wordcloud image
wordcloud.to_file("mail_dashboard_v3/wc_email.png")

# Create the dashboard layout
app_ui = ui.page_fluid(
    ui.tags.style(
        """
        .app-col {
            border: 1px solid black;
            border-radius: 5px;
            background-color: #eee;
            padding: 8px;
            margin-top: 5px;
            margin-bottom: 5px;
        }
        """
    ),
    ui.h2({"style": "text-align: center;"}, "Email Dashboard"),
    ui.row(
        ui.column(
            6,
            ui.div(
                {"class": "app-col"},
               ui.h2({"style": "text-align: center;"},"From: Emails"),
               ui.output_plot("_from_"),
            ),
        ),
        ui.column(
            6,
            ui.div(
                {"class": "app-col"},
                ui.h2({"style": "text-align: center;"},"To: Emails"),
                ui.output_plot("_to_"),
            ),
        ),
    ),
    ui.row(
        ui.column(
            12,
            ui.div(
                {"class": "app-col"},
                ui.h2({"style": "text-align: center;"},"Email Subject's Wordcloud"),
				ui.output_image("image"),
            ),
        )
    ),    	
)

def server(input, output, session):
# Display the "From" emails	
	@output
	@render.plot
	def _from_():
		g = sns.catplot(data=top_3_from,x="person",y="count",hue="person",kind="bar")
		return g
		
# Display the "To" emails
	@output
	@render.plot
	def _to_():
		h = sns.catplot(data=top_3_to,x="person",y="count",hue="person",kind="bar")
		return h		
		
# Display the Wordcloud	
	@output
	@render.image
	def image():
		from pathlib import Path
		dir = Path(__file__).resolve().parent
		img: ImgData = {"src": str(dir / "wc_email.png"),
                                   "width": "800px", "height":"300px"}
		return img

# Start the server
app = App(app_ui, server, debug=True)
