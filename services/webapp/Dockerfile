# syntax=docker/dockerfile:1

ARG PYTHON_VERSION


# ==============================================
# ~~~~~~~~ Stage 0: Task ~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


FROM golang:bullseye@sha256:a0b51fe882f269828b63e7f69e6925f85afc548cf7cf967ecbfbcce6afe6f235 AS build-task
ENV GOBIN=/app/bin
WORKDIR /app
RUN go install github.com/go-task/task/v3/cmd/task@latest


# ==============================================
# ~~~~~~~~ Stage 1: webapp ~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


FROM --platform=linux/amd64 python:${PYTHON_VERSION}-slim
LABEL description="M-PT1-63-23"
LABEL org.opencontainers.image.authors="Alexander Sidorov <a375296648709@gmail.com>"

ARG VERSION
LABEL version=${VERSION}


# ~~~~~~~~ System packages ~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RUN apt update \
    && apt install --no-install-recommends --yes \
    bash \
    curl \
    g++ \
    libffi-dev \
    libpq-dev \
    netcat \
    python3-dev


# ~~~~~~~~ Poetry & Python dependencies ~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ARG PIP_VERSION
RUN pip install "pip==${PIP_VERSION}"

ARG POETRY_VERSION
RUN pip install "poetry==${POETRY_VERSION}"

COPY --from=build-task /app/bin/task /usr/bin/task


# ~~~~~~~~ User & App directories ~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ARG GROUP_ID=9999
ARG USER_ID=9999
ARG USERNAME=m-pt1-63-23

ARG DIR_APP="/app"
ARG DIR_CACHE="/var/cache/app"

RUN addgroup --system --gid ${GROUP_ID} ${USERNAME} \
    && useradd \
        --create-home \
        --no-log-init \
        --system \
        --home-dir="/home/${USERNAME}" \
        --gid=${GROUP_ID} \
        --uid=${USER_ID} \
        ${USERNAME} \
    && install --owner ${USERNAME} --group ${USERNAME} --directory "${DIR_APP}" \
    && install --owner ${USERNAME} --group ${USERNAME} --directory "${DIR_CACHE}"

WORKDIR "${DIR_APP}"

USER ${USERNAME}


# ~~~~~~~~ Virtualenv ~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

COPY ./pyproject.toml ./poetry.lock ./

ENV POETRY_VIRTUALENVS_ALWAYS_COPY=false
ENV POETRY_VIRTUALENVS_CREATE=true
ENV POETRY_VIRTUALENVS_IN_PROJECT=false
ENV POETRY_VIRTUALENVS_PATH="${DIR_CACHE}"

RUN poetry env use "${PYTHON_VERSION}" \
    && poetry env info > "${DIR_CACHE}/.poetry-env-info.txt"
RUN if echo "${VERSION}" | grep -Pq '^\d{4}-\d{2}-\d{2}$' ; then poetry install --without dev; else poetry install --with dev; fi

COPY . .

ENV ENVIRONMENT=docker-build
ENV SECRET_KEY=1
RUN task static

# ~~~~~~~~ Health check ~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HEALTHCHECK \
    --interval=15s \
    --retries=6 \
    --start-period=6s \
    --timeout=6s \
    CMD curl -f "http://localhost:80/livez" || exit 1
