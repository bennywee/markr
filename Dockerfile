FROM python:3.10.11
COPY requirements.txt .
RUN  pip install -r requirements.txt 
RUN rm requirements.txt 
WORKDIR /markr
ENTRYPOINT [ "/bin/bash" ]
