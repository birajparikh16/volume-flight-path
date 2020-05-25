from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from stop_words import get_stop_words
en_stop = get_stop_words('en')

import re

import warnings
warnings.filterwarnings("ignore")


"""
Preprocessed methods include the following:
 - Convert to Lowercase
 - Decontract the words
 - Remove stopwords
 - Remove Digits
 - Remove special characters
 - Remove single characters
 - Remove Emoji's
 - Remove Whitespace
"""

# Lowercase
def lowercase(review):
    """ Method to convert the review to lowercase

    Args: 
        review: string
    Returns:
        review: string converted to lowercase
    """
    return review.lower()

# Decontract the words in the string
def decontracted(review):
    """ Method to decontract the words from the review string

    Args: 
        review: string
    Returns:
        review: string decontracted
    """
    review = re.sub(r"won't", "will not", review)
    review = re.sub(r"can\'t", "can not", review)
    review = re.sub(r"n\'t", " not", review)
    review = re.sub(r"\'re", " are", review)
    review = re.sub(r"\'s", " is", review)
    review = re.sub(r"\'d", " would", review)
    review = re.sub(r"\'ll", " will", review)
    review = re.sub(r"\'t", " not", review)
    review = re.sub(r"\'ve", " have", review)
    review = re.sub(r"\'m", " am", review)
    return review

# Remove stopwords
def remove_stopwords(review):
    """ Method to remove the stopwords from the review string

    Args: 
        review: string
    Returns:
        review: stopwords removed
    """
    # https://gist.github.com/sebleier/554280
    review = ' '.join(e for e in review.split() if e not in en_stop)
    return review.strip()


# Remove digits from the string
def remove_digits(review):
    """ Method to remove whitespace from the review string

    Args: 
        review: string
    Returns:
        review: whitespace removed

    Example: 
    review: "This must not b3 delet3d, but the number at the end yes 134411"
    result: "This must not b3 delet3d, but the number at the end yes"
    """
    review = re.sub(r"\b\d+\b", "", review)
    return review.strip()

# Remove Special Characters
def remove_special_character(review):
    """ Method to remove the special characters from the review string

    Args: 
        review: string
    Returns:
        review: special characters removed
    """
    review = re.sub("[^A-Za-z]+", " ", review)
    return review.strip()

# Remove a single characters
def remove_single_character(review):
    """ Method to remove a single characters from the review string

    Explantion: Sometimes removing punctuation marks, such as an apostrophe, results in a single character which has 
    no meaning. For instance, if you remove the apostrophe from the word Jacob's and replace it with space, the resultant 
    string is Jacob s. Here the s makes no sense. Such single characters can be removed using regex as shown below:

    Args: 
        review: string
    Returns:
        review: a single characters removed

    """
    review = re.sub(r"\s+[a-zA-Z]\s+", " ", review)
    return review.strip()

def remove_emoji(review):
    """ Method to remove the icons or emoji's characters from the review string

    Args: 
        review: string
    Returns:
        review: emoji's removed
    """
    # https://stackoverflow.com/a/49146722/330558
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    review = emoji_pattern.sub(r'', review)
    return review.strip()

# Remove whitespace from start and end of a string
def remove_whitespace(review):
    """ Method to remove whitespace from the review string

    Args: 
        review - string
    Returns:
        review string - whitespace removed
    """
    review = review.strip()   # remove the whitespace from the start and end of the string
    review = re.sub(r"\s+"," ", review, flags = re.I) # remove the whitespace between the string
    return review