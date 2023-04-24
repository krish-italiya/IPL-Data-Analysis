# IPL Data Analysis Project

This project is a data analysis of the Indian Premier League (IPL), based on the 'matches.csv' and 'deliveries.csv' datasets available on Kaggle. The purpose of the analysis is to explore and visualize the data to gain insights into the performance of different teams and players.

## Project Structure

The project consists of the following files:

-  Project contains the 'matches.csv' and 'deliveries.csv' datasets
- `app.py`: Python file
- `README.md`: this file

## Data Description

The 'matches.csv' dataset contains information about the IPL matches, including the date, location, teams, toss winner, winner, player of the match, result, and other details. The 'deliveries.csv' dataset contains information about the individual deliveries in each match, including the over number, ball number, batsman, bowler, runs scored, and other details.

## Analysis

The analysis is performed using Python and various data analysis libraries, including Pandas, NumPy, and Matplotlib and for visualization I used python library streamlit . The code is contained in the `app.py` python file . The analysis consists of the following steps:

1. Data Loading and Cleaning: The datasets are loaded into Pandas DataFrames and cleaned to remove any missing or inconsistent data.

2. Exploratory Data Analysis: Various exploratory data analysis techniques are applied to understand the structure and patterns in the data. This includes summary statistics, histograms, bar charts, and scatter plots.

3. Team Performance Analysis: The performance of different teams is analyzed, including their win/loss record, batting and bowling performance, and home/away performance.

4. Player Performance Analysis: The performance of individual players is analyzed, including their batting and bowling statistics, player of the match awards, and overall impact on the team's performance.

## Results

The analysis reveals several interesting insights about the IPL, including:

- Mumbai Indians is the most successful team in IPL history, with the highest win percentage and the most number of titles.
- Sunrisers Hyderabad has the best bowling attack, with the lowest economy rate and the most number of wickets.
- David Warner and Chris Gayle are the most successful batsmen in IPL history, with the highest strike rates and the most number of runs.

These insights are supported by various visualizations and tables generated as part of the analysis.

## Requirements

The following software and libraries are required to run the code:

- Python 3.x
- Pandas
- NumPy
- Matplotlib
- Streamlit

## Usage

To run the code, open the `app.py` python file and run the following command in terminal,
> streamlit run app.py

## Acknowledgements

This project is based on the 'matches.csv' and 'deliveries.csv' datasets available on Kaggle. The data was originally sourced from the IPL website. The code was developed with the help of various online tutorials and resources.

