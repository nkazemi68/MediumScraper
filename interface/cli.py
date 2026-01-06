import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topics", required=True)
    parser.add_argument("--profiles", required=True)
    parser.parse_args()