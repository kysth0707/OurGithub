FROM python:3.7.8

RUN pip install fastapi
RUN pip install uvicorn[standard]
RUN pip install pymysql
RUN pip install threading
RUN pip install pillow
RUN pip install requests
RUN pip install bs4

RUN mkdir -p /test
WORKDIR /test

ENTRYPOINT ["python", "app.py"]