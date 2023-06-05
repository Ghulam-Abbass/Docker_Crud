FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8090

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8090"]
