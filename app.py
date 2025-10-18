import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Startup Funding Analysis', page_icon=':bar_chart:', layout='wide')

df = pd.read_csv('startup_cleaned.csv')
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['year'] = df['Date'].dt.year
df['month'] = df['Date'].dt.month

def load_investor_details(investor):
    st.title(f'Investor: {investor}')
    recent_investments = df[df['Investors Name'].str.contains(investor)][['Date','Startup Name','Industry Vertical','City','Investment Type','Amount in Cr']].head()
    st.subheader('Recent Investments')
    st.dataframe(recent_investments)

    col1 , col2 = st.columns(2)
    with col1:
        biggest_investments =  df[df['Investors Name'].str.contains(investor)].groupby('Startup Name')['Amount in Cr'].sum().sort_values(ascending=False).head(3)
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(biggest_investments.index, biggest_investments.values)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    with col2:
        vertical_series = (df[df['Investors Name'].str.contains(investor, case=False, na=False)].groupby('Industry Vertical')['Amount in Cr'].sum().sort_values(ascending=False))
        threshold = 0.03 * vertical_series.sum()  # 3% threshold
        others = vertical_series[vertical_series < threshold].sum()
        vertical_series = vertical_series[vertical_series >= threshold]
        vertical_series['Others'] = others

        fig1, ax1 = plt.subplots(figsize=(6, 6))
        ax1.pie(
            vertical_series,
            labels=vertical_series.index,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 8},
        )
        ax1.axis('equal')

        st.subheader('Investment by Industry Vertical')
        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:
        type_series = (df[df['Investors Name'].str.contains(investor, case=False, na=False)].groupby('Investment Type')['Amount in Cr'].sum().sort_values(ascending=False))
        threshold = 0.03 * type_series.sum()  # 3% threshold
        others = type_series[type_series < threshold].sum()
        type_series = type_series[type_series >= threshold]
        type_series['Others'] = others

        fig2, ax1 = plt.subplots(figsize=(6, 6))
        ax1.pie(
            type_series,
            labels=type_series.index,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 8},
        )
        ax1.axis('equal')

        st.subheader('Investment by Type')
        st.pyplot(fig2)

    with col4:
        city_series = (df[df['Investors Name'].str.contains(investor, case=False, na=False)].groupby('City')['Amount in Cr'].sum().sort_values(ascending=False))
        threshold = 0.03 * city_series.sum()  # 3% threshold
        others = city_series[city_series < threshold].sum()
        city_series = city_series[city_series >= threshold]
        city_series['Others'] = others

        fig3, ax1 = plt.subplots(figsize=(6, 6))
        ax1.pie(
            city_series,
            labels=city_series.index,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 8},
        )
        ax1.axis('equal')

        st.subheader('Investment by City')
        st.pyplot(fig3)

    yearly_series =  df[df['Investors Name'].str.contains('investor')].groupby('year')['Amount in Cr'].sum() 
    st.subheader('Investment Over the Years')
    fig4, ax4 = plt.subplots()
    ax4.plot(yearly_series.index, yearly_series.values)
    plt.xticks(yearly_series.index, rotation=45)
    st.pyplot(fig4)

    # Similar Investors
    st.subheader('Similar Investors')
    invested_startups = df[df['Investors Name'].str.contains(investor)]['Startup Name'].unique()
    similar_investors = df[df['Startup Name'].isin(invested_startups) & ~df['Investors Name'].str.contains(investor)]['Investors Name'].unique()
    st.write(similar_investors)


def load_overall_analysis():
    st.title('Overall Analysis of Startup Funding')
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        #Total Investments  
        total_investment = df['Amount in Cr'].sum()
        st.metric('Total Investment (in Cr)', f'{total_investment:,.2f}')
    with col2:
        #Maximum Amount Infused in a Startup
        max_investment = df.groupby('Startup Name')['Amount in Cr'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Maximum Amount Infused in a Startup (in Cr)', f'{max_investment:,.2f}')
    with col3:
        #Average Amount Infused in a Startup
        avg_investment = df.groupby('Startup Name')['Amount in Cr'].sum().mean()
        st.metric('Average Amount Infused in a Startup (in Cr)', f'{avg_investment:,.2f}')
    with col4:
        #Number of Startups Funded
        num_startups = df['Startup Name'].nunique()
        st.metric('Number of Startups Funded', f'{num_startups}')

    st.header('Month on Month Investment Analysis')
    selected = st.selectbox('Select Type', ['Total', 'Count'])
    if selected == 'Total':
        temp_df = df.groupby(['year', 'month'])['Amount in Cr'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['Amount in Cr'].count().reset_index()
    # Combine month and year for x-axis
    temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)
    # Create a larger figure
    fig, ax = plt.subplots(figsize=(12, 6))
    # Plot with markers
    ax.plot(temp_df['x_axis'], temp_df['Amount in Cr'], marker='o', linewidth=2)
    # Label settings
    plt.xticks(rotation=45, ha='right')
    # Optionally, show every 2nd label if too many months
    if len(temp_df) > 10:
        ax.set_xticks(temp_df['x_axis'][::2])
    # Add labels and grid
    ax.set_xlabel('Month-Year')
    ax.set_ylabel('Amount in Cr' if selected == 'Total' else 'Count')
    ax.set_title(f'Month on Month Investment ({selected})')
    ax.grid(True, linestyle='--', alpha=0.5)
    # Adjust layout
    plt.tight_layout()
    # Display plot
    st.pyplot(fig)

    # Sector Analysis Pie chart (Sum and Count)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Investment by Industry Vertical (Sum)')
        vertical_series = df.groupby('Industry Vertical')['Amount in Cr'].sum().sort_values(ascending=False)
        threshold = 0.03 * vertical_series.sum()  # 3% threshold
        others = vertical_series[vertical_series < threshold].sum()
        vertical_series = vertical_series[vertical_series >= threshold]
        vertical_series['Others'] = others

        fig1, ax1 = plt.subplots(figsize=(6, 6))
        ax1.pie(
            vertical_series,
            labels=vertical_series.index,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 8},
        )
        ax1.axis('equal')
        st.pyplot(fig1)
    with col2:
        st.subheader('Investment by Industry Vertical (Count)')
        vertical_series_count = df.groupby('Industry Vertical')['Amount in Cr'].count().sort_values(ascending=False)
        threshold = 0.03 * vertical_series_count.sum()  # 3% threshold
        others = vertical_series_count[vertical_series_count < threshold].sum()
        vertical_series_count = vertical_series_count[vertical_series_count >= threshold]
        vertical_series_count['Others'] = others

        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.pie(
            vertical_series_count,
            labels=vertical_series_count.index,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 8},
        )
        ax2.axis('equal')
        st.pyplot(fig2)

    # Type of funding
    col3, col4 = st.columns(2)
    with col3:
        st.subheader('Investment by Type (Sum)')
        type_series = df.groupby('Investment Type')['Amount in Cr'].sum().sort_values(ascending=False)
        threshold = 0.03 * type_series.sum()  # 3% threshold
        others = type_series[type_series < threshold].sum()
        type_series = type_series[type_series >= threshold]
        type_series['Others'] = others

        fig3, ax3 = plt.subplots(figsize=(6, 6))
        ax3.pie(
            type_series,
            labels=type_series.index,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 8},
        )
        ax3.axis('equal')
        st.pyplot(fig3)
    with col4:
        st.subheader('Investment by Type (Count)')
        type_series_count = df.groupby('Investment Type')['Amount in Cr'].count().sort_values(ascending=False)
        threshold = 0.03 * type_series_count.sum()  # 3% threshold
        others = type_series_count[type_series_count < threshold].sum()
        type_series_count = type_series_count[type_series_count >= threshold]
        type_series_count['Others'] = others

        fig4, ax4 = plt.subplots(figsize=(6, 6))
        ax4.pie(
            type_series_count,
            labels=type_series_count.index,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 8},
        )
        ax4.axis('equal')
        st.pyplot(fig4)

        # City-wise Funding
    st.header('City-wise Funding')
    city_df = df.groupby('City')['Amount in Cr'].sum().sort_values(ascending=False).head(10)
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    ax5.barh(city_df.index[::-1], city_df.values[::-1], color='skyblue')
    ax5.set_xlabel('Total Funding (in Cr)')
    ax5.set_title('Top 10 Cities by Total Funding')
    plt.tight_layout()
    st.pyplot(fig5)

    # Top Startups (Year-wise and Overall)
    st.header('Top Funded Startups')
    year_list = sorted(df['year'].dropna().unique())
    selected_year = st.selectbox('Select Year', ['Overall'] + list(map(str, year_list)))

    if selected_year == 'Overall':
        top_startups = df.groupby('Startup Name')['Amount in Cr'].sum().sort_values(ascending=False).head(10)
        st.subheader('Top 10 Startups (Overall)')
    else:
        temp = df[df['year'] == int(selected_year)]
        top_startups = temp.groupby('Startup Name')['Amount in Cr'].sum().sort_values(ascending=False).head(10)
        st.subheader(f'Top 10 Startups in {selected_year}')

    fig6, ax6 = plt.subplots(figsize=(10, 5))
    ax6.barh(top_startups.index[::-1], top_startups.values[::-1], color='lightgreen')
    ax6.set_xlabel('Total Funding (in Cr)')
    plt.tight_layout()
    st.pyplot(fig6)

    # Top Investors
    st.header('Top Investors')
    investor_df = df.groupby('Investors Name')['Amount in Cr'].sum().sort_values(ascending=False).head(10)
    fig7, ax7 = plt.subplots(figsize=(10, 5))
    ax7.barh(investor_df.index[::-1], investor_df.values[::-1], color='lightcoral')
    ax7.set_xlabel('Total Funding (in Cr)')
    ax7.set_title('Top 10 Investors by Total Funding')
    plt.tight_layout()
    st.pyplot(fig7)

    # Funding Heatmap (Month vs Year)
    st.header('Funding Heatmap (Month vs Year)')
    pivot_df = df.pivot_table(
        index='year',
        columns='month',
        values='Amount in Cr',
        aggfunc='sum'
    ).fillna(0)

    fig8, ax8 = plt.subplots(figsize=(10, 6))
    import seaborn as sns
    sns.heatmap(pivot_df, cmap='YlGnBu', annot=True, fmt='.0f', ax=ax8)
    ax8.set_title('Funding Distribution Heatmap (in Cr)')
    st.pyplot(fig8)



def load_startup_details(startup):
    st.title(f'StartUp Analysis')
    
    #Name of the Startup
    startup_df = df[df['Startup Name'] == startup]
    st.markdown(f"**Startup Name:** {startup}")

    # Industry Vertical
    industry = startup_df['Industry Vertical'].values[0]
    st.markdown(f"**Industry Vertical:** {industry}")

    #Sub Industry
    sub_industry = startup_df['SubVertical'].values[0]
    st.markdown(f"**Sub Industry:** {sub_industry}")

    # Location
    location = startup_df['City'].values[0]
    st.markdown(f"**Location:** {location}")

    # Funding Rounds(Stage, Investors, Date)
    st.subheader('Funding Rounds')
    funding_rounds = startup_df[['Date','Investment Type','Investors Name','Amount in Cr']].sort_values(by='Date', ascending=False)
    st.dataframe(funding_rounds)

    # Similar Startups
    st.subheader('Similar Startups')
    similar_startups = df[(df['Industry Vertical'] == industry) & (df['Startup Name'] != startup)]['Startup Name'].unique()
    st.write(similar_startups)

    

st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select Analysis Type', ['Overall Analysis', 'StartUp', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    selected_startup = st.sidebar.selectbox('Select StartUp', sorted(df['Startup Name'].unique()))
    if st.sidebar.button('Find StartUp Details'):
        load_startup_details(selected_startup)

else:
    investor_list = sorted(set(df['Investors Name'].dropna().str.split(',').sum()))
    selected_investor = st.sidebar.selectbox('Select Investor', investor_list)
    if st.sidebar.button('Find Investor Details'):
        load_investor_details(selected_investor)