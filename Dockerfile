# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
FROM python:3.14-slim@sha256:cd89c30eda26ee911a4611b18680086e0ea42e6f5f8cbe653d07fa7958c9cec8 AS build
RUN python -m pip install --no-cache-dir uv==0.13.1
WORKDIR /build
COPY pyproject.toml uv.lock README.md LICENSE NOTICE ./
COPY src ./src
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
RUN uv sync --locked --extra all --no-editable

FROM python:3.14-slim@sha256:cd89c30eda26ee911a4611b18680086e0ea42e6f5f8cbe653d07fa7958c9cec8
LABEL org.opencontainers.image.title="OneKit" \
      org.opencontainers.image.source="https://github.com/mattiapiazzalunga/onekit" \
      org.opencontainers.image.licenses="LicenseRef-PolyForm-Shield-1.0.0" \
      org.opencontainers.image.authors="Mattia Piazzalunga <hello@mattiapiazzalunga.com>"
COPY --from=build /opt/venv /opt/venv
COPY LICENSE NOTICE /usr/share/doc/onekit/
ENV PATH="/opt/venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1
WORKDIR /files
USER 65532:65532
ENTRYPOINT ["onekit"]
CMD ["--help"]
