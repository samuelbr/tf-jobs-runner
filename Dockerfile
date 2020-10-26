FROM tensorflow/tensorflow

ADD run.py /
RUN chmod a+x /run.py

ENTRYPOINT /run.py
