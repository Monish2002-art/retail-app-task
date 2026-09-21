FROM python:latest

WORKDIR /app

COPY app/src/requirements.txt .

RUN pip install -r requirements.txt

COPY app/src/ ./src/

EXPOSE 5000

ENV FLASK_APP=src/app.py

HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/').read()" || exit 1

CMD ["python", "src/app.py"]