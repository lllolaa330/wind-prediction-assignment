FROM python:3.12-slim
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.9.1
COPY decoder.py /decoder.py
ENTRYPOINT ["python", "/decoder.py"]
