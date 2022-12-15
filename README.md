# dsci510_project_cars

### branch main: with clean data
### branch withdata: with generated data

## Code files description:
#### 1. data collect and apis.py: the code for connecting cars API and collecting the data.
#### 2. main.py main code to run
#### 3. data_decision_making_system.py : the code for decision-making
#### 4. config.py configs
#### 5. data_analysis_and_visualizations.py: the code for analysis the data
#### 6. two jupyter notebooks: test file, not important
## How to run the code:
#### pre-require environment: python>=3.6
#### 1. pip install -r requirements.txt 
#### 2. cd code
#### 3. python main.py
#### to play with decision-making system (under code file)
#### 4. python data_decision_making_system.py
## Data description:
#### 7 files with roughly 5000 samples
#### The original data format is JSON. 
#### After requesting the API, the keywords are collected and converted into a data frame format and saved as CSV files.
#### The collected keywords are make, model, price, trim, repair, total_price, and maintenance.
## Result figure description (under results):
#### Car Price Changes from 2021 to 2022 is the figure that shows the price changes of different models. The red line is the 2022 price, and the black line is the 2021 price. It can be found that the red line is mostly above the black line, indicating price increases.
#### Car Price Changes for Different Classes is the figure that shows the price changes for different categories of models. Compared with affordable and economical cars, the price of luxury cars changes very little. 
#### Car Price Increase Rate from 2021 to 2022 is the figure that shows the growth rate of the prices of different models.
#### Car Price Increase Rate for Different Classes is the figure that shows the growth rate of different categories of car prices.
## Link to the GitHub repository: 
#### https://github.com/fearofhelicopter/dsci_510_final_project
