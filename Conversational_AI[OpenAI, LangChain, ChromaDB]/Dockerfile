wFROM amd64/python:3
ARG PIP=pip3

RUN ${PIP} install --no-cache-dir --upgrade pip 
COPY requirements.txt /app/requirements.txt
RUN python3 -m pip install  -r /app/requirements.txt

COPY . /app
WORKDIR /app

ENV HOST 0.0.0.0
ENV PORT 8000
EXPOSE 8000
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]