FROM python:3-slim

LABEL maintainer="d-Rickyy-b <blackjack@rico-j.de>"
LABEL site="https://github.com/d-Rickyy-b/Python-BlackJackBot"

RUN mkdir -p /blackjackbot/logs
COPY . /blackjackbot
WORKDIR /blackjackbot
RUN pip install --no-cache-dir -r /blackjackbot/requirements.txt

CMD ["python", "/blackjackbot/bot.py"]
