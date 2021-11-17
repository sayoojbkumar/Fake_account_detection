from sklearn.datasets import make_classification
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
from urllib.parse import urlparse

import requests

from flask import Flask, render_template ,request
data=pd.read_csv('dataset/fake_genuine_merge.csv',header=0)
normalized=data
normalized.drop('username',inplace=True,axis=1)
normalized.drop('full_name',inplace=True,axis=1)
normalized.drop('has_anonymous_profile_picture',inplace=True,axis=1)
data=normalized


Y=data["is_fake"]
X=data.loc[:, data.columns != 'is_fake']

print("ready to go")


def get_user_data(session,username):
    if username:
        user_url="https://www.instagram.com/{}/?__a=1"
        headers = {
            'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)',
            'Cookie':session
        }
        try:
            res = requests.get(user_url.format(username),headers=headers)
            user_data = res.json()
        except:
            print("some issue with user "+username)
    return user_data,username



def update_media(x):
    if(x>=12):
        return 12
    else:
        return x

app = Flask(__name__)


@app.route('/instructions')
def instruction():
    return render_template('instruction.html')
@app.route('/authors')
def author():
    return render_template('author.html')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/datacollector', methods =["GET", "POST"])
def collector():
    session='sessionid=49148778067%3AZzjnWkBUCVz6ht%3A24'
    if request.method == "POST":
        input_text = request.get_json()
        url=input_text['input']
        url_parts=urlparse(url)
        if(url_parts.netloc != 'www.instagram.com' or url_parts.path == ''):
            return "Bad Input Format"
        else:
            try:
                x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=1)
                username=url_parts.path.replace('/','')
                single_data,user_name=get_user_data(session,username)
                single_row=[]
                single_row.append(user_name)
                single_row.append(single_data["graphql"]["user"]["full_name"])
                single_row.append(single_data["graphql"]["user"]["is_verified"])
                single_row.append(len(single_data["graphql"]["user"]["biography"]))#bio
                single_row.append(single_data["graphql"]["user"]["external_url"])#eternalurl_in_bio
                single_row.append(single_data["graphql"]["user"]["edge_followed_by"]["count"])#folowers
                single_row.append(single_data["graphql"]["user"]["edge_follow"]["count"])#following
                single_row.append(single_data["graphql"]["user"]["has_clips"])#has any videoclip in acc
                single_row.append(single_data["graphql"]["user"]["highlight_reel_count"])#highlights count
                single_row.append(single_data["graphql"]["user"]["is_professional_account"])#is_professional_acc
                single_row.append(single_data["graphql"]["user"]["is_private"])#is_private_acc?
                single_row.append(single_data["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])#no_of_posts
                media_count=single_data["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]
                tag_count=0
                likes_count=0
                comment_count=0
                location_count=0
                if(media_count >= 12):
                    media_count=12
                for j in range(0,media_count):
                    tag_count=tag_count+len(single_data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][j]["node"]["edge_media_to_tagged_user"]["edges"])#no_of_users_tagged_in_single_post
                    comment_count=comment_count + single_data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][j]["node"]["edge_media_to_comment"]["count"]#count_of_comments
                    likes_count = likes_count + single_data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][j]["node"]["edge_liked_by"]["count"]#postlikes_counts
                    if(single_data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][j]["node"]["location"]):#if_location_given
                        location_count=location_count+1
                single_row.append(tag_count)
                single_row.append(likes_count)
                single_row.append(comment_count)
                single_row.append(len(single_data["graphql"]["user"]["full_name"]))
                single_row.append(update_media(media_count))
                for i in range(0,len(single_row)):
                    if(single_row[i]==False):
                        single_row[i]=0
                    elif(single_row[i]==True):
                        single_row[i]=1
                    elif(single_row[i]==None):
                        single_row[i]=0
                    elif(type(single_row[i])==str):
                        single_row[i]=1
                if(single_row[16]==0):
                    single_row.append(0)
                else:
                    single_row.append(single_row[13]/single_row[16])
                print(single_row)
                scaler = StandardScaler()
                scaler.fit(x_train)
                x_train = scaler.transform(x_train)
                x_test = scaler.transform(np.array(single_row[2:]).reshape(1,-1))
                log_reg = LogisticRegression()
                log_reg.fit(x_train, y_train)
                LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
                penalty='l2', random_state=None, solver='lbfgs', tol=0.0001,
                verbose=0, warm_start=False) 
                print(x_test)  
            except:
                return "Failed fetching necessary data \n You Submitted a Private Account read instructions for more info"

            y_pred = log_reg.predict(x_test)
            if(y_pred[0]==1):
                return "Looks Like Fake Account"
            else:
                return "Looks Like Genuine Account"

if __name__ == '__main__':
    app.run()