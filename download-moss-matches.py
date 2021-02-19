import argparse
import pathlib
import requests
import sys
import time


def main(argv):
    args_parser = argparse.ArgumentParser(description="Download match information from a MOSS report.")
    args_parser.add_argument("--report-url", required=True, help="MOSS report URL.")
    # NOTE: We could try and automate this by incrementing the URL until it returns 404, but this is unreliable since MOSS can get overloaded
    args_parser.add_argument("--num-matches", default=250, type=int, help="Number of matches in the report.")
    args_parser.add_argument("--output-dir", required=True)
    parsed_args = args_parser.parse_args(argv[1:])
    base_report_url = parsed_args.report_url
    num_matches = parsed_args.num_matches
    output_dir = pathlib.Path(parsed_args.output_dir)

    # Create the output directory if necessary
    output_dir.mkdir(parents=True, exist_ok=True)

    for i in range(num_matches):
        match_filename = "match" + str(i) + "-top.html"
        match_output_path = output_dir / match_filename

        if match_output_path.exists():
            # Match already downloaded
            continue

        # Download
        r = requests.get(base_report_url + '/' + match_filename, allow_redirects=True)
        with open(match_output_path, "wb") as f:
            f.write(r.content)

        # Wait before the next download to avoid MOSS throttling us
        time.sleep(1)

    return 0


if "__main__" == __name__:
    sys.exit(main(sys.argv))
