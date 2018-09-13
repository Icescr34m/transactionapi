FROM centos:7

ADD requirements.txt app.py test_api.py /

RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm && yum -y update && yum -y install python36u python36u-libs python36u-devel python36u-pip

RUN pip3.6 install -r requirements.txt

CMD ["python3.6", "app.py"]
