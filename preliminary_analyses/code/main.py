import os
from data_collect_and_apis import main

if __name__ == '__main__':
    # if not data file, create one
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "./data")):
        os.mkdir(os.path.join(os.path.dirname(__file__), "./data"))
    main()