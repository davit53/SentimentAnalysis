#Author: Davit Najaryan

#Student Number: 251337836

#uwo username: dnajarya

#Date: Nov 15, 2023

#Description: this code will handle all the functions necessary to read/write/analyze/report the data


#This function will read the keywords from the tsv file and return a dictionary of those keywords

def read_keywords(keyword_file_name):


    my_dict = {}


    try:


        file = open(keyword_file_name,"r")

        #make the file into a list of words

        text = file.readlines()


        #use a for loop to delete the unessasary charchers from the words 

        for line in text:


            # Split the line into a list of words

            words = line.strip().split('\t')


            my_dict[words[0]] = words[1]


        return my_dict

    

    except IOError:


        print(f"Could not open file {keyword_file_name}!")

        return {}

    


#This fucntion will return a string with the clean tweet text

def clean_tweet_text(tweet_text):


    clean_tweet = tweet_text.lower()


    #loop through the tweet and replace all unessasary characters

    for i in clean_tweet:

        if i not in "abcdefghijklmnopqrstuvwxyz ":

            clean_tweet = clean_tweet.replace(i, "")


    #check if the beggining of the string starts with a space, get rid of it if it does

    if clean_tweet.startswith(" ") == True:

        clean_tweet = clean_tweet.replace(" ", "", 1)


    #replace consecutive spaces with one space

    while "  " in clean_tweet:

        clean_tweet = clean_tweet.replace("  ", " ")


    return clean_tweet



#This fucniton will calculate the sentiment score based on the text and return the score in an int value

def calc_sentiment(tweet_text, keyword_dict):


    score = 0


    #split the clean tweet into a list of words

    words = tweet_text.split()


    #iterate through the list of words and compare it to the keys of the dictionary

    for i in words:

        if i in keyword_dict.keys():

            score += int(keyword_dict[i])


    return score


#This function will take entiment score, and return a str of positive, negative or neutural

def classify(score):


    if score > 0:

        return "positive"

    elif score == 0:

        return "neutral"

    else:

        return "negative"


#This function will read the csv file and return a list with a dicitionary for each tweet

def read_tweets(tweet_file_name):


    my_list = []


    try:

        #read the file and split every line into a list

        file = open(tweet_file_name,"r")

        text = file.readlines()


        #iterate through each row

        for line in text:


            my_dict = {}


            #split the line using the commas

            row = line.strip().split(',')


            created_at = str(row[0])

            tweet_text = str(row[1]) 

            username = str(row[2])

            retweet_count = int(row[3])

            favourite_count = int(row[4])

            language = str(row[5])

            country = str(row[6])

            state_province = str(row[7])

            city = str(row[8])

            if row[9] == "NULL":

                latitude = str(row[9])

            else:

                latitude = float(row[9])

            if row[10] == "NULL":

                longitude = str(row[10])

            else:

                longitude = float(row[10])


            #append all the values into the dicitonary

            my_dict['city'] = city

            my_dict['country'] = country

            my_dict['date'] = created_at

            my_dict['favorite'] = favourite_count

            my_dict['lang'] = language

            my_dict['lat'] = latitude

            my_dict['lon'] = longitude

            my_dict['retweet'] = retweet_count

            my_dict['state'] =  state_province

            my_dict['text'] = clean_tweet_text(tweet_text)

            my_dict['user'] = username


            #add the temporary dictionary into the list

            my_list.append(my_dict)

        

        return my_list

    

    except IOError:


        print(f"Could not open file {tweet_file_name}!")

        return []


#This funciton analyzes and returns a dictionary

def make_report(tweet_list, keyword_dict):


    my_dict = {}


    #this is the number of all tweets

    num_tweets = len(tweet_list)

    my_dict["num_tweets"] = num_tweets


    #this is the number of retweers with at least 1

    num_retweet = 0

    for i in tweet_list:

        if i['retweet'] > 0:

            num_retweet += 1

    my_dict["num_retweet"] = num_retweet


    #this is number of tweets with at least 1 like/favourite

    num_favorite = 0

    for i in tweet_list:

        if i["favorite"] > 0:

            num_favorite += 1

    my_dict["num_favorite"] = num_favorite



    #this is avarage sentiment of tweets

    temp = 0

    for i in tweet_list:

        if num_tweets == 0:

            my_dict["avg_sentiment"] = "NAN"

        else:

            #call the function to calculat the setiment score for each sentence

            temp += calc_sentiment(i["text"], keyword_dict) 


    #divide that number by the number of tweets

    avg_sentiment = temp / num_tweets

    my_dict["avg_sentiment"] = round(avg_sentiment, 2)


    #this is avarage number of favorites

    temp2 = 0

    for i in tweet_list:

        if num_favorite == 0:

            my_dict["avg_favorite"] = "NAN"

        else:

            #check if the tweet has at least 1 favorite

            if i["favorite"] > 0:

                temp2 += calc_sentiment(i["text"], keyword_dict) 


    #calculat ethe avarage score by dividing the sentiment by the number of favorited tweets

    avg_favorite = temp2 / num_favorite

    my_dict["avg_favorite"] = round(avg_favorite, 2)


    #this is avarage number of retweets

    temp3 = 0

    for i in tweet_list:

        if num_tweets == 0:

            my_dict["avg_retweet"] = "NAN"

        else:

            #check if the tweets as at least 1 retweet

            if i['retweet'] > 0:

                #call the sentiment function at i to calculate the score

                temp3 += calc_sentiment(i["text"], keyword_dict) 

    

    #divide the total score by number of retweets to get avg

    avg_retweet = temp3 / num_retweet

    my_dict["avg_retweet"] = round(avg_retweet, 2)

        

    #this is number of tweets that are classified as negative, posotive and neutral

    num_negative = 0

    num_positive = 0

    num_neutral = 0

    for i in tweet_list:

        temp = calc_sentiment(i["text"], keyword_dict)

        if classify(temp) == "negative":

            num_negative += 1

        elif classify(temp) == "positive":

            num_positive += 1

        elif classify(temp) == "neutral":

            num_neutral += 1

    

    #add all values to the dicitonary

    my_dict["num_negative"] = num_negative

    my_dict["num_neutral"] = num_neutral

    my_dict["num_positive"] = num_positive


    #this will handle avg sentiment score of countires

    country_avg_score = {}

    country_tweet_dict = {}


    #make a sperate dicitonary of all the countries and all the tweets from those countries

    for tweet in tweet_list:

        if tweet["country"] not in country_tweet_dict.keys():

            country_tweet_dict[tweet["country"]] = [tweet] 

        else:

            country_tweet_dict[tweet["country"]].append(tweet)

    

    #make a sperate dicitonary of all the countries and their avg sentiment socres


    temp_score = 0

    avg = 0


    for country in country_tweet_dict:

        tweet_list = country_tweet_dict[country]

        for tweet in tweet_list:

            temp_score += calc_sentiment(tweet["text"], keyword_dict)

        avg = temp_score / len(tweet_list)

        country_avg_score[country] = avg


    #sort the values from highest to lowest

    country_avg_score = sorted(country_avg_score.items(), key=lambda x:x[1], reverse=True)


    counter = 0

    temp_string = ""

    for i in range(len(country_avg_score)):

        if country_avg_score[i][0] == "NULL" or country_avg_score[i][0] in temp_string:

            continue

        else:

            temp_string = temp_string + country_avg_score[i][0] + ", "

        counter += 1

        if counter == 5:

            break


    #if stirng ends wiht a comma, slice it out

    if temp_string.endswith(", "):

        temp_string = temp_string[:-2]

    my_dict["top_five"] = temp_string



    return my_dict






#this dunction will generate a .txt file of the report of all the statistics

def write_report(report, output_file):


    try:


        #open a new file with the user specified name

        file = open(output_file, "w") 


        #write all the info using the .write function and the report dictionary

        file.write("Average sentiment of all tweets: " + str(report["avg_sentiment"]) + "\n")

        file.write("Total number of tweets: " + str(report["num_tweets"]) + "\n")

        file.write("Number of positive tweets: " + str(report["num_positive"]) + "\n")

        file.write("Number of negative tweets: " + str(report["num_negative"]) + "\n")

        file.write("Number of neutral tweets: " + str(report["num_neutral"]) + "\n")

        file.write("Number of favorited tweets: " + str(report["num_favorite"]) + "\n")

        file.write("Average sentiment of favorited tweets: " + str(report["avg_favorite"]) + "\n")

        file.write("Number of retweeted tweets: " + str(report["num_retweet"]) + "\n")

        file.write("Average sentiment of retweeted tweets: " + str(report["avg_retweet"]) + "\n")

        file.write("Top five countries by average sentiment: " + str(report["top_five"]))


        print(f"Wrote report to {output_file}")


    except IOError as e:


        print(f"Could not open file {output_file}")
