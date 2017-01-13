#!/usr/bin/env bash

cp ../configs/sysctl.conf /etc
sysctl -p

apt-get update && apt-get install keepalived haproxy -y

cp ../configs/keepalived.conf /etc/keepalived/keepalived.conf
cp ../configs/haproxy.cfg /etc/haproxy/haproxy.cfg
cp ../configs/haproxy /etc/default/haproxy