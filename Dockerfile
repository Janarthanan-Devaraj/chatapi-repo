FROM python:3.11.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /chatapi

WORKDIR /chatapi

COPY . /chatapi/

RUN pip install --upgrade pip && \
    pip install pip-tools

RUN pip install \
    asgiref==3.6.0 \
    boto==2.49.0 \
    boto3==1.26.104 \
    botocore==1.29.104 \
    build==0.10.0 \
    certifi==2022.12.7 \
    charset-normalizer==3.1.0 \
    click==8.1.3 \
    colorama==0.4.6 \
    Django==4.1.7 \
    django-cors-headers==3.14.0 \
    django-rest-swagger==2.2.0 \
    django-storages==1.13.2 \
    djangorestframework==3.14.0 \
    djangorestframework-simplejwt==5.2.2 \
    drf-yasg==1.21.5 \
    idna==3.4 \
    inflection==0.5.1 \
    install==1.3.5 \
    itypes==1.2.0 \
    Jinja2==3.1.2 \
    jmespath==1.0.1 \
    MarkupSafe==2.1.2 \
    openapi-codec==1.3.2 \
    packaging==23.0 \
    Pillow==9.5.0 \
    PyJWT==2.6.0 \
    pyproject_hooks==1.0.0 \
    python-dateutil==2.8.2 \
    python-decouple==3.8 \
    pytz==2023.3 \
    requests==2.28.2 \
    ruamel.yaml==0.17.21 \
    s3transfer==0.6.0 \
    simplejson==3.18.4 \
    six==1.16.0 \
    sqlparse==0.4.3 \
    tzdata==2023.3 \
    uritemplate==4.1.1 \
    urllib3==1.26.15\
    coreapi==2.3.3 \
    coreschema==0.0.4 \
