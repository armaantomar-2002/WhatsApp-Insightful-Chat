# app.py

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessor import preprocess
from help import fetch_stats, monthly_timeline, daily_timeline, week_activity_map, month_activity_map, activity_heatmap, fetch_most_busy, create_wordcloud, most_common_words, most_emojis

st.title("WhatsApp Insightful Chat 📈💬🔍")

st.markdown("""
    WhatsApp Chat Analyzer is a Streamlit-based web application designed to analyze and visualize WhatsApp chat data. It provides insights into chat patterns, message statistics, user activity, and textual content from WhatsApp chat exports. The tool offers a variety of features including:

Message and Word Statistics: Total messages, words, media count, and links.
            
Timeline Analysis: Monthly and daily timelines of chat activity.
            
Activity Maps: Visualizations of user activity by day and month, and a weekly activity heatmap.
            
User Activity Insights: Identification of the most active users and the creation of word clouds from chat messages.
            
Emoji Analysis: Visualization of the most frequently used emojis in the chat. 🚀
""")

st.sidebar.title("Upload Chat Data")
upload_file = st.sidebar.file_uploader("Choose a file", key="file_uploader")

if upload_file is not None:
    try:
        bytes_data = upload_file.getvalue()
        data = bytes_data.decode("utf-8")
        
        # Preprocess the data
        df = preprocess(data)
        
        if 'user' in df.columns:
            user_list = df.loc[df['user'] != 'group_notification', 'user'].unique().tolist()
            user_list.sort()
            user_list.insert(0, "Overall")
        
        select_users = st.sidebar.selectbox("Show Analysis with respect to:", user_list, key="user_select")
        
        if st.sidebar.button("Show Analysis", key="show_button"):
            st.title('* Top Analysis based on Statistics 📊')
            
            num_messages, words, num_media_msg, links = fetch_stats(select_users, df)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.header("Total Messages 📩")
                st.title(num_messages)
            
            with col2:
                st.header("Total Words 📝")
                st.title(words)
            
            with col3:
                st.header("Total Media 📷")
                st.title(num_media_msg)
            
            with col4:
                st.header("All Media Links 🔗")
                st.title(links)
                
            st.title('Monthly Timeline of Chat 📅')
            monthly_timeline_data = monthly_timeline(select_users, df)
            fig, ax = plt.subplots()
            ax.plot(monthly_timeline_data['time'], monthly_timeline_data['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
            st.title('Daily Timeline of Chat 🌞')
            daily_timeline_data = daily_timeline(select_users, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline_data['only_date'], daily_timeline_data['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
            st.title('Most Busy Users Analysis 🔥')
            x, new_df = fetch_most_busy(df)
            fig, ax = plt.subplots()
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            st.dataframe(new_df)
            
            st.title('Weekly Activity Map 🗓️')
            busy_day = week_activity_map(select_users, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
            st.title('Monthly Activity Map 📅')
            busy_month = month_activity_map(select_users, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
                
            st.title('Weekly Activity Heatmap 🔥')
            user_heatmap = activity_heatmap(select_users, df)
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, ax=ax)
            st.pyplot(fig)
            
            st.title('Word Cloud 🗣️')
            wc = create_wordcloud(select_users, df)
            fig, ax = plt.subplots()
            ax.imshow(wc)
            st.pyplot(fig)
            
            st.title('Most Common Words 📜')
            common_words_df = most_common_words(select_users, df)
            fig, ax = plt.subplots()
            ax.bar(common_words_df['word'], common_words_df['count'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
            st.title('Emoji Analysis 😃')
            emoji_df = most_emojis(select_users, df)
            st.dataframe(emoji_df)
            
    except Exception as e:
        st.error(f"An error occurred: {e}")
