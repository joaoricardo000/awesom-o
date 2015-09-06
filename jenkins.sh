#!/usr/bin/env bash
if [ ! -f /opt/awesom-o/venv/bin/python ]; then
    virtualenv /opt/awesom-o/venv
fi
if [ ! -d /opt/awesom-o/log ]; then
    mkdir /opt/awesom-o/log
fi
/opt/awesom-o/venv/bin/pip install -r /opt/awesom-o/opt/requirements.pip
supervisorctl restart awesom-o