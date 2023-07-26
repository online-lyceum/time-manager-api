FROM python:3.11
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY setup.py ./
COPY ./time_manager ./time_manager
RUN pip3 install .
CMD cd time_api && \
        init_db && \
        alembic -c ./alembic.prod.ini upgrade head && \
        cd /app && \
        gunicorn time_manager.main:app -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80
