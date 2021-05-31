FROM nikolaik/python-nodejs:python3.9-nodejs16-slim	

ENV NODE_ENV=production

RUN apt  update -y && apt  upgrade -y && apt install -y git cron

RUN mkdir -p /home/node/app/node_modules &&  useradd -s /bin/bash  node  && usermod -aG node node && chown -R node:node /home/node/

USER node

WORKDIR /home/node/app

RUN git clone https://github.com/vaddisrinivas/WebSheets.git && cd WebSheets;pip3 install -r requirements.txt; npm install lowdefy@latest npx; chmod 777 base-cron 

ENTRYPOINT  cd WebSheets; ls -lart;mkdir output; python3 WebSheetsGen.py;bash base-cron & cd output/; npx lowdefy@latest dev
