# cli-utilities

## Files in directory

- Sorted by count
- Limit results
- Optionally group by path depth
- Print results as tsv, csv or json format

### Usage

```bash
❯ python src/dir_file_count.py --help
usage: dir_file_count.py [-h] [-c CUTOFF] [-r RESULT_COUNT] [-s DEPTH] [-d DIR] [-f {tsv,csv,json}]

Process some integers.

options:
  -h, --help            show this help message and exit
  -c CUTOFF, --cutoff CUTOFF
                        Minimum number of files in a directory for the directory to be considered (default: 100)
  -r RESULT_COUNT, --results RESULT_COUNT
                        Number of top results to show (default: 100)
  -s DEPTH, --show-depth DEPTH
                        Directory depth to show in the results (default: 3)
  -d DIR, --dir DIR     Directory to start the search from (default: current user's home directory)
  -f {tsv,csv,json}, --format {tsv,csv,json}
                        Output format (default: tsv)
```

### Examples

```bash
❯ python src/dir_file_count.py --cutoff 100 --results 3 --show-depth 4 --dir $HOME/Library --format json
[
    {
        "File Count": 74993,
        "Directory": "/Users/janispuris/Library/Caches"
    },
    {
        "File Count": 48132,
        "Directory": "/Users/janispuris/Library/Application Support"
    },
    {
        "File Count": 17565,
        "Directory": "/Users/janispuris/Library/Containers"
    }
]
```
