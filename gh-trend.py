#!/usr/bin/env python3
# Listing new trending repo on GitHub
# Copyright (c) 2013, 2015 Yu-Jie Lin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Github: https://github.com/lbgists/gh-trend.py
# Blog  : https://yjlv.blogspot.com/2013/10/checking-new-trending-repos-on-github.html

import argparse
import json
import sys
from os import path

import feedparser as fp

fp.PREFERRED_XML_PARSERS.remove('drv_libxml2')

# default JSON file is in current working directory
DEFAULT_JSON = path.abspath(path.basename(sys.argv[0]) + '.json')

REPO_BASE = 'https://github.com/%s'
TREND_BASE = 'http://github-trends.ryotarai.info/rss/github_trends_%s_%s.rss'


def get_trend(lang, freq):

  for repo in fp.parse(TREND_BASE % (lang, freq)).entries:
    yield (repo.title.split(' ', 1)[0],   # "(#n - lang - freq)" is stripped
           repo.description or '')        # "\n(lang)" is kept


def main():

  p = argparse.ArgumentParser(description='List new trending repo')
  p.add_argument('-j', '--json', default=DEFAULT_JSON,
                 help='checked repos save file in JSON (default: %(default)s)')
  p.add_argument('-p', '--period',
                 choices=['today', 'this-week', 'this-month'],
                 default='today',
                 help='time period of trending (default: %(default)s)')
  p.add_argument('language', nargs='+',
                 help='language names, all lower case, spaces to dashes')
  args = p.parse_args()

  # get checked list
  LIST = {}
  LIST_CHANGED = False
  if path.exists(args.json):
    with open(args.json) as f:
      LIST = json.load(f)

  PERIODS = {'today': 'daily', 'this-week': 'weekly', 'this-month': 'monthly'}
  period = PERIODS[args.period]
  all_language = [lang.replace('cpp', 'c++') for lang in args.language]
  for lang in args.language:
    for repo, description in get_trend(lang, period):
      if repo in LIST:
        continue
      lang_desc = description.rsplit('\n', 1)[-1].strip('()').lower()
      if lang_desc and lang_desc not in all_language:
        continue
      print(REPO_BASE % repo)
      print(description)
      print()

      LIST[repo] = description
      LIST_CHANGED = True

  # save checked list
  if LIST_CHANGED:
    with open(args.json, 'w') as f:
      # save a JSON like
      # {
      # "user1/repo1": "description1\n(lang1)",
      # "user2/repo2": "description2\n(lang2)"
      # }
      json.dump(LIST, f, indent=0)


if __name__ == '__main__':
  main()
