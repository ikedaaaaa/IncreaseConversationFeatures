FROM --platform=linux/amd64 python:3.8

WORKDIR /app

# librosaを使用するのために必要なffmpegをインストール
RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc libsndfile1
RUN apt-get install -y ffmpeg

# requirements.txtをコピーしてpythonの必要なライブラリをインストール
COPY requirements.txt /app

RUN pip install --upgrade pip && pip install -r ./requirements.txt
RUN pip install --upgrade setuptools