import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cleanup import dataCleanup #Function for cleaning up data is in cleanup module

pd.set_option('display.max_columns', None)    

#Read the csv file into a data frame
dog_bites = pd.read_csv('dog_bites.csv', usecols=['UniqueID', 'DateOfBite', 'Breed', 'Age', 
                                                  'Gender', 'SpayNeuter', 'Borough'])
#   This dataset examines around 20,000 dog-bite incidents in New York City that took place
#   between the years 2015 and 2021.  It features important columns that could
#   help us identify correlations and potential causes of these incidents, such as Breed, 
#   Age, Gender, and whether or not the dog was spayed/neutered.

#Data inspection
dog_bites.head(10)
dog_bites.tail(10)
dog_bites.info()
dog_bites.describe()
dog_bites.dtypes
dog_bites.shape

#Call function to cleanup data
dog_bites = dataCleanup(dog_bites)

#Add a column (bool) indicating whether or not the dog was a pitbull in any way
dog_bites['Pitbull/Partial Pitbull'] = (dog_bites['Breed'].str.contains('(?i)Pit Bull') |
                                        dog_bites['Breed'].str.contains('(?i)Pitbull'))


#Visualizations
#Line graph showing number of incidents over the years
dog_bites.Year.value_counts().sort_index().plot(
    kind='line', 
    xlabel='Year',
    ylabel='# of Bites',
    title='Number of bites over time',
    color='red'
)

#Histogram showing age frequencies of the incidents
known_ages = dog_bites.drop(dog_bites[dog_bites.Age == 'U'].index)
known_ages['Age'] = known_ages['Age'].astype(int).plot(
    kind='hist', 
    xlabel='Age',
    xticks=np.arange(0, 22, step=2),
    title='Frequency of ages',
    color='limegreen'
)

#Bar graph comparing male to female dog bite incidents
known_genders = dog_bites.drop(dog_bites[dog_bites.Gender == 'U'].index)
known_genders.loc[known_genders['Gender'] == 'M'] = 'Male'
known_genders.loc[known_genders['Gender'] == 'F'] = 'Female'
known_genders['Gender'].value_counts().plot(
    kind='bar', 
    color=['blue', 'magenta'],
    title='Male vs. Female Bites',
    rot=0
)

#Pie chart demonstrating how many incidents consisted of some form of pitbull
pitbulls = pd.DataFrame(dog_bites)
pitbulls['Breed'] = pitbulls['Pitbull/Partial Pitbull'].apply(
    lambda x: 'Pitbull/Partial Pitbull' if (x == True) else 'Not Pitbull')
pitbulls['Breed'].value_counts().plot(kind='pie')

#Bar graph demonstrating the amount of incidents per borough
dog_bites['Borough'].value_counts().sort_values().plot(kind='barh', 
                                         color=['brown', 'purple', 'red', 
                                                'green', 'orange', 'blue'])  


#Questions
# How has the number of bite incidents changed over the years? Has it gotten
# better or worse? Did some event cause the number of incidents to rise/drop significantly?
dog_bites.Year.value_counts().sort_index().plot(kind='line', color='red')
'''It appears that the data fluctuates over the years, but in 2020, the amount of incidents
    dropped significantly. This is likely due to the fact that the Coronavirus pandemic 
    was rampant and at large during this year, and people weren't out and about as much.
    Thus, less dog bites were recorded'''
    
# Which of the boroughs had the highest number of incidents? Of those incidents, how many
# dogs were spayed/neutered?
borough = dog_bites['Borough'].value_counts().idxmax()
highestBorough = dog_bites[dog_bites['Borough'] == borough]
highestBorough[highestBorough['Spay/Neuter'] == True].count()
'''The borough with the highest number of incidents was Queens. It appears that in Queens,
    1,639 of the dogs were spayed/neutered'''

# Which borough had the lowest number of incidents? What was the most frequent age of
# the dog for the incidents
borough = dog_bites[dog_bites['Borough'] != 'Other'].Borough.value_counts().idxmin()
lowestBorough = dog_bites[dog_bites['Borough'] == borough]
lowestBorough[lowestBorough['Age'] != 'U'].Age.value_counts().idxmax()
'''The borough with the lowest number of incidents was Staten Island. It appears that in
    Staten Island, the most common age was 2'''
    
# Which gender of dog was responsible for most of the incidents? Of those incidents,
# how many were spayed/neutered?
gender = dog_bites[dog_bites['Gender'] != 'U'].Gender.value_counts().idxmax()
higherGender = dog_bites[dog_bites['Gender'] == gender]
higherGender[higherGender['Spay/Neuter'] == True].count()
'''It appears that male dogs were more responsible for dog bites than females. 
    Among the male dogs, it appears that 4,082 of them were neutered'''

# In which months did bites most frequently occur? In other words, is there a correlation
# between the potential weather during these months and the number of bites?
dog_bites['Month'].value_counts()
'''After viewing the data presented via the command above, it appears that dog bites were
    most frequent in July, August, and June, in that order. Such results indicate that 
    bites are more frequent during warmer weather that is common during these months, as 
    both people and dogs are out more. Additionally, the months with the fewest bites were 
    January, February, and December. As the weather is typically colder during these months,
    dog bites are less likely to occur'''

# What percentage of total incidents were either a pitbull or partially a pitbull?
numPitbulls = dog_bites[dog_bites['Pitbull/Partial Pitbull'] == True]['Breed'].count() 
allDogs = dog_bites['Pitbull/Partial Pitbull'].count()
print(str(int(numPitbulls / allDogs * 100)) + '%')
'''Around 24% of all dog bites consisted of a dog that was a pitbull or partially 
    a pitbull. That's nearly a quarter of all incidents'''

    
#Correlation Analysis
ageFreq = dog_bites['Age'].value_counts().rename_axis('Age').reset_index(name='Bites')
ageFreq = ageFreq.drop(ageFreq[ageFreq['Age'] == 'U'].index).astype(int)

x = ageFreq['Age']
y = ageFreq['Bites']
a, b = np.polyfit(x, y, 1)
ageFreq.plot(
    kind='scatter',
    x='Age',
    y='Bites',
    title='Effect of age on number of bites',
    color='red'
)
plt.xticks(np.arange(0, 22, step=2))
plt.plot(x, a*x+b)

r = np.corrcoef(x, y)
r[0, 1]
'''Based on the correlation analysis of the dog_bites data frame, it appears that a negative
    correlation exists between the age of the dog and the number of bites that occur. 
    Although correlation does not equal causation, one can use this correlation to infer
    that the older a dog is, the less likely it is to bite someone'''