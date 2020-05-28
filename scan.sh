#!/bin/bash
#

PROJECT=$1
VERSION=$2
SOURCE_PATH=$3

if [ "$PROJECT" = "" ] 
then
  PROJECT=$(pwd)
fi

if [ "$VERSION" = "" ]
then
  VERSION=LATEST
fi

bash <(curl -s -L https://detect.synopsys.com/detect.sh) --blackduck.url=https://ec2-3-21-46-158.us-east-2.compute.amazonaws.com \
--blackduck.api.token= ZDI4OTBlMjMtNDBlNi00MDJhLTk3M2EtNTA2MmY3ZTQwMTMxOmI3YjJiZDZjLTE5ZmQtNGYwYy1iNmU2LWNhYzM5OTgyOTliMw== \
--blackduck.trust.cert=true \
--detect.project.name=hub-spdx \
     --detect.project.version.name=${VERSION} \
     --detect.source.path=${PROJECT}/${SOURCE_PATH} \
     --detect.code.location.name=${PROJECT}_${VERSION}_$3_code \
     --detect.bom.aggregate.name=${PROJECT}_${VERSION}_$3_PKG \
     --detect.excluded.detector.types=ALL

