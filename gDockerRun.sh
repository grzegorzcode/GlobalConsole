#!/bin/bash

docker run -it --rm -v `pwd`:/usr/src/app global_console:`cat VERSION`  /bin/bash