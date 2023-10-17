from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import emoji

# Set the font for Matplotlib
plt.rcParams['font.sans-serif'] = 'Arial Unicode MS'  # Change to a font that supports the missing glyph


def fetch_stats(selectedUser, df):

    if selectedUser != 'Overall':
        df = df[df['User'] == selectedUser]

# fetch total number of messages
    num_messages = df.shape[0]

    words = []
    for m in df['Message']:
        words.extend(m.split())


    # fetch number of media messages
   # df['message'] = df['message'].str.strip()
    num_media_messages = df[df['Message'] == 'image omitted\n'].shape[0]
    # number_of_rows_to_store = 3

    # Use .loc to select and store the desired number of rows
  #  selected_rows = num_media_messages.iloc[:number_of_rows_to_store]

    # fetch number of links shared

    links = []
    url_extractor = URLExtract()

    for m in df['Message']:
        links.extend(url_extractor.find_urls(m))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    busy_user = df['User'].value_counts().head()
    msgpercent = round(df['User'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(
        columns={'Count': 'Percentage', 'User': 'Name'})
    return busy_user, msgpercent


def create_wordcloud(selectedUser, df):
    try:

        with open('stop_hinglish.txt', 'r') as f:
            stop_words = f.read()

        if selectedUser != 'Overall':
            df = df[df['User'] == selectedUser]

        temp = df[df['Message'] != 'video omitted\n']
        temp = temp[temp['Message'] != 'image omitted\n']

        def remove_stop_words(message):
            word_list = []
            for word in message.lower().split():
                if word not in stop_words:
                    word_list.append(word)
            return " ".join(word_list)

        wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
        temp['Message'] = temp['Message'].apply(remove_stop_words)
        df_wc = wc.generate(temp['Message'].str.cat(sep=" "))
        return df_wc

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def most_common_words(selectedUser, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selectedUser != 'Overall':
        df = df[df['User'] == selectedUser]

    temp = df[df['Message'] != 'video omitted\n']
    temp = temp[temp['Message'] != 'image omitted\n']

    words = []

    for message in temp['Message']:
        # Convert the message to lowercase and split it into words
        message = message.lower().split()

        # Filter out stop words and append the remaining words
        words.extend([word for word in message if word not in stop_words])

    df_words = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Count'])

    # Filter out rows with blank or white spaces in the 'Words' column
    df_words = df_words[df_words['Word'].str.strip() != ' ']

    # Use the drop method to remove the row by index
    df_words = df_words.drop(0)

    # Reset the index after removing rows
    df_words = df_words.reset_index(drop=True)

    return df_words


# emoji analysis

def emoji_count(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['User'] == selectedUser]

    emojis = []

    for message in df['Message']:
        for character in message:
            if emoji.is_emoji(character):
                emojis.append(character)


    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selectedUser, df):

    if selectedUser != 'Overall':
        df = df[df['User'] == selectedUser]

    timeline = df.groupby(['Year', 'Month_Number', 'Month']).count()['Message'].reset_index()

    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + " - " + str(timeline['Year'][i]))

    timeline['Timeline'] = time

    return timeline



def daily_timeline(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['User'] == selectedUser]

    daily_timeline = df.groupby('Date').count()['Message'].reset_index()

    return daily_timeline


def week_activity(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['User'] == selectedUser]

    return df['Day'].value_counts()


def month_activity(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['User'] == selectedUser]

    return df['Month'].value_counts()


def activity_heatmap(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['User'] == selectedUser]

    user_activity = df.pivot_table(index='Day', columns='Period', values='Message', aggfunc='count').fillna(0)

    return user_activity





