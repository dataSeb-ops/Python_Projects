#!/usr/bin/env python
# coding: utf-8

# # Analyzing Mobile App Data
# This project explores mobile app data from Google Play and the App Store.
# The goal is to help developers understand what type of apps are likely to attract more users on both platforms.
# 
# ## Setting up and exploring data

# In[1]:


# FUNCTIONS FOR ACCESSING/VIEWING DATA

# function to open datasets
def open_dataset(file_name, header=True):        
    opened_file = open(file_name)
    from csv import reader
    read_file = reader(opened_file)
    data = list(read_file)
    
    if header:
        return data[0], data[1:]
    
    return data


# function to explore datasets
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[2]:


# EXPLORE DATA

apple_header, apple_data = open_dataset('data_raw/AppleStore.csv')
ggle_header, ggle_data = open_dataset('data_raw/googleplaystore.csv')

print(apple_header)
print('\n')
explore_data(apple_data, 0, 3)

print(ggle_header)
print('\n')
explore_data(ggle_data, 0, 3)

explore_data(apple_data, 1, 1, True)
explore_data(ggle_data, 1, 1, True)


# ## Data cleaning
# ### Removing entries with missing information

# In[3]:


# DATA CLEANING

print(ggle_data[10472])
del ggle_data[10472] # removed entry with missing category       
print(ggle_data[10472])


# ### Removing duplicate entries
# The Google Play dataset has duplicate entries for some apps, so we need to remove these.
# Let's examine some of the duplicates:

# In[4]:


# record which apps have duplicate entries
dup_apps = []
unique_apps = []

for app in ggle_data:
    name = app[0]
    if name in unique_apps:
        dup_apps.append(name)
    else:
        unique_apps.append(name)
        
print('Number of duplicate apps: ', len(dup_apps))
print('\n')
print('Examples of apps with duplicates: ', dup_apps[:10])


# In removing duplicate entries, we want to keep the most recent entry. To achieve this, we'll keep the entry with the highest number of reviews for each app since this entry should be the most recent.
# 
# First we'll create a dictionary to **store the highest number of reviews for each app.**

# In[5]:


# record highest number of reviews for each app
reviews_max = {}

for app in ggle_data:
    name = app[0]
    n_reviews = float(app[3])
    
    # check if app name is already keyed, and if the current number of
        # reviews is greater than the recorded number of reviews
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    
    # if the app name has not been keyed yet, then add it
    elif name not in reviews_max:
        reviews_max[name] = n_reviews


# Now that we know the number of reviews for each entry that we want to keep, we can **select the entries with the corresponding number of reviews.**
# 
# To do this, we'll cycle through the Google dataset and see if the entry has the max number of reviews for that app. If it does, then we'll **add it to our cleaned dataset, and then record that we've added it**.

# In[6]:


# create dataset with no duplicate app entries

android_clean = [] # stores cleaned dataset
already_added = [] # stores names of apps in cleaned dataset

for app in ggle_data:
    name = app[0]
    n_reviews = float(app[3])
    
    # check if entry has max number of reviews and has not been recorded
        # in clean dataset
    if n_reviews == reviews_max[name] and name not in already_added:
        android_clean.append(app)
        already_added.append(name)
        

print('Cleaned Google dataset should have 9,659 rows.')
print('\nActual number of rows: ', len(android_clean))


# ### Removing non-English app
# Our company's audience is English-speaking, so there's no need to look at non-English apps.
# 
# We'll exclude these apps from the dataset by checking if the app name has any characters that are not commonly used in English text. The commonly used English characters have ASCII values less than or equal to 127. If the app name does not contain characters with ASCII values greater than 127, then it likely is an English-speaking app.
# 
# However, some English app names have emojis or trademark symbols, which have ASCII values greater than 127. If we exclude these app, then we will lose a lot of valuable data. Therefore, our code should check if the app name has **more than 3 characters whose ASCII value is greater than 127.**

# In[7]:


# Function to check if string is in English

def isEnglish(string):
    
    # count number of non-English characters
    n_nonEnglish = 0
    
    for char in string:
        if ord(char) > 127: # if ASCII value is greater than 127
            n_nonEnglish += 1 # then increment non-English char count
        
    if n_nonEnglish > 3:
        return False # if more than 3 non-Eng chars, then string is non-English
    
    return True

print(isEnglish('Docs To Go™ Free Office Suite'))
print(isEnglish('Instachat 😜'))
print(isEnglish('爱奇艺PPS -《欢乐颂2》电视剧热播'))


# As demonstrated, the function above achieves the desired effect of filtering out English and non-English app names based on the selected criterion.
# 
# Now we'll remove the non-English apps from our dataset.

# In[8]:


# new list to store only English apps

android_english = []

# for each app, if name is English, add to new dataset
for app in android_clean:
    name = app[0]
    
    if isEnglish(name):
        android_english.append(app)
        
print('\nNumber of English apps: ', len(android_english))


# ### Isolating free English apps
# Now that we've removed duplicate entries, removed entries with missing data, and removed non-English apps, we want to isolate the free apps.
# 
# We'll do this by checking if the price of the app is equal to 0.

# In[9]:


# for each English app, if price is 0, add to new dataset

android_freeEng = []

for app in android_english:
    price = app[7]
    
    if price == '0':
        android_freeEng.append(app)
        
print('\nNumber of free English apps: ', len(android_freeEng))


# ## Analysis
# Now that we have a clean dataset, we can begin our analysis to help developers understand what type of apps are likely to attract more users on both platforms.
# 
# Our validation strategy for an app has three steps:
# 1. Build a minimal Android version of the app, and add it to Google Play.
# 2. If the app has a good response from users, we develop it further.
# 3. If the app is profitable after six months, we build an iOS version of the app and add it to the App Store.
# 
# To do this analysis, let's start by looking at the most common app genres for each platform by creating frequency tables for the genres.
# 
# ### Most common app genres

# In[10]:


# function to generate frequency tables for any dataset
def freq_table(dataset, idx):
    ft = {}
    num = len(dataset)
    
    # for each row in dataset, if element in selected column is already
        # in the freq table, then increment the percentage in freq table
        # if element not in freq table, then record the first instance
    for row in dataset:
        value = row[idx]
        
        if value in ft:
            ft[value] += 1 * 100 / num
        else:
            ft[value] = 1 * 100 / num
            
    return ft


# function to display frequency tables
def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1] + ':', entry[0])
        
        
display_table(android_freeEng, 1) # ft for Category column in Google Play data
print('\n')
display_table(android_freeEng, 9) # ft for Genres column in Google Play data
print('\n')
display_table(apple_data, 12) # ft for prime_genre column in App Store data


# For free English speaking apps in the **App Store**, Games is by far the most common genre, covering over 50% of all the apps. (This doesn't necessarily imply that this genre has the largest number of users.)
# 
# The most common genres in the **Google Play** store is a little less cut and dry. The genres are much more evenly distributed across the free English apps. Games are common, but Family apps are the most common, and Tools apps are comparable in number.
# 
# Bascially, **apps designed for fun and entertainment dominate the App Store**, while **Google Play shows a more balanced landscape of both practical and fun apps.**
# 
# ### Most popular app genres
# The analysis in the previous section tells us how *common* each genre is, but we want to know how *popular* each genre is so that we can ***select an app genre that will be popular on both platforms***. To do this, we'll **calculate the average number of installs for each app genre.** (The Google Play dataset provides this information, but the App Store dataset does not. Instead, we can use the the total number of user ratings as a proxy for number of installs.

# In[11]:


# proxy avg num installs by avg num of reviews for Apple dataset

apple_genre_ft = freq_table(apple_data, 12) # get unique genres in Apple dataset
apple_genre_avgReviews = {} # dictionary to store avg num reviews per app for each genre

# for each unique genre
for genre in apple_genre_ft:
    genre_totReviews = 0 # create variable to store tot num reviews
    n_genre = 0 # variable to store number of apps in genre

    # for each app in the Apple dataset
    for app in apple_data:
        app_genre = app[12] # get genre for that app
        
        # check if the app genre is equal to the genre in question
        if app_genre == genre:
            n_genre += 1 # if yes, increment genre app count
            n_reviews = float(app[6]) # get num reviews for that app
            genre_totReviews += n_reviews # sum tot num genre reviews
                
    # calculate avg num reviews per app in genre
    apple_genre_avgReviews[genre] = genre_totReviews / n_genre
    #print(genre + ':', apple_genre_avgReviews[genre])
    
apple_genre_avgReviews_sorted = dict(sorted(apple_genre_avgReviews.items(), key=lambda x: x[1], reverse=True))
print('App Store genres ranked by popularity: \n')
n = 0
for genre in apple_genre_avgReviews_sorted:
    n += 1
    print(str(n) + '. ' + genre + ':', apple_genre_avgReviews_sorted[genre])
            


# In[12]:


# avg num of installs per app for Google Play dataset

ggle_genre_ft = freq_table(android_freeEng, 1) # get unique genres in Google dataset
ggle_genre_avgInstalls = {} # dictionary to store avg num reviews per app for each genre

# for each unique genre
for genre in ggle_genre_ft:
    genre_totInstalls = 0 # create variable to store tot num installs
    n_genre = 0 # variable to store number of apps in genre

    # for each app in the Google Play dataset
    for app in android_freeEng:
        app_genre = app[1] # get genre for that app
        
        # check if the app genre is equal to the genre in question
        if app_genre == genre:
            n_genre += 1 # if yes, increment genre app count
            s_installs = app[5]
            n_installs = int(s_installs.replace(",", "").replace("+", "")) # get num installs for that app
            genre_totInstalls += n_installs # sum tot num genre installs
                
    # calculate avg num installs per app in genre
    ggle_genre_avgInstalls[genre] = genre_totInstalls / n_genre


ggle_genre_avgInstalls_sorted = dict(sorted(ggle_genre_avgInstalls.items(), key=lambda x: x[1], reverse=True))
print('Google Play genres ranked by popularity: \n')
n = 0
for genre in ggle_genre_avgInstalls_sorted:
    n += 1
    print(str(n) + '. ' + genre + ':', ggle_genre_avgInstalls_sorted[genre])
            


# One issue with this data is that it's not very precise. The Google Play dataset gives us the number of installs rounded down to the nearest thousand. For example, it lists 10,000+ or 5,000,000+ installs rather than precise numbers. However, it is adequate for our analysis. We only need an idea of which genres will attrach the most users.
# 
# ### Comparison between genre popularity across platforms
# Now that we have the genres sorted by most popular, let's compare the top ten genres for each platform.

# In[13]:


dict1 = {f"A{i}": i for i in range(1, 21)}
dict2 = {f"B{i}": i for i in range(1, 21)}

# Convert keys to lists
keys1 = list(apple_genre_avgReviews_sorted.keys())
keys2 = list(ggle_genre_avgInstalls_sorted.keys())

print('           Top Ten Genres by Popularity')
print(f"{'Rank.':<6} {'App Store':<20} | {'Google Play'}")
print("-" * 55)

# Loop through first 10 only
for i, (k1, k2) in enumerate(zip(keys1[:10], keys2[:10]), start=1):
    print(f"{i}.     {k1:<20} | {k2}")


# ## Discussion and Recommendation
# In this project, we cleaned and analyzed data for mobile apps from the Google Play and App Store platforms. Using the metric of average number of installs per app for each genre, we can draw some conclusions about the popularity of each genre for each market. 
# 
# Social networking apps are popular on both platforms, but the level of involvement in creating a social app is beyond the scope of our company.
# Music is popular for the App Store, but not much so on Google Play. Same for Reference, Weather, and Shopping apps.
# However, the Photo & Video and Travel genres from the App Store show promise. Video Players, Photography, and Travel and Local apps are all popular on Google Play.
# 
# In light of this analysis, it is recommended to develop a **travel / local**, as this is likely to be profitable in both markets. The app could show users upcoming events that are happening in their area. It could add features such as a map to show popular events within a radius from their current location, possibly even tying in travel/drive/flight durations. This would also easily enable revenue from ads as they could be seemlessly tied in for nearby food and drink.

# In[ ]:





# In[14]:


import nbformat
from nbconvert import PythonExporter

# Replace with your notebook filename
notebook_filename = 'mobile_app_analysis.ipynb'
script_filename = 'mobile_app_analysis.py'

# Load the notebook
with open(notebook_filename, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# Convert to Python script
exporter = PythonExporter()
source, _ = exporter.from_notebook_node(nb)

# Save to .py file
with open(script_filename, 'w', encoding='utf-8') as f:
    f.write(source)

print(f"Saved Python script as {script_filename}")

