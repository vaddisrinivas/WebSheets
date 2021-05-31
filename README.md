# WebSheets
A simple Lowdefy based site generator that uses CMS/Google-Sheets as a backend! 

Lowdefy is an amazing Lowcode framework that allows us to write websites with mere YAML!
More about that -> https://lowdefy.com

#### #SayHelloTo #Lowdefy!
# How to run this ?
Via docker -

```sudo docker run -itd -p 2583:3000 --name websheets  --env GOOGLE_SHEETS_URL='YOURDRIVE_SHARING_URL' --env CRON_TIME_SECS=60 websheets:latest```

You can also deploy the same with a `docker-compose up -d` -

```
version: "3.9"
services:
  web:
    image: "imvegeta/websheets:latest"
    environment:
      - GOOGLE_SHEETS_URL="https://drive.google.com/file/d/1MLKjqVdjHrE8H1hH-nmF4Cd0uBW_dnUH/view?usp=sharing"
      - CRON_TIME_SECS=600
    ports:
     - 2583:3000
    restart: always
```

## Upcoming features/ideas 

### Templates

- Lowdefy templates:
  - adding multiple layouts and templates for homescreen and posts
  - "markdown" post template
  - image post template
  - post with image template
  - optional More button for each post 
  - comment options for each post to 
  - thoughts template

- Spreadsheets template - 
  - documenting 
  - customization
  - change detection
  - cron management from python to pull the spreadsheets changes automatically

### Docker/Other
- lighter and much secure docker image
- easing deployment options
- Portainer Template
- Pulling Spreadsheet from nextcloud/s3/minio/local/
- n8n workflow to update website  
## How does this project work?
It takes a google-sheet that is shared publically and generates websites based on that.
However this excel sheet has to follow a very easy to create template that can be found here -> https://drive.google.com/file/d/1MLKjqVdjHrE8H1hH-nmF4Cd0uBW_dnUH/view?usp=sharing

Jinja is used to render this data via the Lowdefy templates bundled here.
