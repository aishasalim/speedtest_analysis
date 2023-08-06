import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Set global font size and type
matplotlib.rcParams.update({'font.size': 15, 'font.family': 'Helvetica'})

class GraphDrawer:
    def __init__(self, data, promised_download, promised_upload):
        self.data = data  # This now assumes 'data' is a list of dictionaries
        self.promised_download = promised_download
        self.promised_upload = promised_upload

    def plot_graph(self, df):
        # Convert the datetime to the format MM/DD HH pm/am for the graph
        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
        df['datetime'] = df['datetime'].dt.strftime('%m/%d %I %p').str.replace('^0', '', regex=True).str.replace(' 0', ' ', regex=True)
        df = df.set_index('datetime')

        # Plot the download_speed and upload_speed
        fig, ax1 = plt.subplots(figsize=(10, 5))
        df.download_speed.plot(kind='bar', color='green', ax=ax1, width=0.4, position=1)
        df.upload_speed.plot(kind='bar', color='purple', ax=ax1, width=0.4, position=0)

        # Lines of promised speeds
        ax1.axhline(y=self.promised_download, color='red', linestyle='-', label="Promised Download Speed")
        ax1.axhline(y=self.promised_upload, color='red', linestyle='--', label="Promised Upload Speed")

        # Labels and title
        plt.xlabel('Dates', labelpad=15)
        plt.ylabel('Speed Mbps', labelpad=15)
        plt.title('Internet Speed Trends For the Last 7 Days', pad=20, fontsize=20)
        plt.legend()

        # Save the plot
        plt.tight_layout()
        plt.savefig(f"7-days-graph-{datetime.now().date()}.png")

    def check_data_and_plot(self):
        # the program to make graphs once a day --> every 4 iterations of main code.
        if len(self.data) % 4 == 0:
            df = pd.DataFrame(self.data)  # Convert the list to DataFrame directly without transpose
            self.plot_graph(df)

