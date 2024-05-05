FROM python:3.12

RUN mkdir /application

WORKDIR "/application"

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED 1
ENTRYPOINT ["tail", "-f", "/dev/null"]


