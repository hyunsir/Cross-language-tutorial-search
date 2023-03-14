################################################
#                This Dockerfil                #
################################################

#FROM python:3.8
#COPY ./requirements.txt /
#RUN pip install -i  https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

FROM android_recommend_env_v1.0:latest
WORKDIR /projects
COPY ./ AndroidRecommend/
WORKDIR /projects/AndroidRecommend
EXPOSE 4321
ENTRYPOINT [ "gunicorn", "-c", "gunicorn.conf.py", "-k", "uvicorn.workers.UvicornWorker", "run:fast_app" ]

