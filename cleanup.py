import pandas as pd

def dataCleanup(dog_bites):
    #Rename
    dog_bites.rename(columns={'UniqueID': 'Incident ID', 'DateOfBite': 'Date', 
                              'SpayNeuter': 'Spay/Neuter'}, inplace=True)

    #Modify Incident ID and set it as index
    dog_bites.loc[12383:22662, 'Incident ID'] = dog_bites.loc[12383:22662, 'Incident ID'] + 12383
    dog_bites.set_index('Incident ID', inplace=True)

    #Break up date into month and year
    get_month = lambda s: s.split(' ')[0]
    get_year = lambda s: s.split(' ')[2]

    months = dog_bites['Date'].apply(get_month)
    years = dog_bites['Date'].apply(get_year)

    dog_bites.drop('Date', axis=1, inplace=True)
    dog_bites['Month'] = months
    dog_bites['Year'] = years

    #Fill NaN values for these columns
    dog_bites.Breed.fillna('UNKNOWN', inplace=True)
    dog_bites.Age.fillna('U', inplace=True)

    #Cleanup Age
    for i in range(2, 0, -1):
        dog_bites.loc[dog_bites['Age'].str.contains('Y') | dog_bites['Age'].str.contains('y'), 
                      'Age'] = dog_bites['Age'].str[:i]
        dog_bites.loc[dog_bites['Age'].str.contains('\.', na=False), 'Age'] = dog_bites['Age'].str[:i]
        
    dog_bites.loc[dog_bites['Age'].str.contains('M') | dog_bites['Age'].str.contains('m') | 
                  dog_bites['Age'].str.contains('W') | dog_bites['Age'].str.contains('w'),
                  'Age'] = '0'

    dog_bites.loc[dog_bites['Age'].str.contains(' ', na=False), 'Age'] = dog_bites['Age'].str[0]

    ageList = []
    for i in range(0, 21):
        ageList.append(str(i))
    ageList.append('U')

    return dog_bites[dog_bites['Age'].isin(ageList)]

#Miscellaneous code for finding issues
# dog_bites['Incident ID'].duplicated()
# dog_bites[dog_bites['Incident ID'] == 1]
# dog_bites.iloc[12382:12384]

# dog_bites['Age'][dog_bites['Age'].str.contains('Y') | dog_bites['Age'].str.contains('y')]

# dog_bites['Age'].tail(60)
# dog_bites['Age'].head(60)

# dog_bites.Age.value_counts()
# dog_bites.Age.value_counts().head(60)
# dog_bites.Age.value_counts().iloc[60:120]
# dog_bites.Age.value_counts().tail(60)
# dog_bites.Age.value_counts().tail(20)

# dog_bites[dog_bites['Age'].str.contains('\.', na=False)]

# dog_bites.Breed.value_counts()
# dog_bites.Gender.value_counts()
# dog_bites['Spay/Neuter'].value_counts()
# dog_bites['Pitbull/Partial Pitbull'].value_counts()