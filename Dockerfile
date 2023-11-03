FROM python:3-alpine3.18

ENV DIR=/srv/docker/textextraction

WORKDIR ${DIR}

COPY . ${DIR}

RUN pip install -r requirements.txt

VOLUME [ "${DIR}" ]

ENTRYPOINT [ "python3" , "src/main.py" ]
