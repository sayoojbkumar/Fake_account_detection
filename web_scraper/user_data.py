import requests
import os
import csv

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

def get_folowing(user_id,session):
    user = {}
    if user_id:
        base_url = "https://i.instagram.com/api/v1/friendships/{}/following/?count="+input("enter no of followers ")
        headers = {
            'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)',
            'Cookie':session
        }
        try:
            res = requests.get(base_url.format(user_id),headers=headers)
            user_info = res.json()
        except:
            print("getting user failed")
    return user_info

user_id=5989317029#need_to_change
session='sessionid='+input('input session ')#check ur cookie to get sessionid value

user_data=get_folowing(user_id,session)
header = ['username', 'full_name', 'is_verified', 'has_anonymous_profile_picture']
with open('users.csv', 'w', encoding='UTF16', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for i in range(0,len(user_data['users'])):
        single_row=[]
        single_row.append(user_data['users'][i]['username'])
        single_row.append(user_data['users'][i]['full_name'])
        single_row.append(user_data['users'][i]['is_verified'])
        single_row.append(user_data['users'][i]['has_anonymous_profile_picture'])
        print(single_row)
        writer.writerow(single_row)

with open('users_data.csv', 'w', encoding='UTF16', newline='') as g:
    header = ['username', 'seo_category_infos', 'biography_len', 'external_url','followers','following','fbid','has_clips','highlight_count','is_professional_account','business_email','business_phone_number','is_private','media_count','total_tags','total_likes','total_comments']
    writer = csv.writer(g)
    writer.writerow(header)
with open('users.csv',encoding='utf-16') as f:
    user_dict=csv.DictReader(f)
    for row in user_dict:
        single_data,user_name = get_user_data(session,row["username"])
        with open('users_data.csv', 'a', encoding='UTF16', newline='') as g:
            writer = csv.writer(g)
            single_row=[]
            single_row.append(user_name)
            single_row.append(len(single_data["seo_category_infos"]))#seocat no
            single_row.append(len(single_data["graphql"]["user"]["biography"]))#bio
            single_row.append(single_data["graphql"]["user"]["external_url"])#eternalurl_in_bio
            single_row.append(single_data["graphql"]["user"]["edge_followed_by"]["count"])#folowers
            single_row.append(single_data["graphql"]["user"]["edge_follow"]["count"])#following
            single_row.append(single_data["graphql"]["user"]["fbid"])#fbid
            single_row.append(single_data["graphql"]["user"]["has_clips"])#has any videoclip in acc
            single_row.append(single_data["graphql"]["user"]["highlight_reel_count"])#highlights count
            single_row.append(single_data["graphql"]["user"]["is_professional_account"])#is_professional_acc
            single_row.append(single_data["graphql"]["user"]["business_email"])#mail
            single_row.append(single_data["graphql"]["user"]["business_phone_number"])#number
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
            print(single_row)
            writer.writerow(single_row)