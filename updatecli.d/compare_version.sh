#!/bin/bash

remote="$1"
local="$2"

remote="${remote#v}"
local="${local#v}"

compare_versions() {
    local IFS=.
    local remote_arr=($1)
    local local_arr=($2)

    for ((i=0; i<${#remote_arr[@]}; i++)); do
        if (( ${remote_arr[i]} > ${local_arr[i]} )); then
            return 0
        elif (( ${remote_arr[i]} < ${local_arr[i]} )); then
            return 1
        fi
    done
    return 1
}

compare_versions "$remote" "$local"
exit $?
