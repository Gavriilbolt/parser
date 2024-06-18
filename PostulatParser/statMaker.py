import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

import options


# Connect to the SQLite database and retrieve the data
def get_data_from_db(db_name):
    conn = sqlite3.connect(db_name)
    query = "SELECT author FROM articles"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# Process the data to calculate the scores for each author
def calculate_scores(df):
    author_scores = {}

    for authors in df['author']:
        author_list = [author.strip() for author in authors.split(',')]
        score_per_author = 1 if len(author_list) == 1 else 0.5

        for author in author_list:
            if author in author_scores:
                author_scores[author] += score_per_author
            else:
                author_scores[author] = score_per_author

    scores_df = pd.DataFrame(list(author_scores.items()), columns=['Author', 'Score'])
    scores_df = scores_df.sort_values(by='Score', ascending=False)

    return scores_df


# Visualize the data and save the bar chart as an image
def plot_bar_chart(scores_df, output_image_path):
    plt.figure(figsize=(10, 8))
    plt.barh(scores_df['Author'], scores_df['Score'], color='skyblue')
    plt.xlabel('Score')
    plt.ylabel('Author')
    plt.title('Most Popular Authors by Score')
    plt.gca().invert_yaxis()  # Invert y-axis to show the highest score at the top
    plt.tight_layout()
    plt.savefig(output_image_path)
    plt.close()

# Create a table image with author and score data
def save_table_image(scores_df, output_image_path):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('tight')
    ax.axis('off')
    table_data = scores_df.values
    col_labels = scores_df.columns
    table = ax.table(cellText=table_data, colLabels=col_labels, cellLoc='center', loc='center', colColours=['lightblue', 'lightblue'])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)
    plt.savefig(output_image_path, bbox_inches='tight')
    plt.close()


# Main function to execute the steps
def main():
    db_name = options.db_name  # Replace with your database name
    images_dir = options.images_dir
    bar_chart_path = os.path.join(images_dir, 'author_scores_chart.png')  # Output image path for bar chart
    table_image_path = os.path.join(images_dir, 'author_scores_table.png')  # Output image path for table

    # Step 1: Get data from database
    df = get_data_from_db(db_name)

    # Step 2: Calculate scores for each author
    scores_df = calculate_scores(df)

    # Step 3: Plot the bar chart and save the image
    plot_bar_chart(scores_df, bar_chart_path)

    # Step 4: Save the table as an image
    save_table_image(scores_df, table_image_path)


if __name__ == '__main__':
    main()
