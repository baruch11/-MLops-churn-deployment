FROM python:3.9-slim

COPY . /usr/app/
WORKDIR /usr/app/

# install git/ssh
RUN apt-get update
RUN apt-get install -y ssh
RUN apt-get install -y git

# add credentials on build
ARG SSH_CHURN_ACCESS
RUN mkdir ~/.ssh 
RUN echo "$SSH_CHURN_ACCESS" > ~/.ssh/id_ed25519 && chmod 600 ~/.ssh/id_ed25519

# check if domain is accepted
RUN touch ~/.ssh/known_hosts 
RUN ssh-keyscan gitlab.com >> ~/.ssh/known_hosts


COPY pyproject.toml .
COPY poetry.lock .
RUN pip install poetry
RUN poetry install


EXPOSE 8000

CMD ["uvicorn", "chaos.application.server:app","--host","0.0.0.0","--port","8000"]