FROM python
WORKDIR /home/MyApp
COPY . .
EXPOSE 8888

RUN pip install -r -U requrements.txt

CMD [ "uvicorn", "main:app","--reload" ]
