FROM python:3
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod +x run_tests.sh
RUN ln -s /app/run_tests.sh /usr/bin
EXPOSE 80
ENV PATH=$PATH:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]