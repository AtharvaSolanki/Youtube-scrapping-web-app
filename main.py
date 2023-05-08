from youtube_statistics import YTstats
from pytube import YouTube
from pytube import Channel
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import scrapetube 

def flask(video):
    #video=str(input('Enter Video URL '))
    #video=simpledialog.askstring('Video',"Enter Video Url\t\t\t\t",parent=input_ui)
    x=YouTube(video,use_oauth=True, allow_oauth_cache=True)
    channelId=x.channel_id
    curl=x.channel_url
    c=Channel(curl)
    cname=c.channel_name
    print("channel Name =" , cname)
    print("channel Id =" , channelId)
    print("channel url =" , curl)

    API_KEY="AIzaSyDs1FSxbBA7UJZofrSXj0k8WPdjCC1fxqg"
    channel_id=channelId
    yt= YTstats(API_KEY,channel_id)
    #yt.get_channel_statistics()
    #yt.dump()

    yt = YTstats(API_KEY, channel_id)
    yt.extract_all()
    yt.dump() 
    #yt.get_channel_video_data()



    file1=yt.dump()
    #file='hitesh_choudhary.json'
    data= file1
    #with open(file,'r') as f:
    #   data= json.load(f)


    # In[4]:


    channelId, stats = data.popitem()
    print(channelId)


    # In[5]:


    channel_stats=stats['channel_statistics']
    video_stats=stats['video_data']


    # In[6]:


    Views=int(channel_stats [ "viewCount"])
    Subscribers= int(channel_stats [ "subscriberCount"])
    Videos=int(channel_stats [ "videoCount"])

    # In[7]:


    #sorted_vids = sorted(video_stats.items (), key=lambda item: int(item [1]["viewCount"]),reverse=True)
    sorted_vids=video_stats.items ()
    stats = []
    for vid in sorted_vids:
        try:

            video_id = vid[0]
            channel_name=vid[1]["channelTitle"]
            title=vid[1]["title"]
            date=vid[1]["publishedAt"]
            views = vid[1] [ "viewCount"]
            likes = vid[1]["likeCount"]
            comments = vid[1]["commentCount"]
            definition=vid[1]['definition']
            #Dimension=vid[1]['dimension']
            #description=vid[1]['description']
            #tags=vid[1]["tags"]
            stats.append( [channel_name,title,date, views,likes,comments,definition])
        except:
            pass


    # In[97]:


    df=pd.DataFrame(stats, columns=['Channel Name','Video Title','Date','Views','Likes','Comments','Definition'])
    df.to_csv('a.csv')


    # In[10]:


    list_me=[]
    url="https://www.youtube.com/watch?v="
    dataframe=pd.DataFrame(columns=["URL"])
    videos=scrapetube.get_channel (channelId)
    for video in videos:
        url1=url+str(video['videoId'])
        print(url1)
        list_me.append(url1)
    # In[11]:
    new_list=[]
    if len(df)>=len(list_me):
        new_list=list_me
    else:
        
        c=0
        while c<=len(df):

            new_list.append(list_me[c])
            c +=1


    # In[13]:


    titl=[]
    for i in new_list:
        video=i
        #video=simpledialog.askstring('Video',"Enter Video Url\t\t\t\t",parent=input_ui)
        x=YouTube(video,use_oauth=True, allow_oauth_cache=True)
        titl.append(x.title)


    # In[96]:

    df1 = pd.DataFrame(list(zip(titl,list_me)),columns =['Video Title', 'Link'])


    # In[98]:


    newdf=pd.merge(df, df1, on = "Video Title", how = "inner")


    # In[99]:


    # In[63]:


    #newdf.to_csv('hitesh_choudhary.csv')


    # ### Calculating Engagement

    # The total engagement (likes, comments, and dislikes) divided by the number of videos the profile published. The result is then divided by the number of subscribers, and all multiplied by 100.

    #  a=(((likes+comments)/no. of videos)/subscribers)*100

    # In[57]:

    eng=[]

    for index, row in newdf.iterrows():
        likes=row['Likes']
        comments=row['Comments']
        total=likes+comments
        add=int(total)
        engagement=(((add)/Videos)/Subscribers)*100
        output=round(engagement,6)
        
        eng.append(output)
        


    # In[100]:


    newdf['engagement']=eng



    # In[102]:


    finaldata=newdf.sort_values("engagement",ascending=False)


    # In[103]:


    mosteng=finaldata.head(10).drop(['engagement'], axis=1)


    # In[104]:


    mosteng = mosteng.set_index(['Channel Name'])



    # In[106]:


    #sprint(mosteng)


    # In[95]:


    mosteng.to_csv('most_engaged_videos.csv')