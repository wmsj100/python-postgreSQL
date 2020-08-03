FROM centos:7
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV TZ=Asia/Shanghai 
ENV LD_LIBRARY_PATH=/opt/instantclient_12_2

COPY ./docker /docker

WORKDIR /docker

RUN rm -rf /etc/yum.repos.d/* \
	&& mv CentOS-Base.repo epel-7.repo /etc/yum.repos.d/ \
	&& yum clean all \
	&& yum makecache \
	&& yum install -y unzip libaio python3-devel python3-pip libpqxx-devel gcc \
	&& unzip instantclient-basiclite-linux.x64-12.2.0.1.0.zip -d /opt \
	&& mv vimrc /root/.vimrc \
	&& rm -rf /docker \
	&& yum clean all

COPY ./docker/pip.conf /root/.pip/pip.conf

WORKDIR /webapp

RUN python3 -m pip install -U pip \
	&& pip3 install psycopg2 cx_oracle 

COPY webapp webapp
