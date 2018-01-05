import pandas as pd
import re

##### Requirement by prof: don't use SKLearn. Code everything on your own.

# This program evaluates the given .csv file.
# for fun uncomment the #testString on line 105.

#######################################################
# 1 is negative
# 3 is neutral
# 5 is positive
#######################################################

'''
Given a list of strings, the follwoing subroutine outputs the frequency of
each item in the list.
input: list
output: dictionary

example: input: ['a', 'a', 'b']
output: {('a':2), ('b':1)}
'''
def frequencyCounter(ArrayOfStrings):
    #print(type(ArrayOfStrings[2]))
    dictionary = {}
    regex = re.compile('[^a-zA-Z$]')
    for items in ArrayOfStrings:
        temp = items.split()
        for i in temp:
            i = regex.sub('', i)
            if i not in dictionary.keys():
                 dictionary[i] = 1
            else:
                dictionary[i] += 1
    return(dictionary)


'''
The following subroutine is called by the determinePolarity subroutine.
This simply calculates the probability of words according to Naive Bayes
Classifier.
input: dictionary, size of dictionary, differentWords in dictionary, test string
output: probability of the words occuring. It'a a single float variable.
'''
def classifierForPolarity(dictionary, totalSize, differentWords, strings):
    regex = re.compile('[^a-zA-Z$]')
    wordList = strings.split()
    divider = differentWords + totalSize
    count = 1
    probabilityList = []
    for i in wordList:
        i = regex.sub('', i)
        if str(i) in dictionary.keys():
            temp = dictionary[str(i)]
            count += int(temp)
        else:
            count = count
        classify = count / divider
        probabilityList.append(classify)
        classify = 0
        count = 1
    totalProb = 1
    for i in probabilityList:
        totalProb = totalProb * i
    return(totalProb*0.5)


'''
This subroutine calculates the total number of different words in the dictionary
input: dictionary
output: count, which is an int variable.
'''
def totalNumberOfDifferentWords(dictionary):
    count = 0
    for i in dictionary.values():
        count = count + int(i)
    return count

'''
This subroutine is called by the main program. It uses all available lists,
dictionaries and other data to determine the polarity of a tweet.
Probability of a tweet is calculated by the classifierForPolarity
subroutine. Both the dictionaries are used for this part.
Depending on which probability is larger, polarity of the tweet is determined.
If there is 50% or more similarity between the probabilities,
polarity is determined as neutral.
input: dictionries, lists, int variables
output: list
'''
def determinePolarity(dictionary1, sizeOfDictionary1, differentWordsIn1,
            dictionary5, sizeOfDictionary5, differentWordsIn5, arrayTestData):

    result = []
    '''
    The following is a custom list to add bias to probability. If a match is
    found, 0.1 is added to the corresponding positive or negative probability.
    '''
    positiveList = ['happy', 'rocks', 'awesome', 'cool', 'good', 'hilarious',
                                        'award', 'love', 'great', 'wonderful']
    negativeList = ['sucks', 'hideous', 'disaster', 'sad', 'no', 'not',
                                            'waste', 'miserable', 'annoying']
    regex = re.compile('[^a-zA-Z$]')

    #testString = input("Type something here to test:")
    for i in arrayTestData:
        testString = str(i)
        prob1 = classifierForPolarity(dictionary1, sizeOfDictionary1,
                                                differentWordsIn1, testString)
        prob5 = classifierForPolarity(dictionary5, sizeOfDictionary5,
                                                differentWordsIn5, testString)

        testWordList = testString.split()

        # bias has been added to probability if there was a match with the
        # lists positiveList and negativeList.
        for i,j in enumerate(testWordList):
            j = regex.sub('', j)
            for k,l in enumerate(positiveList):
                if j==l:
                    # tuning parameter
                    prob5 += 0.1
            for m,n in enumerate(negativeList):
                if j == n:
                    # tuning parameter
                    prob1 += 0.1

        statement = ""
        polarity = 0

        if prob1> prob5:
            polarity = 1
            statement = "Negative"
        else:
            polarity = 5
            statement = "Positive"

        # tuning parameter
        # adjust threshold to choose polarity 3 (neutral)
        if prob1/prob5*100 >50:
            if prob5/prob1*100 > 50:
                statement = "neutral"
                polarity = 3

        prob1 = 0
        prob5 = 0

        result.append(polarity)

    return(result)


'''
The following program remove the most common words with similar chance of
occuring in both dictionries. The program returns a list.
input: dictionries
outout: list
'''
def removeMostCommonWords(dictionary1, dictionary5):
    newDic1 = {}
    newDic5 = {}

    for i,j in dictionary1.items():
        if int(j)>25000:
            newDic1[i] = j


    for i,j in dictionary5.items():
        if int(j)>25000:
            newDic5[i] = j


    strList = []
    for i,j in newDic1.items():
        for k,l in newDic5.items():
            if i == k:
                temp1 = int(j)
                temp2 = int(l)
                if temp1/temp2*100 > 99:
                    strList.append(i)


    strList.remove('not')
    strList.remove('like')

    return(strList)


#the main program starts here
'''
The following part process the training data in a Panda dataframe.
In the training data column = 0 represents the polarity of the tweet.
Column = 3 represents the tweet.
Columns = {1,2} has been ignored as they do not provide useful information in
our program. Panda dataframe has been converted to array for easy processing.
'''
pandaData = pd.read_csv('twitter_csci581.csv')
chosenColumns = [0,3]
arrayData = pandaData.as_matrix(columns = pandaData.columns[chosenColumns])

'''
The following part processes the evaluation data.
Only column = 2 has been chosen, since other data is irrelevant.
Data has been converted to array for faster processing.
'''
pandaTestData = pd.read_csv('evaluation_csci581.csv')
chosenTestColumn = [2]
arrayTestData = pandaTestData.as_matrix(columns =
                                    pandaTestData.columns[chosenTestColumn])


'''
polarity1 and polarity5 represents two lists that collects the tweets
with polarity 1 and polarity 5 reslectively.
'''
polarity1 = []
polarity5 = []

for i,j in enumerate(arrayData):
    if j[0] == 1:
        polarity1.append(j[1])
    else:
        polarity5.append(j[1])

'''
The following code segment counts the frequency of the words.
input type: list
output type: dictionary
'''
dictionary1 = frequencyCounter(polarity1)
dictionary5 = frequencyCounter(polarity5)

'''
The following code segment counts the total number of words in
each dictionary.
'''
sizeOfDictionary1 = totalNumberOfDifferentWords(dictionary1)
sizeOfDictionary5 = totalNumberOfDifferentWords(dictionary5)

'''
The following code segment counts the total number of different words in
each dictionary.
'''
differentWordsIn1 = len(dictionary1)
differentWordsIn5 = len(dictionary5)

'''
The following is a list that contains the most common words
in dictionary1 and dictionary5. This list was created with the purpose
of removing most common words that exist in both the dictioanries.
Since words with high frequency, but 90% common to both dictionaries do not
help in imroving the accurcy. These words only prvide a hgh bias while
determing probablity. These wrods have been removed from the dictionaries.
For example: [it, the, of, there]. These words have high frequency, but not
much useful in determing probablity.

'''

'''
# this part of the code has been muted

strList = removeMostCommonWords(dictionary1, dictionary5)
for i in strList:
    temp = str(i)
    dictionary1.pop(temp, N1)
    dictionary5.pop(temp, N1)
'''

# active code starts again from here
'''
Thie is the main part of the program.
It supplies all lists, dictionries, variables to the determinePolarity program,
and saves the result in the list variable "result."
'''
result = determinePolarity(dictionary1, sizeOfDictionary1, differentWordsIn1,
        dictionary5, sizeOfDictionary5, differentWordsIn5, arrayTestData)

print(result)

'''
The following code segment outputs "result" in a csv file.
'''
with open('output.csv','w') as out_file:
  for i in result:
    print(i, file=out_file)


#dictionary1 = sorted(dictionary1.items(), key=lambda x:x[1], reverse = True)
