#!/usr/bin/env bash

USAGE="Usage:
$0 REPOLIST_PATH TARGET_HOSTNAME [PROJECT_PATH]

Mandatory parameters:
  REPOLIST_PATH   - Path to the repolist.json file
  TARGET_HOSTNAME - Hostname of the target machine where vmaas server is running

Optional parameters:
  PROJECT_PATH - Path to the project to speed up waiting for tasks; only works
                 when TARGET_HOSTNAME is 'localhost' and both the client and server
                 are running in the same timezone (VMaaS server runs in UTC by default)
"

wait_and_run() {
  count=60
  while [ "$count" -gt 0 ]; do
    resp="$("$@")"
    if [[ "$resp" != *"Another sync task already in progress"* ]]; then
      echo "$resp"
      echo
      break
    fi
    ((count--))
    sleep 10
  done
}

# 2 arguments expected, 3 if TARGET_HOSTNAME is localhost / 127.0.0.1
if ! ([ "$#" -eq "2" ] || ([ "$#" -eq "3" ] && ([ "$2" == "localhost" ] || [ "$2" == "127.0.0.1" ]))); then
	echo "$USAGE" >&2
	exit 1
fi

printf "Step 1/3: Repo sync\nAPI Response: "
wait_and_run curl -sS -d "@${1}" -X POST "http://${2}:8081/api/v1/sync/repo"

printf "Step 2/3: CVE sync from NIST\nAPI Response: "
wait_and_run curl -sS -X GET "http://${2}:8081/api/v1/sync/cve"

printf "Step 3/3: CVE sync from RH\nAPI Response: "
wait_and_run curl -sS -X GET "http://${2}:8081/api/v1/sync/cvemap"

printf "Workaround for GH#271: "
wait_and_run curl -sS -X GET "http://${2}:8081/api/v1/sync/export"


# check that every sync is finished
wait_and_run curl -sS -X GET "http://${2}:8081/api/v1/sync/export" >/dev/null

echo "Done."
