import os
from pathlib import Path
import itertools
import argparse
import json


def tuple_to_csv(
    data: list[tuple[int, str]],
    sep: str,
    header: tuple[str] = None,
) -> str:
    """Converts a list of tuples to a CSV string

    Args:
        data (list[tuple[int, str]]): List of tuples to convert
        sep (str): Separator to use
        header (tuple[str], optional): Header to use. Defaults to None.

    Returns:
        str: CSV string
    """
    results = []
    if header is not None:
        results.append(sep.join(header))
    results.extend(sep.join([str(value) for value in row]) for row in data)
    return "\n".join(results)


def print_results(
    data: list[tuple[int, str]],
    count: int,
    format: str,
    header: tuple[str] = None,
) -> None:
    """Prints tuple data in the specified format

    Args:
        data (list[tuple[int, str]]): List of tuples to print
        count (int): Number of results to print
        format (str): Output format
        header (tuple[str], optional): Header to use. Defaults to None.
    """
    data = data[:count]
    if format == "tsv":
        print(tuple_to_csv(data, "\t", header))
    elif format == "csv":
        print(tuple_to_csv(data, ",", header))
    elif format == "json":
        dict_data = [dict(zip(header, val)) for val in data]
        json_data = json.dumps(dict_data, indent=4)
        print(json_data)


def get_dir_file_count(
    search_dir: str,
    cutoff: int = 100,
    show_result_depth: int = None,
) -> list[tuple[int, str]]:
    """Gets the number of files in each directory in the specified directory
        and its subdirectories. Will group the results by the specified depth. When the
        depth is below 1 or None, the results will not be grouped.

    Args:
        search_dir (str, optional): Directory to search.
        cutoff (int, optional): Minimum number of files in
            a directory for the directory to be considered. Defaults to 100.
        show_result_depth (int, optional): Directory depth to show in the results.
            Defaults to None.

    Returns:
        list[tuple[int, str]]: List of tuples containing the number of files
            and the directory path
    """
    results = []
    for dir, _, files in os.walk(search_dir):
        file_count = len(files)
        if file_count > cutoff:
            results.append((file_count, dir))

    # print the top N results
    sorted_results = sorted(results, reverse=True)
    if show_result_depth > 0:
        # truncate the paths to the specified depth
        depth_truncated_paths = [
            (res[0], f"{os.sep}".join(res[1].split(os.sep)[: show_result_depth + 1]))
            for res in sorted_results
        ]
        # group the results by the truncated path
        results = sorted(
            [
                (sum(i[0] for i in group), key)
                for key, group in itertools.groupby(
                    sorted(depth_truncated_paths, key=lambda i: i[1]), lambda i: i[1]
                )
            ],
            reverse=True,
        )
    else:
        results = sorted_results

    return results


parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument(
    "-c",
    "--cutoff",
    type=int,
    default=100,
    help="Minimum number of files in a directory for the directory to be considered (default: 100)",
)
parser.add_argument(
    "-r",
    "--results",
    dest="result_count",
    type=int,
    default=100,
    help="Number of top results to show (default: 100)",
)
parser.add_argument(
    "-s",
    "--show-depth",
    dest="depth",
    type=int,
    default=3,
    help="Directory depth to show in the results (default: 3)",
)
parser.add_argument(
    "-d",
    "--dir",
    type=str,
    default=str(Path.home()),
    help="Directory to start the search from (default: current user's home directory)",
)
parser.add_argument(
    "-f",
    "--format",
    type=str,
    default="tsv",
    help="Output format (default: tsv)",
    choices=["tsv", "csv", "json"],
)
args = parser.parse_args()

results = get_dir_file_count(
    search_dir=args.dir,
    cutoff=args.cutoff,
    show_result_depth=args.depth,
)

print_results(
    results,
    args.result_count,
    args.format,
    header=("File Count", "Directory"),
)
