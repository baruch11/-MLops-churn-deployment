FROM python:3.9-slim
COPY . /usr/app/
WORKDIR /usr/app/


RUN apt-get -yq update && apt-get -yqq install ssh git
RUN mkdir ~/.ssh && ssh-keyscan gitlab.com >> ~/.ssh/known_hosts
RUN pip install poetry
RUN --mount=type=ssh,id=churn_ssh  poetry install


EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "chaos.application.server:app","--host","0.0.0.0","--port","8000"]
