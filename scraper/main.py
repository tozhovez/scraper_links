import os
import asyncio
import argparse
import functools
import signal
from pprint import pprint
from spider import Task, DomainEmptyTypeError


def main():
    parser = argparse.ArgumentParser(description='Scraper should receive 2 params: initial url & max depth.')
    parser.add_argument('--url', help='initial url', type=str, required=True)
    parser.add_argument('--depth', help='max depth', type=int, required=True)
    args = parser.parse_args()
    output = "./pages"

    try:
        job = Task(args.url, args.depth, output)
        job.start_spider()
        pprint(job.__dict__)
    except DomainEmptyTypeError as ex:
        print(ex)
        exit()

if __name__ == "__main__":
    main()
