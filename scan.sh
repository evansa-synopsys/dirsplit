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

bash <(curl -s -L https://detect.synopsys.com/detect.sh) --blackduck.url=<BD_URL> --blackduck.api.token=<BD_API_TOKEN> --blackduck.trust.cert=true \
--detect.project.name=hub-spdx \
     --detect.project.version.name=${VERSION} \
     --detect.source.path=${PROJECT}/${SOURCE_PATH} \
     --detect.code.location.name=${PROJECT}_${VERSION}_$3_code \
     --detect.bom.aggregate.name=${PROJECT}_${VERSION}_$3_PKG \
     --detect.excluded.detector.types=ALL

