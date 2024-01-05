#Author: Davit Najaryan

#Student Number: 251337836

#uwo username: dnajarya

#Date: Nov 15, 2023

#Description: This file should take input from the user and call the functions in sentiment_analysis.py



# Import the sentiment_analysis module

from sentiment_analysis import *



def main():

	# Add code for main() here.

	# This should get input from the user and call the 

	# required functions from sentiment_analysis.py


	keyword_file_name = input("Input keyword filename (.tsv file): ")


	#check if it end with a tsv

	if keyword_file_name.endswith(".tsv") == False:

		raise Exception("Must have tsv file extension!")

	else:

		keyword_dict = read_keywords(keyword_file_name)

		#check if keywords is empty

		if keyword_dict == None:

			raise Exception("Tweet list or keyword dictionary is empty!")


	tweet_file_name = input("Input tweet filename (.csv file): ")


	#check if it ends with a csv

	if tweet_file_name.endswith(".csv") == False:

		raise Exception("Must have csv file extension!")

	else:

		tweet_list = read_tweets(tweet_file_name)

		#check if tweets is empty

		if tweet_list == None:

			raise Exception("Tweet list or keyword dictionary is empty!")


	report = make_report(tweet_list, keyword_dict)


	output_file = input("Input filename to output report in (.txt file): ")


	if output_file.endswith(".txt") == False:

		raise Exception("Must have txt file extension!")

	else:

		write_report(report, output_file)



main()
