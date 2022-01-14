import argparse
from bs4 import BeautifulSoup
import pathlib
import sys


def prettify_moss_match(match_html_template_path: pathlib.Path, source_dir: pathlib.Path, moss_match_top_file_path: pathlib.Path, output_path: pathlib.Path):
    # Load raw match
    moss_match_top_file = open(moss_match_top_file_path, 'r')
    moss_match_top_file_soup = BeautifulSoup(moss_match_top_file.read(), "html5lib")
    moss_match_top_file.close()

    moss_table_rows = moss_match_top_file_soup.find_all("tr")

    # Parse file paths and match percentages
    moss_header_cells = moss_table_rows[0].find_all("th")
    left_file_path, left_file_percent = moss_header_cells[0].text.split(' ')
    left_file_percent = left_file_percent[1:-1]
    right_file_path, right_file_percent = moss_header_cells[2].text.split(' ')
    right_file_percent = right_file_percent[1:-1]

    # Load match template
    match_html_template = open(match_html_template_path, 'r')
    template_soup = BeautifulSoup(match_html_template.read(), "html5lib")
    match_html_template.close()

    # Set title
    template_soup.title.string = left_file_path + " v " + right_file_path

    # Write file paths and percentages to table header
    matches_nav_table = template_soup.find("table", {"id": "matches_nav"})
    matches_nav_header_cells = matches_nav_table.find_all("th")
    matches_nav_header_cells[0].string = left_file_path
    matches_nav_header_cells[1].string = left_file_percent
    matches_nav_header_cells[2].string = right_file_percent
    matches_nav_header_cells[3].string = right_file_path

    # Add left file
    left_pre = template_soup.find("pre", {"id": "left_code_container"})
    left_code = template_soup.find("code", {"id": "left_code"})
    left_code.string = ""
    with open(source_dir / left_file_path, 'r') as f:
        for line in f:
            left_code.string += line

    # Add right file
    right_pre = template_soup.find("pre", {"id": "right_code_container"})
    right_code = template_soup.find("code", {"id": "right_code"})
    right_code.string = ""
    with open(source_dir / right_file_path, 'r') as f:
        for line in f:
            right_code.string += line

    # Write rows for each snippet of the match
    matches_nav_tbody = matches_nav_table.find("tbody")
    left_line_ranges = []
    right_line_ranges = []
    for row in moss_table_rows[1:]:
        moss_cells = row.find_all("td")

        # Parse left match info
        left_line_range = moss_cells[0].text.strip()
        left_line_range_begin = left_line_range.split('-')[0]
        left_match_percent = pathlib.Path(moss_cells[1].find_all("img")[0]["src"]).name[5:-4]
        left_line_ranges.append(left_line_range)

        # Parse right match info
        right_line_range = moss_cells[2].text.strip()
        right_line_range_begin = right_line_range.split('-')[0]
        right_match_percent = pathlib.Path(moss_cells[3].find_all("img")[0]["src"]).name[5:-4]
        right_line_ranges.append(right_line_range)

        # Write match info
        tr = template_soup.new_tag("tr")

        td = template_soup.new_tag("td", attrs={"class": "text-right"})
        anchor = template_soup.new_tag("a", attrs={"href": "#left_code." + left_line_range_begin})
        anchor.string = left_line_range
        td.append(anchor)
        tr.append(td)

        td = template_soup.new_tag("td")
        td.string = left_match_percent + '%'
        tr.append(td)

        td = template_soup.new_tag("td", attrs={"class": "text-right"})
        td.string = right_match_percent + '%'
        tr.append(td)

        td = template_soup.new_tag("td")
        anchor = template_soup.new_tag("a", attrs={"href": "#right_code." + right_line_range_begin})
        anchor.string = right_line_range
        td.append(anchor)
        tr.append(td)

        matches_nav_tbody.append(tr)

    # Highlight matched snippets in code
    left_pre["data-line"] = ','.join(left_line_ranges)
    right_pre["data-line"] = ','.join(right_line_ranges)

    # Output match
    output_file = open(output_path, 'w')
    output_file.write(template_soup.prettify())
    output_file.close()

    return [
        left_file_path,
        left_file_percent,
        right_file_path,
        right_file_percent
    ]


def main(argv):
    args_parser = argparse.ArgumentParser(description="Prettify an HTML report output by MOSS.")
    args_parser.add_argument("--moss-matches-dir", required=True, help="Directory containing MOSS matches.")
    args_parser.add_argument("--moss-submission-root-dir", required=True,
                             help="Root directory when submitting source to moss.")
    args_parser.add_argument("--templates-dir", required=True,
                             help="Directory containing HTML templates for pretty output.")
    args_parser.add_argument("--output-dir", required=True)
    parsed_args = args_parser.parse_args(argv[1:])
    moss_matches_dir = pathlib.Path(parsed_args.moss_matches_dir)
    source_dir = pathlib.Path(parsed_args.moss_submission_root_dir)
    templates_dir = pathlib.Path(parsed_args.templates_dir)
    output_dir = pathlib.Path(parsed_args.output_dir)

    # Create the output directory if necessary
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load index HTML template
    index_html_template = open(templates_dir / "index.html", 'r')
    index_template_soup = BeautifulSoup(index_html_template.read(), "html5lib")
    index_html_template.close()

    matches_table = index_template_soup.find("table", {"id": "matches"})
    matches_tbody = matches_table.find("tbody")
    match_ix = 0
    match_html_template_path = templates_dir / "match.html"
    while True:
        moss_match_top_file_path = moss_matches_dir / ("match" + str(match_ix) + "-top.html")
        if not moss_match_top_file_path.exists():
            # No more matches
            break

        output_filename = "match" + str(match_ix) + ".html"
        output_path = output_dir / output_filename

        # Generate pretty match
        left_file_path, left_file_percent, right_file_path, right_file_percent = prettify_moss_match(match_html_template_path, source_dir,
                                                                                                     moss_match_top_file_path, output_path)

        # Add match to index
        tr = index_template_soup.new_tag("tr")

        td = index_template_soup.new_tag("td", attrs={"class": "text-right"})
        anchor = index_template_soup.new_tag("a", attrs={"href": output_filename})
        anchor.string = left_file_path
        td.append(anchor)
        tr.append(td)

        td = index_template_soup.new_tag("td")
        td.string = left_file_percent
        tr.append(td)

        td = index_template_soup.new_tag("td", attrs={"class": "text-right"})
        td.string = right_file_percent
        tr.append(td)

        td = index_template_soup.new_tag("td")
        anchor = index_template_soup.new_tag("a", attrs={"href": output_filename})
        anchor.string = right_file_path
        td.append(anchor)
        tr.append(td)

        matches_tbody.append(tr)

        match_ix += 1

    # Output idnex
    output_file = open(output_dir / "index.html", 'w')
    output_file.write(index_template_soup.prettify())
    output_file.close()

    return 0


if "__main__" == __name__:
    sys.exit(main(sys.argv))
