FROM python:3.10.11 AS base
COPY requirements.txt .
RUN  pip install -r requirements.txt 
RUN rm requirements.txt 
WORKDIR /markr

FROM base AS dev
ENTRYPOINT ["/bin/bash"]

FROM base as app
COPY . .
RUN python db/create_db.py
EXPOSE 5000
CMD ["python", "app/main.py"]