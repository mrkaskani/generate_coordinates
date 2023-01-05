FROM python:3.9

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . ./src

CMD python ./src/main.py
