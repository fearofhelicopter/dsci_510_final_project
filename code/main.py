import os
from data_collect_and_apis import main
from data_analysis_and_visualizations import main_data_analysis, generate_result
from data_decision_making_system import play_board

import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

if __name__ == '__main__':
    # if not data file, create one
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "../data")):
        os.mkdir(os.path.join(os.path.dirname(__file__), "../data"))
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "../result")):
        os.mkdir(os.path.join(os.path.dirname(__file__), "../result"))

    main()

    logging.info("data analysis start...")
    data = main_data_analysis()
    generate_result(data)
    logging.info("data analysis done...")
