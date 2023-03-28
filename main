from film_database_creation import *
import argparse
import time
from database_query import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("create", type=bool)
    args = parser.parse_args()
    if args.create:
        basic_create(True)
    while True:
        try:
            # any queries should be executed in this block
            for f in get_film_titles():
                json = get_json(f)
            # please set returning/saving a JSON
        except KeyboardInterrupt:
            print(f"Sqlite server was shutdown at time: {time.time()}")
