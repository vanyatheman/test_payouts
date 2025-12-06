FROM python:3.11-slim

WORKDIR /app

COPY payouts_project/requirements.txt .
COPY ./docker/docker-start.sh .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY payouts_project .

RUN addgroup --system app && adduser --system --group app
RUN chown -R app:app /app
RUN chmod u+x /app/docker-start.sh
RUN ls -la


# CMD ["gunicorn", "payouts_project.wsgi:application", "--bind", "0:8000", "--reload"]
CMD ["/app/docker-start.sh"]
