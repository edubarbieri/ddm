#!/bin/bash

echo "===========Start DDM==========="


docker run -it --rm \
    --user "$(id -u):$(id -g)" \
    -v "$PWD":/usr/src/ddm \
    -w /usr/src/ddm \
    -v /u01/transmission/completes:/completes \
    -v /u01/media/tvshows:/u01/media/tvshows \
    -v /u01/media/movies:/u01/media/movies \
    --name DudaDownloadManager \
    python:3 sh -c 'cd /usr/src/ddm \
        && pip install -r requirements.txt \
        && python ddm.py'

echo "===========End DDM==========="
