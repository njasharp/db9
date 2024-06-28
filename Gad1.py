import streamlit as st
import pandas as pd
import plotly.express as px

# Hide Streamlit menu and footer
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        body {background-color: #212121;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Radio button for selecting the dataset
dataset_options = ["United-Arab-Emirates", "Saudi Arabia", "Egypt", "Iraq", "Morocco"]
selected_dataset = st.sidebar.radio("Select Dataset", options=dataset_options)

# Sidebar range slider for selecting the range of items to display
range_slider = st.sidebar.slider("Select rank range", 0, 50, (0, 20))

# File uploader for CSV in the sidebar (moved to bottom)
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Load the appropriate default data based on the selected dataset
if selected_dataset == "Saudi Arabia":
    default_csv_path = 'extracted_Saudi Arabia.csv'
elif selected_dataset == "Egypt":
    default_csv_path = 'extracted_Egypt.csv'
elif selected_dataset == "Iraq":
    default_csv_path = 'extracted_Iraq.csv'
elif selected_dataset == "Morocco":
    default_csv_path = 'extracted_Morocco.csv'
else:
    default_csv_path = 'extracted_uae.csv'

data = pd.read_csv(default_csv_path, encoding='latin1')

if uploaded_file is not None:
    # Load the CSV file
    data = pd.read_csv(uploaded_file, encoding='latin1')
    st.write("Data Preview:")
    st.write(data.head())
else:
    st.sidebar.write("Using default data.")

# Strip any leading/trailing whitespace from column names
data.columns = data.columns.str.strip()

# Get unique regions for the radio button options
regions = data['Region'].unique()

# Sidebar radio button for selecting the region
selected_region = st.sidebar.radio("Select Region", options=regions)

# Filter data by selected region
filtered_data = data[data['Region'] == selected_region]

# Data processing and visualization
st.title(f'Top Ranked Games by Category in {selected_region}')

# Filter data by category
free_games = filtered_data[filtered_data['Type'].str.contains('Free', case=False)].sort_values(by='Rank')
paid_games = filtered_data[filtered_data['Type'].str.contains('Paid', case=False)].sort_values(by='Rank')
top_grossing_games = filtered_data[filtered_data['Type'].str.contains('Grossing', case=False)].sort_values(by='Rank')

def create_chart(title, dataset, start, end):
    dataset = dataset.iloc[start:end]
    dataset['Reversed Rank'] = dataset['Rank'].max() - dataset['Rank'] + 1
    fig = px.bar(
        dataset,
        y='Title',
        x='Reversed Rank',
        orientation='h',
        title=title,
        labels={'Reversed Rank': 'Rank (1 = Best, 50 = Least Good)', 'Title': 'Game Title'},
        color='Rank',
        color_continuous_scale='Viridis',
        hover_data=['Region']
    )
    fig.update_coloraxes(reversescale=True)
    fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),
        title_font=dict(size=24, color='white', family="Arial"),
        xaxis=dict(title='Rank', showgrid=False, zeroline=False),
        yaxis=dict(title='Game Title', showgrid=False, zeroline=False),
        coloraxis_colorbar=dict(title='Rank (1 = Best, 50 = Least Good)')
    )
    fig.update_yaxes(dtick=1, tickfont=dict(size=10))  # Adjust font size for y-axis labels
    
    # Add rank number to the right of each bar
    fig.update_traces(texttemplate='%{text}', textposition='outside', text=dataset['Rank'])
    return fig

# Get the range values
start, end = range_slider

# Create and display charts
st.plotly_chart(create_chart('Top Free Games', free_games, start, end))
st.plotly_chart(create_chart('Top Paid Games', paid_games, start, end))

# Check if top_grossing_games is empty
if not top_grossing_games.empty:
    st.plotly_chart(create_chart('Top Grossing Games', top_grossing_games, start, end))
else:
    st.write("No data available for Top Grossing Games.")

# Additional visualizations and analyses can be added here as needed
st.header(f'{selected_region}')
st.markdown("#### Top 50 Matrix")
st.write(data)
st.info("Built by DW v1.2 6-27-24")