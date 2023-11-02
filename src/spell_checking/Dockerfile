FROM python:3-alpine3.18

ENV DIR=/srv/docker/textextraction

WORKDIR ${DIR}/src/spell_checking

COPY ${DIR}/requirements.txt .

RUN pip install -r requirements.txt

COPY ${DIR} .

VOLUME [ "${DIR}" ]

ENTRYPOINT [ "python3" , "main.py" ]
