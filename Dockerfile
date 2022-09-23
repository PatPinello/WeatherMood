# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-slim
ADD ./WeatherMood.py ./

COPY requirements.txt .
RUN apt-get update && apt-get install -y python3 python3-pip
RUN python -m pip install -r requirements.txt
RUN pip install requests
RUN pip install googlemaps
WORKDIR /app
COPY ./WeatherMood.py ./

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD python WeatherMood.py