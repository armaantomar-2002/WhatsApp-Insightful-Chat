

import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji

def fetch_stats(select_users, df):
    if select_users != 'Overall':
        df = df[df['user'] == select_users]

    df = df[df['message'].apply(lambda x: isinstance(x, str))]

    num_messages = df.shape[0]
    words = sum(df['message'].dropna().str.split().apply(len))
    num_media_msg = df[df['message'] == '<Media omitted>'].shape[0]
    links = df['message'].str.contains('http').sum()
    
    return num_messages, words, num_media_msg, links

def monthly_timeline(select_users, df):
    if select_users != 'Overall':
        df = df[df['user'] == select_users]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + '-' + timeline['year'].astype(str)
    return timeline

def daily_timeline(select_users, df):
    if select_users != 'Overall':
        df = df[df['user'] == select_users]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(select_users, df):
    if select_users != 'Overall':
        df = df[df['user'] == select_users]
    return df['day_name'].value_counts()

def month_activity_map(select_users, df):
    if select_users != 'Overall':
        df = df[df['user'] == select_users]
    return df['month'].value_counts()

def activity_heatmap(select_users, df):
    if select_users != 'Overall':
        df = df[df['user'] == select_users]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap

def fetch_most_busy(df):
    x = df['user'].value_counts().head(5)
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, new_df

def create_wordcloud(select_users, df):
    if select_users != 'Overall':
        df = df[df['user'] == select_users]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    return wc.generate(' '.join(df['message'].dropna()))

def most_common_words(select_users, df):
    if select_users != "Overall":
        df = df[df['user'] == select_users]
    words = ' '.join(df['message'].dropna()).split()
    word_freq = pd.Series(words).value_counts().reset_index()
    word_freq.columns = ['word', 'count']
    return word_freq.head(20)

def most_emojis(select_users, df):
    if select_users != 'Overall':
        df = df[df['user'] == select_users]
    
    # Update to use the new API
    all_emojis = emoji.EMOJI_DATA.keys()
    emojis = [char for message in df['message'] for char in message if char in all_emojis]
    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['emoji', 'count'])
    return emoji_df
