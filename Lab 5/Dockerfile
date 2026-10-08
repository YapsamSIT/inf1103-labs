FROM python:3.12-slim

WORKDIR /app
COPY dataM_.py .

ENV INVENTORY_FILE=/data/inventory.json
RUN mkdir -p /data

CMD ["python", "dataM_.py"]