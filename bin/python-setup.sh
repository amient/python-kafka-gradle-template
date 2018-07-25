#!/usr/bin/env bash

################################################################################################################

reuquired=( "avro-python3:1.8.2" \
            "avro-gen:0.3.0" \
            "confluent-kafka:0.11.0" \
            "confluent-kafka:0.11.5")

################################################################################################################



DIR="$( cd $(dirname ${BASH_SOURCE[0]}) && pwd )"
LOCAL_REPO_DIR="$HOME/pypi-ivy"
PIVY_IMPORTER_VERSION="0.7.4"

if [ ! -f "$DIR/build/pygradle/build/pivy-importer/libs/pivy-importer-$PIVY_IMPORTER_VERSION-SNAPSHOT-all.jar" ]; then
    if [ ! -d "$DIR/build/pygradle" ]; then
        git clone https://github.com/linkedin/pygradle.git $DIR/build/pygradle
    fi
    cd "$DIR/build/pygradle"
    git checkout "v$PIVY_IMPORTER_VERSION"
    ./gradlew build --exclude-task test --exclude-task integTest
    if [ $? -ne 0 ]; then
        echo "failed to build pivy-importer"
        exit 1;
    fi
fi

mkdir -p "$LOCAL_REPO_DIR"
if [ $? -ne 0 ]; then
    echo "could not create $LOCAL_REPO_DIR"
    exit 1;
fi

#clean broken cached downloads
find $LOCAL_REPO_DIR -name *.tar.gz | while read file; do tar -tzf $file  > /dev/null; if [ $? -ne 0 ]; then echo "fixing: $file"; rm $file; fi done


do_update=""
for package in "${reuquired[@]}"
do
    if [ ! -d "$LOCAL_REPO_DIR/pypi/${package//://}" ]; then
        do_update="$do_update $package"
    fi
done

if [ ! -z "$do_update" ]; then
java -jar $DIR/build/pygradle/build/pivy-importer/libs/pivy-importer-0.7.4-SNAPSHOT-all.jar \
    --replace Babel:0.8=Babel:1.0 \
    --replace python-dateutil:1.0=python-dateutil:2.4.1 \
    --repo "$LOCAL_REPO_DIR" \
    $do_update
fi
