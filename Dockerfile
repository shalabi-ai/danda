FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /workspace

# Create a non-root user
RUN useradd --create-home --uid 1001 appuser

RUN apt-get update && \
    apt-get install -y --no-install-recommends git git-lfs && \
    git lfs install && \
    python -m pip install --upgrade pip setuptools wheel && \
    pip install \
        pandas \
        seaborn \
        numpy \
        pytest \
        pytest-cov \
        ruff \
        mypy \
        twine \
        build && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
USER appuser

CMD ["bash"]