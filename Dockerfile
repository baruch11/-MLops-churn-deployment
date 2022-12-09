FROM python:3.8-slim

WORKDIR /usr/app/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "chaos.application.server:app","--host","0.0.0.0","--port","8000"]