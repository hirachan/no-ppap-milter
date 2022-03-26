FROM python:3.9-buster as builder

WORKDIR /app
ARG GITHUB_TOKEN

RUN pip3 install --upgrade pip
RUN pip3 install poetry

RUN apt update &&\
    apt install -y libmilter-dev
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root



FROM python:3.9-slim-buster as runner

WORKDIR /app

RUN pip3 install --upgrade pip

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/lib/x86_64-linux-gnu/libmilter* /usr/lib/x86_64-linux-gnu/


COPY pyproject.toml poetry.lock /app/
COPY no_ppap_milter /app/no_ppap_milter

RUN pip3 install --no-deps --use-feature=in-tree-build . && rm -rf /app
# RUN poetry install --no-dev && rm -rf /app

ENTRYPOINT [ "/usr/local/bin/no-ppap-milter" ]
