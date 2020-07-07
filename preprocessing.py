#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: Biraj Parikh

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from stop_words import get_stop_words
en_stop = get_stop_words('en')

import re
import pandas as pd

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

    Explantion: Sometimes removing punctuation marks, such as an apostrophe, results in a 
    single character which has no meaning. For instance, if you remove the apostrophe from 
    the word Jacob's and replace it with space, the resultant string is Jacob s. Here the 
    s makes no sense. Such single characters can be removed using regex as shown below:

    Args: 
        review: string
    Returns:
        review: a single characters removed

    """
    review = re.sub(r"\s+[a-zA-Z]\s+", " ", review)
    return review.strip()

# Remove Emoji's
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
    review = review.strip()  # remove the whitespace from the start and end of the string
    review = re.sub(r"\s+"," ", review, flags = re.I) # remove the whitespace between the string
    return review

# Creating new features based on user's review comment - Feature Engineering

# Condition feature
def conditions(review):

    """ Method to find keywords about conditions based on the reviewer comment or user info and creating a new feature called conditions
    
    Args: 
        review - string
    Returns:
        keyword - string value
    """
    
    if re.search(r"\bfungal\b|\bmalassezia\b|\bmalassezia folliculitis\b|\bpityrosporum folliculitis\b|\bfungal infection\b|\banti fungal\b|\banti fungals\b|\bitchy bumps\b|\bitching\b|\bitchy\b|\bitchiness\b|\bnizoral\b", review):
        return 'Fungal acne'
    elif re.search(r"\beczema\b|\bpsoriasis\b", review):
        return 'Eczema or psoriasis'
    elif re.search(r"\brosacea\b|\bred flush\b|\bred flushing\b|\bred cheeks\b|\bred cheek\b|\bflushed cheeks\b|\bflush cheek\b", review):
        return 'Rosacea'
    else:
        return 'Miscellaneous'

# Characteristics feature
def characterisitics(review, skintone):

    """ Method to find keywords about characterisitics based on the reviewer comment or user info and creating a new feature called characterisitics
    
    Args: 
        review - string
    Returns:
        keyword - string
    """
    
    if re.search(r"\bwhitehead\b|\bwhite bumps\b|\bwhiteheads\b|\bwhite heads\b|\bwhite head\b|\bcongestion\b|\bcongested\b", review):
        return 'Whiteheads'
    elif re.search(r"\bblackhead\b|\bblackheads\b|\bblack heads\b|\bblack head\b|\bblack dots\b|\bblack dot\b|\bdots on nose\b", review):
        return 'Blackheads'
    elif (skintone in ['Dark', 'Tan', 'Deep', 'Olive']) and re.search(r"\bPIH\b|\bpih\b|\bhyperpigmentation\b|\baccutane\b|\bscar\b|\bscarring\b|\bscars\b|\bpigment\b|\bmelanin\b|\bpigmented\b|\bpost acne\b|\bpost inflammatory\b|\bhyperpigmentation\b|\bpost-inflammatory hyperpigmentation\b", review):
        return 'PIH'
    elif (skintone in ['Porcelain', 'Light', 'Fair', 'Medium']) and re.search(r"\bPIE\b|\bpie\b|\bhyperpigmentation\b|\baccutane\b|\berythema\b|\bpost inflammatory erythema\b|\bred spot\b|\bred spots\b|\bscar\b|\bscarring\b|\bscars\b|\bpigment\b|\bpigmented\b|\bpost acne\b", review):
        return 'PIE'
    elif re.search(r"\bdry patches\b|\bdry patch\b|\bflaking\b|\bpeeling\b|\bbroken skin\b|\bdead skin\b", review):
        return 'Dry patches'
    elif re.search(r"\bsensitive\b|\bred\b|\birritated\b|\birritation\b|\birritate\b|\bsensitized\b", review):
        return 'Sensitive'
    elif re.search(r"\bvery oily\b|\bsuper oily\b|\bso oily\b|\bmore oily\b", review):
        return 'Very oily'
    elif re.search(r"\buneven tone\b|\buneven\b|\bunevenness\b|\bblotch\b|\bblotches\b|\bblotchy\b|\bpatch\b|\bpatches\b|\bpatchy\b", review):
        return 'Uneven tone'
    else:
        return 'Miscellaneous'


# Goals feature
def goals(review):

    """ Method to find keywords about goals based on the reviewer comment or user info and creating a new feature called goals
    
    Args: 
        review - string
    Returns:
        keyword value
    """
    
    if re.search(r"\bfade dark spots\b|\bfade\b|\bdark spots\b|\bmelanin\b|\bmelasma\b|\bage spots\b|\bsun spots\b|\buneven tone\b", review):
        return "Fade hyperpigmentation"
    elif re.search(r"\bbrighten\b|\bglow\b", review):
        return "Brighten"
    elif re.search(r"\boil control\b|\bcontrol oil\b|\bpore\b|\bpores\b|\bbig pores\b|\bminimize pores\b|\breduce pore size\b|\breduce pore\b|\breduce pores\b|\bsmaller pores\b|\bsmall pores\b", review):
        return "Oil control/pores"
    elif re.search(r"\bmoisturize\b|\bmoisturizing\b|\bhydrate\b|\bhydrating\b|\bthirsty\b|\bmoisture\b|\bwater\b|\brestore\b|\bskin barrier\b|\bnatural barrier\b|\bplump\b|\bheal\b", review):
        return "Hydrate"
    elif re.search(r"\bsoothe\b|\bsoothing\b|\bcalm\b|\bcalming\b|\breduce redness\b|\bless red\b|\bheal\b|\brelieve\b|\brefresh\b|\brebalance\b|\bbalance\b|\banti-inflammatory\b|\binflamed\b|\binflammation\b|\birritate\b|\birritated\b|\birritation\b|\birritant\b|\birritants\b", review):
        return "Soothe"
    elif re.search(r"\bblackheads\b|\bblack heads\b|\bblack head\b|\bblack dots\b|\bblack dot\b|\bnose\b|\bclear\b", review):
        return "Clear blackheads"
    elif re.search(r"\bwhiteheads\b|\bwhite bumps\b|\bwhite bump\b|\bbump\b|\bbumps\b|\bbumpy\b|\bno head\b|\bwhite heads\b|\bwhite head\b|\bclear\b|\bcongestion\b|\bcongested\b", review):
        return "Clear whiteheads"
    elif re.search(r"\bprotect\b|\bprotected\b|\bprotection\b|\bstrengthen\b|\bUV\b|\buv\b|\buv exposure\b|\bUV exposure\b|\bsunlight\b|\bsunscreen\b|\bSPF\b|\bspf\b|\bradicals\b|\bpollution\b|\bpollutant\b|\bpollutants\b|\bantioxidant\b|\bantioxidants\b", review):
        return "Protect"
    elif re.search(r"\bacne\b|\bacne-prone\b|\bacne prone\b|\bfight acne\b|\bclear\b", review):
        return "Fight acne"
    else:
        return "Miscellaneous"

    
# Acne Severity feature
def acne_severity(review):

    """ Method to find keywords about goals based on the reviewer comment or user info and creating a new feature called goals
    
    Args: 
        review - string
    Returns:
        keyword value
    """
    
    if re.search(r"\bmild acne\b|\bmild\b|\bfew pimple\b|\blittle pimples\b|\bsmall pimples\b|\bnew pimple\b|\bnew pimples\b|\bpimple\b", review):
        return 2
    elif re.search(r"\bintermediate acne\b|\bacne-prone\b|\bacne prone\b|\bhuge pimple\b|\bpimples\b", review):
        return 5
    elif re.search(r"\bsevere acne\b|\bnasty pimples\b|\bcluster\b|\bclusters\b|\bclustering\b|\bcongested\b", review):
        return 6
    else:
        return 0 

def preprocess_review_db(df):

    """ Method to apply all the preprocessing steps
    
    Args: 
        dataframe
    Returns:
        dataframe - with all preprocessing methods applied

    """
    
    # Renaming columns names to avoid whitespace
    df.columns = [label.replace(' ', '_') for label in df.columns]
    
    # Filling missing recommends value : If rating is on or below 3 then Recommends = False else True
    df.loc[df["IsRecommended"].isnull(), 'IsRecommended'] = df["Rating"].apply(lambda x: 'true' if x > 3 else 'false')

    # Removing rows where review is not given and skin type is not mentioned
    df.dropna(subset=['Name', 'ReviewText', 'SkinType'], inplace = True)

    # Applying a list of function on the reviewer comment
    func_list = [lowercase, decontracted, remove_digits, remove_single_character, remove_emoji, remove_whitespace]
    for func in func_list:
        df['ReviewText'] = df['ReviewText'].apply(func)

    # Feature Engineering
    # Skin based on conditions
    df['Condition'] = df['ReviewText'].apply(conditions)

    # Skin based on characteristics
    df['Characteristics'] = df.apply(lambda x: characterisitics(x['ReviewText'], x['SkinTone']), axis=1)

    # Skin based on goals
    df['Goals'] = df['ReviewText'].apply(goals)

    # Skin based on acne severity
    df['AcneSeverity'] = df['ReviewText'].apply(acne_severity)

    df = df.drop_duplicates().reset_index(drop = True)

    return df

def preprocess_product_db(df):

    df.rename(columns = {'Product Tags (product type, base skin type, fungal acne, eczema or psoriasis, rosacea, PIH, PIE, dry patches, sensitive, very oily, uneven tone, mild acne, intermediate acne, severe acne, fade hyperpigmentation, brighten, oil control/pores, hydrate, soothe, clear blackheads, clear whiteheads, protect, fight acne, fragrance-free, cruelty-free': 'ProductTags', 
                      'Brand Category (prestige, pharmacy, clinical, k+j beauty, indie)': 'BrandCategory', 'Preference Tags (Fragrance-free, Cruelty-free, Silicone/Paraben/Sulfate-free, Alcohol-free) + should add essential oil-free' : 'PreferenceTags',
                      'Brand': 'ProductBrand', 'Full Size Price': 'FullSizePrice', 'Trial available? (Y/N)': 'TrialAvailable',
                      'If trial (Y), price': 'TrialPrice'}, inplace = True)

    df["FullSizePrice"] = df["FullSizePrice"].replace({'\$':''}, regex = True)
    df["TrialPrice"] = df["TrialPrice"].replace({'\$':''}, regex = True)
    # Renaming columns names to avoid whitespace
    df.columns = [label.replace(' ', '_') for label in df.columns]
    return df


"""
Regex Pattern

\d -  Match any digit     
\D -  Match any non-digit
\s -  Match any whitespace        
\S -  Match any non-whitespace
\w -  Match any alphanumeric char     
\W -  Match any non-alphanumeric char

                                                            Example
? -  Match zero or one repetitions of preceding                 "ab?" matches "a" or "ab"
* -  Match zero or more repetitions of preceding                "ab*" matches "a", "ab", "abb", "abbb"...
+ -  Match one or more repetitions of preceding                 "ab+" matches "ab", "abb", "abbb"... but not "a"
{n} - Match n repetitions of preeeding                          "ab{2}" matches "abb"
{m,n} - Match between m and n repetitions of preceding          "ab{2,3}" matches "abb" or "abbb"


Reference - 
https://jakevdp.github.io/WhirlwindTourOfPython/14-strings-and-regular-expressions.html
https://www.programiz.com/python-programming/regex


"""