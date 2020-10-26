FROM tensorflow/tensorflow

ADD run.py /

ENTRYPOINT /run.py
