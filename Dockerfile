################################################
#                This Dockerfil                #
################################################

# 指定基础镜像
#   FROM <image>
#   FROM <image>:<tag>
FROM python:3.8

# 指定工作目录
#   WORKDIR <path>
WORKDIR /projects

# 添加本地文件（相对路径或网络资源）到容器
#   ADD <src> <dest>

# 复制本地文件（相对路径）到容器
#   COPY <src> <dest>
COPY ./ FlaskAPIProjectTemplate/

# 指定工作目录
#   WORKDIR <path>
WORKDIR /projects/FlaskAPIProjectTemplate

# 执行指令
#   RUN <command>
RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "gunicorn", "-c", "gunicorn.conf.py", "run:app" ]