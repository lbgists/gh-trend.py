Listing new trending repo on GitHub
===================================

`gh-trend.py` uses [GitHub Trend RSS][trendrss] as the data source and lists new trending repos. Each repo will only be listed once in output.

[trendrss]: http://github-trends.ryotarai.info/


Usage
-----

```
gh-trend.py [-h] [-j JSON] [-p {today,this-week,this-month} language [language ...]
```

* `-j` is the saved JSON file, which is used to check if a repo has been listed before.
* `-p` the trending period, one of `today`, `this-week`, or `this-month`.
* language, the names of interested languages.

Examples:

```bash
$ gh-trend.py -p this-week all python bash
$ gh-trend.py -j $HOME/.gh-trend.json objective-c common-lisp csharp cpp
```

You may want to check the [RSS URLs][trendrss] for correct language names.


### With cron

It could be a nice idea to use with cron, e.g.

```
@daily      /path/to/gh-trend.py -j /path/to/saved.json               all python bash >> /path/to/output.txt
@weekly     /path/to/gh-trend.py -j /path/to/saved.json -p this-week  all python bash >> /path/to/output.txt
@monthly    /path/to/gh-trend.py -j /path/to/saved.json -p this-month all python bash >> /path/to/output.txt
```

Your cron's syntax may differ, check with its manual pages.


### Converting to HTML

The following AWK code converts the output into simple HTML code:

```bash
gh-trend.py [options] | awk "
/^https/ {
  print(\"<a href='\" \$0 \"'>\"\
        gensub(\"https://github.com/\", \"@\", \"\", \$0)\
        \"</a><br/>\");
  next;
}
/^.+$/ {
  print(\"<span>\" \$0 \"</span><br/>\");
  next;
}
/^$/ {
  print(\"<br/>\");
}
" > output.html
```


Bugs and Suggestions
--------------------

The script is very basic, not even any error checking or messages, like for bozo feeds or incorrect language names.

Feel free to comment below, or fork this Gist and notify me with your modifications.


Related Links
-------------

* Blog post about [why I wrote this script](#).


License
-------

This project is licensed under the MIT License, see `COPYING`.
