#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import pandas as pd 


# In[2]:


books=pd.read_csv('Books.csv')
users=pd.read_csv('Users.csv')
ratings=pd.read_csv('Ratings.csv')


# In[3]:


books.head()


# In[4]:


users.head()


# In[5]:


ratings.head()


# In[6]:


print(books.shape)
print(ratings.shape) 
print(users.shape)


# In[7]:


books.isnull().sum()


# In[8]:


users.isnull().sum()


# In[9]:


ratings.isnull().sum()


# In[10]:


books.duplicated().sum()


# In[11]:


ratings.duplicated().sum()


# In[12]:


users.duplicated().sum()


# # EDA

# In[13]:


import matplotlib.pyplot as plt 
import seaborn as sns


# In[14]:


# Convert to numeric, forcing non-numeric values to NaN
books["Year-Of-Publication"] = pd.to_numeric(books["Year-Of-Publication"], errors="coerce")

# Replace NaN values with the median year
median_year = books["Year-Of-Publication"].median()
books["Year-Of-Publication"].fillna(median_year, inplace=True)

# Convert to integer
books["Year-Of-Publication"] = books["Year-Of-Publication"].astype(int)


# In[15]:


plt.figure(figsize=(10, 5))
sns.histplot(books["Year-Of-Publication"], bins=50, kde=True, color="royalblue")
plt.xlabel("Year of Publication")
plt.ylabel("Count of Books")
plt.title("Distribution of Book Publication Years")
plt.show()


# In[16]:


books.describe(include='all')

o and 2050 years are invalid
# In[17]:


# removing outliers


# In[18]:


books_cleaned=books[(books['Year-Of-Publication']>=1900) & (books['Year-Of-Publication']<=2025)]


# In[19]:


common_year = books_cleaned["Year-Of-Publication"].mode()[0]
print(f"The most common year of publication is: {common_year}")


# In[20]:


books_cleaned.describe(include='all')


# In[21]:


books_cleaned.describe(include='all')


# # Popularity Based recommender System

# In[22]:


ratings_with_name=ratings.merge(books_cleaned,on='ISBN')


# In[23]:


ratings_with_name.shape


# In[24]:


ratings_with_name.head()


# In[25]:


num_rating_df=ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_rating_df.rename(columns={'Book-Rating':"num_ratings"},inplace=True)


# In[26]:


num_rating_df


# In[27]:


# df with average


# In[28]:


avg_rating_df=ratings_with_name.groupby('Book-Title')['Book-Rating'].mean().reset_index()
avg_rating_df.rename(columns={'Book-Rating':"avg_ratings"},inplace=True)


# In[29]:


avg_rating_df


# In[30]:


popularity_df=num_rating_df.merge(avg_rating_df,on='Book-Title')


# In[31]:


popularity_df


# In[32]:


books_cleaned


# In[33]:


popular_df=popularity_df[popularity_df['num_ratings']>=250].sort_values('avg_ratings',ascending=False).head(50).reset_index()


# In[34]:


popular_df

Keeping Required columns
# In[35]:


popular_df=popular_df.merge(books,on='Book-Title',how='left').drop_duplicates('Book-Title')[['Book-Title','Book-Author','Image-URL-M','num_ratings','avg_ratings']]


# In[36]:


popular_df.shape


# In[37]:


popular_df[['Book-Title', 'Image-URL-M']].isna().sum()


# In[38]:


popular_df


# # Collaborative Filtering Based Recommender System

# In[39]:


# 1) Finding user who have voted on >=200 books & 2) books with >=50 users ratings 


# # 1)

# In[40]:


X=ratings_with_name.groupby('User-ID').count()['Book-Rating'] > 200
padhe_users=X[X].index


# In[41]:


filtered_rating=ratings_with_name[ratings_with_name['User-ID'].isin(padhe_users)]


# # 2)

# In[42]:


filtered_rating


# In[43]:


y=filtered_rating.groupby('Book-Title').count()['Book-Rating']>=50
famous_books=y[y].index


# In[44]:


famous_books


# In[45]:


final_ratings=filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]


# In[46]:


final_ratings


# In[47]:


pt = final_ratings.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')


# In[48]:


pt


# In[49]:


pt.fillna(0,inplace=True)


# In[50]:


pt


# In[51]:


from sklearn.metrics.pairwise import cosine_similarity


# In[52]:


if pt.shape[0] == 0 or pt.shape[1] == 0:
    print("Pivot table is empty! Check data loading.")


# In[53]:


similarity_score=cosine_similarity(pt)


# In[54]:


similarity_score[0]


# In[55]:


np.where(pt.index=='Year of Wonders')[0][0]


# In[56]:


sorted(list(enumerate(similarity_score[0])),key=lambda x:x[1],reverse=True)[1:6] # sorting according to the values 


# In[57]:


def recommend(book_name):
    #index fetch
    index=np.where(pt.index==book_name)[0][0]
    similar_items=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:6]

    data=[]
    for i in similar_items:
        # print(pt.index[i[0]])
        item=[]
        temp_df=books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))
        
        data.append(item)
    return data


# In[58]:


recommend('Harry Potter and the Chamber of Secrets (Book 2)')


# In[59]:


recommend('The Notebook')


# In[60]:


import pickle 


# In[61]:


with open('top_50.pkl','wb') as f :
    pickle.dump(popular_df,f)


# In[62]:


pickle.dump(pt,open('pt.pkl','wb'))


# In[63]:


pickle.dump(books_cleaned,open('books.pkl','wb'))


# In[64]:


pickle.dump(similarity_score,open('similarity_score.pkl','wb'))


# In[ ]:





# In[ ]:





# In[ ]:




