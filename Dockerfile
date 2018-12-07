FROM python:latest
WORKDIR /usr/src/app
ENV PATH="/usr/src/app:${PATH}"
COPY requirements.txt ./
VOLUME ["/usr/src/app"]
RUN pip install --no-cache-dir -r  requirements.txt
