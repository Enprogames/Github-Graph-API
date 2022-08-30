FROM python:3.9
# stop python creating __pycache__ files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
# install all requirements
COPY ./requirements.txt /app/
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
# copy all code
COPY . /app/
# start server
CMD ["uvicorn", "Github-Graph-API.graph_api_server:app", "--host", "fastapi", "--port", "8500"]
