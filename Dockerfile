FROM python:3.9

RUN apt-get update && apt-get install -y sqlite3 && apt-get install -y libsqlite3-dev
RUN apt -y update && apt -y upgrade
RUN apt -y install libopencv-dev

WORKDIR /usr/src/

COPY ./apps /usr/src/apps
COPY ./local.sqlite /usr/src/local.sqlite
COPY ./requirements.txt /usr/src/requirements.txt
COPY ./model.pt /usr/src/model.pt

RUN pip install --upgrade pip

RUN pip install torch==2.3.1+cpu torchvision==0.18.1+cpu torchaudio==2.3.1 -f https://download.pytorch.org/whl/torch_stable.html

RUN pip install -r requirements.txt

ENV FLASK_APP "apps.app:create_app('local')"
ENV IMAGE_URL "/storage/images/"

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
