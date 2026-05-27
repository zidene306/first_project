import pandas as pd

#=============================================================================
#Split the category colinto several categories
#=============================================================================


def clean_category_col(df):
    """
    input: raw df
    slit the main category into 2 sub_categories
    output: df1 = df with 2 more columns (sub_cat1/2)
    """
    df1 = df.copy()
    
    #split the category colinto several categories
    cat1 = df1["category"].apply(
                                 lambda x : str(x).split("|")[0]
                                            .strip()
                                            .replace("&", "_")
                                 )
    cat2 = df1["category"].apply(
                                 lambda x : str(x).split("|")[1]
                                            .strip()
                                            
                                            .replace(",", "_")
                                            .replace("&", "_")
                                 )
    
    df1.insert(3, "sub_cat1", cat1)
    df1.insert(4, "sub_cat2", cat2)
    
    return df1

#=============================================================================
#Clean the discounted_price column
#=============================================================================

def disc_price_col_clean(df):
    """
    input: raw df
    Clean the column discount_price and cast it to float
    output: df1 = df 
    """

    df1 = df.copy()
    df1["discounted_price"] = (
                                df1["discounted_price"]
                                .astype(str)
                                .str.replace("₹", "", regex= False)
                                .str.replace(",", "", regex = False)
                                .astype(float)
                                .round(2)
                                .apply(lambda x : f"{x : .2f}")
                              )
    
    return df1

#=============================================================================
#Clean the actual_price column
#=============================================================================

def actual_price_col_clean(df):
    """
    input: raw df
    Clean the column actual_price and cast it to float
    output: df1 = df 
    """

    df1 = df.copy()
    df1["actual_price"] = (
                                df1["actual_price"]
                                .astype(str)
                                .str.replace("₹", "", regex= False)
                                .str.replace(",", "", regex = False)
                                .astype(float)
                                .apply(lambda x : f"{x : .2f}")
                              )
    
    return df1

#============================================================================#
#Clean the discount_percentage column                                        #
#============================================================================#

def discount_percent_clean(df):
    """
    input: raw df
    Clean the column discount_percentage and cast it to integer: remove % sign
    output: df1
    """

    df1 = df.copy()
    df1["discount_percentage"] = (
                                df1["discount_percentage"]
                                .astype(str)
                                .str.replace("%", "", regex= False)
                                .astype(int)
                              )
    return df1

#============================================================================#
#convert the 2 columns: rating rating & rating_count to floats                                    #
#============================================================================#

def rating_cols_clean(df):
    """
    input: raw df
    convert the 2 columns: rating to float  & rating_count to in
    output: df1
    """

    df1 = df.copy()

    #delete 2  NaN rows based on column: "rating_count": 2/1464 = 0.14%
    df1 = df1.dropna(subset = "rating_count")
    #convert the column rating to int
    df1["rating"] = (
                     df1["rating"]
                     .astype(str)
                     
                     .str.replace("|", "1", regex= False)    
                     .astype(float)
                     .apply(lambda x : f"{x : .1f}")
                     )
   #convert the column rating_count to int
    df1["rating_count"] = (
                     df1["rating_count"]
                     .astype(str)
                     
                     .str.replace(",", "", regex= False)
                     .astype(int)
                     )
    
    return df1  

def clean_split_reviews_ids(df):
    """
    input raw df
    split all columns containing multiple values into lists for indexing
    output
    """
    df1=df.copy()
    
    df1.review_id = df1.review_id.str.split(',')
    df1.user_id = df1.user_id.str.split(',')
    df1.review_title = df1.review_title.str.split(',')
    df1.review_content = df1.review_content.str.split(',')
    return df1


def remove_product_id_dupl(df):
    """
    input raw df
    order by the number of product reviews
    remove any duplicates, as identified by identical product names or product ids
    """
    df1 = df.copy()
    sorted_df1 = df1.sort_values(by='rating_count', ascending=False)
    df1 = sorted_df1.drop_duplicates(subset='product_id', keep='first')
    df1 = sorted_df1.drop_duplicates(subset='product_name', keep='first')
    df1.reset_index(drop=True, inplace=True)
    return df1