# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /code

COPY requirements.txt /code
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

#COPY . /code

ENTRYPOINT ["python3"]
CMD ["app.py"]
# ENV FLASK_APP=app/__init__.py
# CMD ["flask", "run", "--host", "0.0.0.0", "-p", "80"]

FROM builder as dev-envs

RUN <<EOF
apk update
apk add git bash
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
