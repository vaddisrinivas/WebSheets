# WebSheets

A simple Lowdefy based site generator that uses CMS/Google-Sheets as a backend! 

![Lowdefy Version](https://img.shields.io/static/v1?label=Lowdefy&message=3.18.0&color=green&style=for-the-badge&logo=npm)
![GitHub commit checks state](https://img.shields.io/github/checks-status/vaddisrinivas/WebSheets/master?style=for-the-badge&logo=github)
![GitHub last commit](https://img.shields.io/github/last-commit/vaddisrinivas/WebSheets?style=for-the-badge)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/vaddisrinivas/WebSheets?style=for-the-badge)
![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/imvegeta/websheets?style=for-the-badge&logo=docker)
![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/imvegeta/websheets?style=for-the-badge&logo=docker)
![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/imvegeta/websheets?style=for-the-badge&logo=docker)
![Docker Pulls](https://img.shields.io/docker/pulls/imvegeta/websheets?style=for-the-badge&logo=docker)

---
### New Features (06/20/2021)
- Added Markdown, MarkdownWithCode, DangerousMarkdown  Blocks support!
- Improved Templates and made them much modular.
- Made Excel-template simpler! 
- bug fixes and improved PyLint
- Roadmap added [here](https://npm.ajetavya.com/projects/websheets/)
- [Demo!](https://srinivas.ajetavya.com/) 
---
# What is Lowdefy?

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
      - GOOGLE_SHEETS_URL="YOUR_DRIVE_URL"
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
  - "other" items for every post(similar to about)
  
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
- "Auto" span for the given fields in social fields

## How does this project work?
It takes a google-sheet that is shared publically and generates websites based on that.
However this excel sheet has to follow a very easy to create template that can be found here -> https://docs.google.com/spreadsheets/d/110-t6737J8Nz9iIFTNRDTJInLzJ8b7QtnN4wxnJO2jk/edit?usp=sharing

Jinja is used to render this data via the Lowdefy templates bundled here.
