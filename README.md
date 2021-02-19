At the time of writing, MOSS' output does not have syntax highlighting. Syntax 
highlighting can help to more quickly compare two matches, e.g., you can 
quickly ignore a commented block of code.

# Dependencies
* python3
* beautifulsoup4: `pip install beautifulsoup4`

# Usage
* Download matches from a MOSS report using `download-moss-matches.py`
* Prettify them using `prettify-moss-matches.py`

# Examples
* Download MOSS matches from a report
  ```
  python3 ./download-moss-matches.py \
    --report-url http://moss.stanford.edu/results/9/999999999999 \
    --output-dir asst1-matches/
  ```
* Prettify downloaded matches
  ```
  python3 ./prettify-moss-matches.py \
    --moss-matches-dir asst2-matches/ \
    --source-dir . \
    --templates-dir html-templates \
    --output-dir asst2-matches-pretty/
  ```
