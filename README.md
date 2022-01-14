At the time of writing, MOSS' output does not have syntax highlighting. Syntax 
highlighting can help to more quickly compare two matches, e.g., you can 
quickly ignore a commented block of code.

# Dependencies

* python3
* beautifulsoup4: `pip3 install beautifulsoup4`

# Usage

* Download matches from a MOSS report using `download-moss-matches.py`
* Prettify them using `prettify-moss-matches.py`
* Use the `--help` option to see more details

Note that `prettify-moss-matches.py` uses the source paths listed in the match
files to find the source files on disk:

* E.g., if you ran moss like
`run-moss.py --src-dir-pattern "../asst1/os-*/threads" ...`, then the
match files would contain paths like 
`../asst1/os-001/threads/thread.c`.
* So the
`--moss-submission-root-dir` option of `prettify-moss-matches.py` should point
at a directory `dir` such that `dir/../asst1/os-001/threads/thread.c` refers to a valid
source file.

# Examples

* Download MOSS matches from a report
  ```
  python3 ./download-moss-matches.py \
    --report-url http://moss.stanford.edu/results/9/999999999999 \
    --output-dir ../submissions/asst1-matches/
  ```
* Prettify downloaded matches
  ```
  python3 ./prettify-moss-matches.py \
    --moss-matches-dir ../submissions/asst1-matches/ \
    --moss-submission-root-dir ../submissions \
    --templates-dir html-templates \
    --output-dir ../submissions/asst1-matches-pretty/
  ```
