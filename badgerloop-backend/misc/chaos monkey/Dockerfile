FROM python:2-alpine

ADD chaos-monkey-config.yml chaos-monkey-config.yml
ADD requirements.txt requirements.txt
ADD docker-chaos-monkey.py docker-chaos-monkey.py

RUN pip install -r requirements.txt

CMD [ "python", "docker-chaos-monkey.py" ]