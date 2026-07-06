FROM python:3.13-slim

WORKDIR /app

RUN pip install \
    pandas \
    numpy \
    pytest \
    pytest-cov \
    ruff \
    mypy

CMD ["bash"]