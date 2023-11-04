# syntax=docker/dockerfile:1

FROM python:3.10.13-slim-bullseye

WORKDIR /final_project

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--port=3000", "--host=0.0.0.0" ]

EXPOSE 3000