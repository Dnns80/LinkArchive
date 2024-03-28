FROM python:3.11.2

RUN apt-get update && apt-get install -y \
    libleptonica-dev \
    tesseract-ocr \
    libtesseract-dev \
    python3-pil \
    tesseract-ocr-eng \
    tesseract-ocr-script-latn

WORKDIR /app

COPY . /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

CMD [ "python", "main.py" ]