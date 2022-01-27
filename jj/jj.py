#!/usr/bin/env python3
"""CLI for querying and parsing Jenkins jobs."""
import requests
import datetime
import os
import json
import argparse


def get_time_delta(jobs, filter_ob):
    """For handling input of a low timestamp and high timestamp."""
    final_returns = []
    now = int(datetime.datetime.now().timestamp())
    delta_sec = filter_ob["timedelta"] * 3600
    since = now - delta_sec
    for job in jobs:
        if int(job["timestamp"]) / 1000 > since:
            if job["duration"] > filter_ob["normal_duration"]:
                final_returns.append(
                    {
                        job["id"]: {
                            "ts": job["timestamp"],
                            "ts_utc": datetime.datetime.fromtimestamp(
                                job["timestamp"] / 1000, datetime.timezone.utc
                            ).strftime(date_format),
                            "ts_pst": datetime.datetime.fromtimestamp(
                                job["timestamp"] / 1000
                            ).strftime(date_format),
                            "duration": job["duration"],
                            "url": job["url"],
                        }
                    }
                )
    return final_returns


def get_id_delta(jobs, filter_ob):
    """For handling input of a job id range."""
    final_returns = []
    for job in jobs:
        if (
            int(job["id"]) > filter_ob["lowid"]
            and int(job["id"]) < filter_ob["highid"]
        ):
            if job["duration"] > filter_ob["normal_duration"]:
                final_returns.append(
                    {
                        job["id"]: {
                            "ts_utc": datetime.datetime.fromtimestamp(
                                job["timestamp"] / 1000, datetime.timezone.utc
                            ).strftime(date_format),
                            "ts_pst": datetime.datetime.fromtimestamp(
                                job["timestamp"] / 1000
                            ).strftime(date_format),
                            "duration": job["duration"],
                            "url": job["url"],
                        }
                    }
                )
    return final_returns


def apply_filter(ret, filter_ob):
    """Filter results."""
    if filter_ob["lowid"] and filter_ob["highid"]:
        return get_id_delta(ret, filter_ob)
    elif filter_ob["timedelta"]:
        return get_time_delta(ret, filter_ob)


def query_jenkins(url):
    """Rest API call."""
    ret = requests.get(url).json()["allBuilds"]
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse Jenkins job base on duration or date"
    )
    parser.add_argument(
        "-t",
        "--timedelta",
        default=24,
        type=int,
        help="Get jobs from since this value to now",
    )
    parser.add_argument(
        "-l",
        "--lowid",
        type=int,
        help="Specify job id range, must have -i or --highid",
    )
    parser.add_argument(
        "-i",
        "--highid",
        type=int,
        help="Specify job id range, must have -l or --lowid",
    )
    parser.add_argument(
        "-d",
        "--duration",
        type=int,
        default=68000,
        help="Specify job duration in milliseconds, default around 70,000ms",
    )
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        default="dluo",
        help="Your name/token for querying jenkins",
    )
    parser.add_argument(
        "-j",
        "--jenkinsurl",
        type=str,
        default="jenkins.wildrift.ci.riotgames.io",
        help="Your jenkins url",
    )
    parser.add_argument(
        "-b",
        "--jenkinsjob",
        type=str,
        default="JointArtSync",
        help="Your jenkins job name",
    )
    parser.add_argument(
        "-q",
        "--jenkinsquery",
        type=str,
        default="tree=allBuilds[id,duration,timestamp,url]",
        help="Your jenkins job query, default to all builds",
    )
    parser.add_argument(
        "-k",
        "--jenkinstoken",
        type=str,
        help="Your jenkins api token",
    )
    args = parser.parse_args()
    filter_ob = {
        "lowid": None,
        "highid": None,
        "timedelta": None,
        "normal_duration": None,
    }
    if args.lowid and args.highid:
        filter_ob["lowid"] = args.lowid
        filter_ob["highid"] = args.highid
    else:
        filter_ob["timedelta"] = args.timedelta
    filter_ob["normal_duration"] = args.duration

    user = args.user if args.user else os.environ.get("jjuser", "dluo")
    token = (
        args.jenkinstoken
        if args.jenkinstoken
        else os.environ.get("jjtoken", "")
    )
    jenkins_url = (
        args.jenkinsurl
        if args.jenkinsurl
        else os.environ.get("jjjurl", "jenkins.wildrift.ci.riotgames.io")
    )
    job_name = (
        args.jenkinsjob
        if args.jenkinsjob
        else os.environ.get("jjjobname", "JointArtSync")
    )
    query = (
        args.jenkinsquery
        if args.jenkinsquery
        else os.environ.get(
            "jjquery", "tree=allBuilds[id,duration,timestamp,url]"
        )
    )
    date_format = "%Y-%m-%d %H:%M:%S"

    url = (
        f"https://{user}:{token}@{jenkins_url}/job/{job_name}/api/json?{query}"
    )
    ret = query_jenkins(url)
    filtered = apply_filter(ret, filter_ob)
    print(json.dumps(filtered, indent=2))
#
# jenkins.riotgames.com
# CEFF_SourceArtValidation
