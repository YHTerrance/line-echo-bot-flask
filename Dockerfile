FROM python:alpine
COPY . /app
WORKDIR /app
RUN ["pip3", "install", "-r", "requirements.txt"]
ENV FLASK_PORT=8080
ENTRYPOINT [ "python3" ]
CMD [ "line_simple_server_echo_bot.py" ]
