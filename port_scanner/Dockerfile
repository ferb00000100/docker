FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./
#
RUN pip install --no-cache-dir -r requirements.txt
#
COPY . .
ARG AWS_DEFAULT_REGION
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_SESSION_TOKEN

CMD [ "python", "/usr/src/app/main.py" ]