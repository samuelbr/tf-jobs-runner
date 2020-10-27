FROM tensorflow/tensorflow

ADD run.py /
RUN chmod a+x /run.py

ENTRYPOINT /usr/bin/python3.6
