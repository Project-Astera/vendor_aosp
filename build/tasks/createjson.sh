#!/bin/bash
#
# Copyright (C) 2019-2022 crDroid Android Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#$1=TARGET_DEVICE, $2=PRODUCT_OUT, $3=FILE_NAME $4=Astera_BASE_VERSION
existingOTAjson=./vendor/officialdevices/devices/$1.json
output=$2/$1.json

#cleanup old file
if [ -f $output ]; then
	rm $output
fi

if [ -f $existingOTAjson ]; then
	#get data from already existing device json
	#there might be a better way to parse json yet here we try without adding more dependencies like jq
	filename=$3
	version=`echo "$4" | cut -d'-' -f5`
	v_max=`echo "$version" | cut -d'.' -f1 | cut -d'v' -f2`
	v_min=`echo "$version" | cut -d'.' -f2`
	version="$4"
	buildprop=$2/system/build.prop
	linenr=`grep -n "ro.system.build.date.utc" $buildprop | cut -d':' -f1`
    download="https://sourceforge.net/projects/project-astera/files/downloads/$1/$3/downloads"
	timestamp=`sed -n $linenr'p' < $buildprop | cut -d'=' -f2`
	md5=`md5sum "$2/$3" | cut -d' ' -f1`
	size=`stat -c "%s" "$2/$3"`
	buildtype=`grep -n "\"buildtype\"" $existingOTAjson | cut -d ":" -f 3 | sed 's/"//g' | sed 's/,//g' | xargs`

	echo '{
  "response": [
    {
      "datetime": '$timestamp',
      "filename": "'$filename'",
      "id": "'$md5'",
      "romtype": "'$buildtype'",
      "size": '$size',
      "url": "'$download'",
      "version": "'$version'"
    }
  ]
}
' >> $output

        echo "JSON file data for OTA support:"
else
	#if not already supported, create dummy file with info in it on how to
	echo 'There is no official support for this device yet' >> $output;
fi

cat $output
echo ""