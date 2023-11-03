# Shiny-for-Python-Building-an-Email-Dashboard

This sample will show you to create an email dashboard using Shiny for Python.

You can follow along step-by-step in our blog post ["Shiny for Python: Building an Email Dashboard"](https://www.nylas.com/blog/shiny-for-python-building-an-email-dashboard/).

## Setup

### System dependencies

- Python v3.x

### Gather environment variables

You'll need the following values:

```text
V3_TOKEN =
GRANT_ID =
V3_HOST = 
```

Add the above values to a new `.env` file:

```bash
$ touch .env # Then add your env variables
```

### Install dependencies

```bash
$ pip3 install nylas # Nylas API SDK
$ pip3 install shiny # Shiny for Python
$ pip3 install seaborn # Python data visualization library
$ pip3 install pandas # Data analysis library
$ pip3 install wordcloud # Wordcloud generator
$ pip3 install matplotlib # library for creating static, animated, and interactive visualizations
```

## Usage

Create the application using the following command:

```bash
$ shiny create mail_dashboard
```

And modify the contents of app.py

Run the script using the `shiny run` command:

```bash
$ shiny run --reload mail_dashboard/app.py
```

The dashboard should run on your browser on port 8000.

## Learn more

Visit our [Nylas Python SDK documentation](https://developer.nylas.com/docs/developer-tools/sdk/python-sdk/) to learn more.
