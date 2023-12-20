FROM python:3.10-slim as requirements-stage

WORKDIR /tmp
RUN pip install poetry
 
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10-slim

RUN apt-get -yq update && apt-get -yqq install ssh git
RUN mkdir -p ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

COPY --from=requirements-stage /tmp/requirements.txt /usr/app/requirements.txt
RUN --mount=type=ssh,id=churn_ssh\
    pip install --no-cache-dir --upgrade -r /usr/app/requirements.txt

RUN sphinx-build --version
RUN apt -y install make

COPY . /usr/app/


WORKDIR /usr/app/docs
RUN sphinx-apidoc -o . ../chaos/
RUN mkdir -p _build/
RUN make clean html

WORKDIR /usr/app/

EXPOSE 8000
CMD ["uvicorn", "chaos.application.server:app","--host","0.0.0.0","--port","8000"]



