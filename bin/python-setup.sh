#!/usr/bin/env bash

reuquired=($@)

######################################################################

LOCAL_REPO_DIR="$HOME/pypi-ivy"
PIVY_IMPORTER_VERSION="0.7.4"

if [ ! -f "$LOCAL_REPO_DIR/pygradle/build/pivy-importer/libs/pivy-importer-$PIVY_IMPORTER_VERSION-SNAPSHOT-all.jar" ]; then
    if [ ! -d "$LOCAL_REPO_DIR/pygradle" ]; then
        git clone https://github.com/linkedin/pygradle.git $LOCAL_REPO_DIR/pygradle
    fi
    cd "$LOCAL_REPO_DIR/pygradle"
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
    package_dir="$LOCAL_REPO_DIR/pypi/${package//://}"
    if [ ! -d "$package_dir" ]; then
        do_update="$do_update $package"
    else
        echo "$package      already present: $package_dir"
    fi
done

if [ ! -z "$do_update" ]; then
java -jar $LOCAL_REPO_DIR/pygradle/build/pivy-importer/libs/pivy-importer-$PIVY_IMPORTER_VERSION-SNAPSHOT-all.jar \
    --replace Babel:0.8=Babel:1.0 \
    --replace python-dateutil:1.0=python-dateutil:2.4.1 \
    --repo "$LOCAL_REPO_DIR" \
    $do_update
fi
