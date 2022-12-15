FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt requirements.txt
COPY pyproject.toml pyproject.toml
RUN apt-get update \
    && apt-get -y install g++ ffmpeg libsm6 libxext6 swig \
    && pip install numpy cython
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--reload"]