FROM fluent/fluentd:v1.7-debian-1

USER root

WORKDIR /home/
ENV PATH /home/.gem/ruby/2.2.0/bin:$PATH
RUN apt-get update
RUN apt install -y ruby-full
RUN apt install -y libpq-dev build-essential
RUN gem install fluent-plugin-secure-forward
RUN gem install fluent-plugin-influxdb
RUN gem install fluent-plugin-timescaledb
RUN gem install fluent-plugin-grafana-loki
RUN mkdir -p /fluentd/log
EXPOSE 24224
CMD fluentd -c /fluentd/etc/$FLUENTD_CONF -p /fluentd/plugins $FLUENTD_OPT
