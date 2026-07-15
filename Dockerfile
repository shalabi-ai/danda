FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /workspace

RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install \
    pandas \
    numpy \
    pytest \
    pytest-cov \
    ruff \
    mypy \
    twine \
    build

CMD ["bash"]