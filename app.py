import streamlit as st
import pandas as pd
from datetime import date
from services import SalesService
import altair as alt
import calendar

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Initialize the sales service
sales_service = SalesService()

def show_daily_sales():
    # User input
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=date(2009, 1, 1),
            key="daily_start_date"
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=date(2009, 12, 31),
            min_value=start_date,
            key="daily_end_date"
        )
    
    if st.button("Get Daily Sales"):
        try:
            with st.spinner('Fetching data...'):
                # Fetch data for selected range
                df = sales_service.get_daily_sales(
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d")
                )
                
                if df.empty:
                    st.warning("No data available for the selected date range.")
                    return
                
                # Process data
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                df = df.dropna(subset=['date'])
                df['total_sales_millions'] = df['total_sales'] / 1_000_000
                df = df.sort_values(by="date")
                
                # Create title with date range
                title = f"📅 Daily Sales Trend ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})"
                
                # Create Altair chart
                chart = alt.Chart(df).mark_line(point=True).encode(
                    x=alt.X('date:T', 
                           title='Date',
                           axis=alt.Axis(format='%Y-%m-%d', labelAngle=45)),
                    y=alt.Y('total_sales_millions:Q',
                           title='Total Sales (Millions $)',
                           scale=alt.Scale(
                               domain=[
                                   df['total_sales_millions'].min() * 0.98,
                                   df['total_sales_millions'].max() * 1.02
                               ]
                           ),
                           axis=alt.Axis(format='$,.4f')),
                    tooltip=[
                        alt.Tooltip('date:T', title='Date', format='%Y-%m-%d'),
                        alt.Tooltip('total_sales_millions:Q', title='Sales (M)', format='$,.4f'),
                        alt.Tooltip('day_of_week:N', title='Day'),
                        alt.Tooltip('store_count:Q', title='Stores'),
                        alt.Tooltip('product_count:Q', title='Products')
                    ]
                ).properties(
                    title=title,
                    height=500
                ).configure_point(
                    size=100
                ).interactive()
                
                # Display the chart
                st.altair_chart(chart, use_container_width=True)
                
                # Stats
                st.subheader("📊 Summary Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Min Sales", f"${df['total_sales_millions'].min():.2f}M")
                with col2:
                    st.metric("Avg Sales", f"${df['total_sales_millions'].mean():.2f}M")
                with col3:
                    st.metric("Max Sales", f"${df['total_sales_millions'].max():.2f}M")
                
                # Raw data
                with st.expander("📄 Show Raw Data"):
                    st.dataframe(df)
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Check if API is reachable.")

def show_monthly_sales():
    # Year selection
    selected_year = st.selectbox(
        "Select Year",
        options=range(2007, 2009),
        key="monthly_year_select"
    )
    
    if st.button("Get Monthly Sales"):
        try:
            with st.spinner('Fetching data...'):
                # Fetch yearly data
                response = sales_service.get_monthly_sales(selected_year)
                
                if not response or 'monthly_data' not in response:
                    st.warning("No data available for the selected year.")
                    return
                
                # Convert monthly data to DataFrame
                df = pd.DataFrame(response['monthly_data'])
                
                # Convert sales to millions for better readability
                df['total_sales_millions'] = df['total_sales'] / 1_000_000
                
                # Create title
                title = f"📅 Monthly Sales for {selected_year}"
                
                # Create Altair chart for monthly sales
                sales_chart = alt.Chart(df).mark_line(point=True).encode(
                    x=alt.X('month:N', 
                           title='Month',
                           sort=None),  # Preserve month order
                    y=alt.Y('total_sales_millions:Q',
                           title='Total Sales (Millions $)',
                           scale=alt.Scale(
                               domain=[
                                   df['total_sales_millions'].min() * 0.98,
                                   df['total_sales_millions'].max() * 1.02
                               ]
                           ),
                           axis=alt.Axis(format='$,.2f')),
                    tooltip=[
                        alt.Tooltip('month:N', title='Month'),
                        alt.Tooltip('total_sales_millions:Q', title='Sales (M)', format='$,.2f'),
                        alt.Tooltip('store_count:Q', title='Stores'),
                        alt.Tooltip('product_count:Q', title='Products'),
                        alt.Tooltip('avg_sale_amount:Q', title='Avg Sale', format='$,.2f')
                    ]
                ).properties(
                    title=title,
                    height=400
                ).configure_point(
                    size=100
                ).interactive()
                
                # Create line chart for store and product count trends
                metrics_df = pd.melt(df, 
                                   id_vars=['month'], 
                                   value_vars=['store_count', 'product_count'],
                                   var_name='metric',
                                   value_name='count')
                
                metrics_chart = alt.Chart(metrics_df).mark_line(point=True).encode(
                    x=alt.X('month:N', 
                           title='Month',
                           sort=None),
                    y=alt.Y('count:Q',
                           title='Count'),
                    color=alt.Color('metric:N', 
                                  title='Metric',
                                  legend=alt.Legend(
                                      title=None,
                                      orient='top')),
                    tooltip=[
                        alt.Tooltip('month:N', title='Month'),
                        alt.Tooltip('metric:N', title='Metric'),
                        alt.Tooltip('count:Q', title='Count')
                    ]
                ).properties(
                    title='Store and Product Count Trends',
                    height=300
                ).interactive()
                
                # Display the charts
                st.altair_chart(sales_chart, use_container_width=True)
                st.altair_chart(metrics_chart, use_container_width=True)
                
                # Yearly Summary
                st.subheader("📊 Yearly Summary")
                
                # Sales metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Yearly Sales", 
                             f"${response['total_yearly_sales']/1_000_000:.2f}M")
                with col2:
                    st.metric("Average Monthly Sales", 
                             f"${(response['total_yearly_sales']/12)/1_000_000:.2f}M")
                with col3:
                    st.metric("Peak Month", 
                             f"{df.loc[df['total_sales'].idxmax(), 'month']}")
                
                # Store and Product metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Store Count (End of Year)", 
                             f"{df.iloc[-1]['store_count']}")
                with col2:
                    st.metric("Product Count (End of Year)", 
                             f"{df.iloc[-1]['product_count']}")
                with col3:
                    avg_sale = df['avg_sale_amount'].mean()
                    st.metric("Average Sale Amount", 
                             f"${avg_sale:.2f}")
                
                # Raw data
                with st.expander("📄 Show Raw Data"):
                    st.dataframe(df.style.format({
                        'total_sales': '${:,.2f}',
                        'avg_sale_amount': '${:,.2f}'
                    }))
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Check if API is reachable.")

def show_sales_prediction():
    st.subheader("🔮 Sales Prediction")
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        min_date = st.date_input(
            "Start Date",
            value=date(2009, 1, 1),
            key="prediction_start_date"
        )
    with col2:
        max_date = st.date_input(
            "End Date",
            value=date(2009, 1, 31),
            min_value=min_date,
            key="prediction_end_date"
        )
    
    if st.button("Get Sales Prediction"):
        try:
            with st.spinner('Fetching predictions...'):
                # Fetch prediction data
                df = sales_service.get_sales_prediction(
                    min_date.strftime("%Y-%m-%d"),
                    max_date.strftime("%Y-%m-%d")
                )
                
                if df.empty:
                    st.warning("No predictions available for the selected date range.")
                    return
                
                # Convert sales to thousands for better readability
                df['predicted_sales_k'] = df['predicted_sales'] / 1000
                
                # Create title
                title = f"🔮 Sales Predictions ({min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')})"
                
                # Create Altair chart
                chart = alt.Chart(df).mark_line(
                    point=True,
                    strokeDash=[6, 3],  # Creates dotted line
                    color='#8A2BE2'  # Purple color (BlueViolet)
                ).encode(
                    x=alt.X('date:T', 
                           title='Date',
                           axis=alt.Axis(format='%Y-%m-%d', labelAngle=45)),
                    y=alt.Y('predicted_sales_k:Q',
                           title='Predicted Sales (Thousands $)',
                           scale=alt.Scale(
                               domain=[
                                   df['predicted_sales_k'].min() * 0.98,
                                   df['predicted_sales_k'].max() * 1.02
                               ]
                           ),
                           axis=alt.Axis(format='$,.2f')),
                    tooltip=[
                        alt.Tooltip('date:T', title='Date', format='%Y-%m-%d'),
                        alt.Tooltip('predicted_sales_k:Q', title='Predicted Sales (K)', format='$,.2f')
                    ]
                ).properties(
                    title=title,
                    height=500
                ).configure_point(
                    size=100,
                    color='#8A2BE2'  # Match points color with line
                ).interactive()
                
                # Display the chart
                st.altair_chart(chart, use_container_width=True)
                
                # Summary statistics
                st.subheader("📊 Prediction Summary")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Min Predicted Sales", 
                             f"${df['predicted_sales'].min()/1000:.2f}K")
                with col2:
                    st.metric("Avg Predicted Sales", 
                             f"${df['predicted_sales'].mean()/1000:.2f}K")
                with col3:
                    st.metric("Max Predicted Sales", 
                             f"${df['predicted_sales'].max()/1000:.2f}K")
                
                # Raw data
                with st.expander("📄 Show Raw Data"):
                    st.dataframe(df.style.format({
                        'predicted_sales': '${:,.2f}',
                        'predicted_sales_k': '${:,.2f}K'
                    }))
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Check if prediction API is reachable.")

def main():
    st.title("📊 Sales Dashboard")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Daily Sales", "Monthly Sales", "Sales Prediction"])
    
    with tab1:
        show_daily_sales()
    
    with tab2:
        show_monthly_sales()
        
    with tab3:
        show_sales_prediction()

if __name__ == "__main__":
    main()
