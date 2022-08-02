#!/usr/bin/python3
#
# Usage:
# scripts/upload-assets.py VERSION
#
# where VERSION is a version string like "v1.2.3" or "latest"
#
# Generates static assets for HTML, JS, and CSS.
# Then uploads them to the public bucket.

import argparse
import os
import subprocess
import sys


parser = argparse.ArgumentParser(description='Upload JS assets')
parser.add_argument('--clean', action='store_true',
                    help='Instead of uploading assets, delete assets of the given version (if they exist)')
parser.add_argument('version', help='A version string like "v1.2.3".')
args = parser.parse_args()
version = args.version
if version == "latest":
  version = subprocess.check_output([
    "git", "describe", "--tags", "--abbrev=0"
  ]).decode('utf-8').strip()

dir_url = f"https://storage.googleapis.com/tilt-static-assets/{version}/"

if args.clean:
    # Just remove the bucket and exit w/o uploading anything
  print(f"Deleting bucket at {dir_url} (if exists)")
  subprocess.call(
      ["gsutil", "-m", "rm", "-r", f"gs://tilt-static-assets/{version}"],
      stderr=open(os.devnull, 'wb'),
  )
  sys.exit(0)

url = f"{dir_url}index.html"
print(f"Uploading to {dir_url}")
status = subprocess.call(
    ["gsutil", "stat", f"gs://tilt-static-assets/{version}/index.html"])
if status == 0:
  print(f"Error: bucket already exists at: {url}")
  print("Remove the bucket by running this script with --clean,")
  print("or manually delete the bucket at:")
  print((
      "\thttps://console.cloud.google.com/storage/browser/tilt-static-assets" +
      f"?forceOnBucketsSortingFiltering=false&project=windmill-prod&prefix={version}"
  ))
  print("Then try uploading assets again.")
  sys.exit(1)

os.chdir("web")
subprocess.check_call(["yarn", "install"])
e = os.environ.copy()
e["CI"] = "false"
subprocess.check_call(["yarn", "run", "build"], env=e)
subprocess.check_call([
    "gsutil", "-m", "cp", "-r", "build", f"gs://tilt-static-assets/{version}"
])
