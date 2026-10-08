FROM python:3.12-slim

WORKDIR /app
COPY inventory_manager.py .

ENV INVENTORY_FILE=/data/inventory.json
RUN mkdir -p /data

CMD ["python", "inventory_manager.py"]