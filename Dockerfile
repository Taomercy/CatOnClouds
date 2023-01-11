FROM taomercy/ubuntu-python:3.10.8-1
COPY . /home/CatOnClouds/
RUN apt-get update
RUN pip install setuptools==33.1.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -r /home/CatOnClouds/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
WORKDIR /home/CatOnClouds/
CMD python manage.py runserver 0.0.0.0:23614
EXPOSE 23614

