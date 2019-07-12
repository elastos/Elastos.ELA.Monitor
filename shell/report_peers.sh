#!/usr/bin/env bash
 cd ~/monitor/ && source py3env/bin/activate && python3 ./Elastos.ELA.Monitor/report_peers.py -n ${1}