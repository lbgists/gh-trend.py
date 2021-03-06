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

Output looks like:

```
https://github.com/user/repo
Description
(language)
```

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

Output looks like:

```
@user/repo
Description
(language)
```

Where `@user/repo` is a hyperlink. Note that there is no specification of encoding since it's only a partial HTML, therefore some Unicode characters may not be displayed correct until manually setting the encoding to UTF-8 in web browser.

Or a more complete HTML output:

```bash
echo "<html><head><title>gh-trend.py" > output.html
echo -e '</title><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body style="background-color:#000;color:#aaa;font-family:Inconsolata;font-weight:bold">\n' >> output.html
gh-trend.py [options] | awk "
/^https/ {
  print(\"<a href='\" \$0 \"' style='color:lawngreen;text-decoration:none'>\"\
        gensub(\"https://github.com/\", \"@\", \"\", \$0)\
        \"</a><br/>\");
  next;
}
/^\(.*\)$/ {
  print(\"<span style='color:lightblue'>\" \$0 \"</span><br/>\");
  next;
}
/^.+$/ {
  print(\"<span style='color:lightgrey'>\" \$0 \"</span> \");
  next;
}
/^$/ {
  print(\"<br/>\");
}
" >> output.html
echo '</body></html>' >> output.html
```

The output will look like:

![gh-trend html](https://lh6.googleusercontent.com/-8rkUlLIM_mg/UnHjsIjwtdI/AAAAAAAAFY4/EslKF78trZE/s800/gh-trend%2520html%25202013-10-31--12%253A26%253A41.png)

Bugs and Suggestions
--------------------

The script is very basic, not even any error checking or messages, like for bozo feeds or incorrect language names.

Feel free to comment below, or fork this Gist and notify me with your modifications.


Related Links
-------------

* Blog post about [why I wrote this script](https://yjlv.blogspot.com/2013/10/checking-new-trending-repos-on-github.html).


License
-------

This project is licensed under the MIT License, see `COPYING`.
