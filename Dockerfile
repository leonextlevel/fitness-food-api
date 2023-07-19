FROM python:3.10-slim-buster

ARG ENVIRONMENT
ARG USER_ID

ENV USERNAME django

ENV WORK_DIR /usr/src/app/
ENV ENVIRONMENT $ENVIRONMENT
ENV REQUIREMENTS_DIR /usr/src/requirements
ENV CMD_DIR /usr/src/commands
ENV PATH=${PATH}:/home/${USERNAME}/.local/bin
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $WORK_DIR

# Instala os pacotes
RUN apt-get update \
     && apt-get -y install cron

# Cria um novo usuário (não root)
RUN groupadd --gid $USER_ID $USERNAME && \
    useradd --uid $USER_ID --gid $USER_ID -m $USERNAME

# Cria os diretórios necessários para o COPY
RUN mkdir -p $REQUIREMENTS_DIR && mkdir -p $CMD_DIR && touch /var/log/cron.log

# Copia os arquivos/diretórios necessários para o container
COPY --chown=$USERNAME ./src/ $WORK_DIR
COPY --chown=$USERNAME ./requirements/${ENVIRONMENT}.txt ${REQUIREMENTS_DIR}/${ENVIRONMENT}.txt
COPY --chown=$USERNAME ./commands/${ENVIRONMENT}.sh ${CMD_DIR}/${ENVIRONMENT}.sh
COPY --chown=$USERNAME ./crontabs /usr/src/cron/crontabs

# Ajusta permissões para usuário novo
RUN chmod gu+rw /var/run && \
    chmod gu+s /usr/sbin/cron && \
    chown $USERNAME /etc/environment && \
    chown $USERNAME /var/log/cron.log

# Define o usuário como o usuário novo
USER $USERNAME

# Instalação de pacotes python
RUN pip install --user -r ${REQUIREMENTS_DIR}/${ENVIRONMENT}.txt

# Dá permissão de execução aos scripts
RUN chmod u+x ${CMD_DIR}/${ENVIRONMENT}.sh

# Define o script default do container
CMD ["sh", "-c", "bash ${CMD_DIR}/${ENVIRONMENT}.sh"]
