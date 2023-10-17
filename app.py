import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['User'].unique().tolist()
    # user_list.remove("Hello Friends!❤")
    user_list.sort()
    user_list.insert(0, "Overall")

    selectedUser = st.sidebar.selectbox("Show User Analysis", user_list)

    st.markdown(
        f'<h1 style="color: #632626;">TOP WHATSAPP CHAT STATISTICS OF {selectedUser.upper()}</h1>',
        unsafe_allow_html=True
    )

    st.dataframe(df)  # can delete this loc to not dispaly the msgs

    if st.sidebar.button("Show Analysis"):
        msgs, words, num_media_messages, links = helper.fetch_stats(selectedUser, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # Create a header with custom CSS
            st.markdown(
                f'<h2 style="color: #FFD966;">Total Messages</h2>',
                unsafe_allow_html=True
            )
            st.title(msgs)

        with col2:
            st.markdown(
                f'<h2 style="color: #FFD966;">Total Words</h2>',
                unsafe_allow_html=True
            )
            st.title(words)

        with col3:
            st.markdown(
                f'<h2 style="color: #FFD966;">Media Shared</h2>',
                unsafe_allow_html=True
            )
            st.title(num_media_messages)

        with col4:
            st.markdown(
                f'<h2 style="color: #FFD966;">Links Shared</h2>',
                unsafe_allow_html=True
            )
            st.title(links)

        # finding the busiest users in the group (Group level)

        if selectedUser == 'Overall':
            st.title('Most Busy User')
            busy_user, msgpercent = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(busy_user.index, busy_user.values, color='#64CCC5')
                # Set the x and y labels with custom colors
                ax.set_xlabel('Users', color='#9D5353', fontsize=15)
                ax.set_ylabel('Number Of Messages', color='#9D5353', fontsize=12)

            #    fig.set_facecolor('lightpink')  # Dark gray
                st.pyplot(fig)
            with col2:
                st.dataframe(msgpercent, width=600, height=200)

        # monthly timeline
        st.markdown(
            f'<h2 style="color: #FFD966;">Monthly Timeline</h2>',
            unsafe_allow_html=True
        )
     #   st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selectedUser, df)
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.plot(timeline['Timeline'], timeline['Message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline

        # st.title("Daily Timeline")
        st.markdown(
            f'<h2 style="color: #FFD966;">Daily Timeline</h2>',
            unsafe_allow_html=True
        )
        Daily_timeline = helper.daily_timeline(selectedUser, df)
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.plot(Daily_timeline['Date'], Daily_timeline['Message'], color='#A7D397')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map

        # st.title("Activity Map")
        st.markdown(
            f'<h2 style="color: #FFD966;">Activity Map</h2>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)
        with col1:
            # st.header("Busiest Day")
            st.markdown(
                f'<h4 style="color: #9D5353;">Busiest Day</h2>',
                unsafe_allow_html=True
            )
            busy_day = helper.week_activity(selectedUser, df)
            fig, ax = plt.subplots(figsize=(8, 12))
            ax.barh(busy_day.index, busy_day.values, color='#3282B8')
            st.pyplot(fig)

        with col2:
            # st.header("Busiest Month")
            st.markdown(
                f'<h4 style="color: #9D5353;">Busiest Month</h2>',
                unsafe_allow_html=True
            )
            busy_month = helper.month_activity(selectedUser, df)
            fig, ax = plt.subplots(figsize=(8, 12))
            ax.barh(busy_month.index, busy_month.values, color='#0F4C75')
            st.pyplot(fig)

        # WORD CLOUD
        # st.title("Word Cloud")
        st.markdown(
            f'<h2 style="color: #FFD966;">Word Cloud</h2>',
            unsafe_allow_html=True
        )
        df_wc = helper.create_wordcloud(selectedUser, df)
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        words_df = helper.most_common_words(selectedUser, df)
        st.dataframe(words_df)

        # Create a bar chart
        fig, ax = plt.subplots()
        ax.barh(words_df['Word'], words_df['Count'], color='#FF6969')
        plt.xticks(rotation='vertical')
      #  fig.set_facecolor('lightpink')
        ax.set_xlabel('Word', color='#9D5353', fontsize=12)
        ax.set_ylabel('Count', color='#9D5353', fontsize=12)
        ax.set_title('Word Count Bar Chart', color='#9D5353')

        # Display the chart in Streamlit
        # st.title("Most Common Words")
        st.markdown(
            f'<h2 style="color: #FFD966;">Most Common Words</h2>',
            unsafe_allow_html=True
        )

        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_count(selectedUser, df)

        # st.title("Emoji Analysis")
        st.markdown(
            f'<h2 style="color: #FFD966;">Emoji Analysis</h2>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")

            st.pyplot(fig)

        # activity heatmap

        # st.title('Weekly Activity Heatmap')
        st.markdown(
            f'<h2 style="color: #FFD966;">Weekly Activity Heatmap</h2>',
            unsafe_allow_html=True
        )

        user_activity = helper.activity_heatmap(selectedUser, df)
        fig, ax = plt.subplots(figsize=(20, 10))
        plt.xticks(rotation='vertical')
        ax.set_xlabel('Day', fontsize=20)
        ax.set_ylabel('Period', fontsize=20)
        ax = sns.heatmap(user_activity)
        st.pyplot(fig)
