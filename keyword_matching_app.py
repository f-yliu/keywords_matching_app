import streamlit as st
import pandas as pd
import re

# core funcs
def add_matching_term(df, keyword_file):
    with open(keyword_file, 'r') as file:
        keywords = file.read().splitlines()

    # Function to check if Legal Name contains any keyword
    def check_keywords(legal_name):
        for keyword in keywords:
            # Use regular expression with word boundaries to match complete words only
            if re.search(r'\b{}\b'.format(re.escape(keyword)), legal_name, flags=re.IGNORECASE):
                return keyword
        return None

    # Apply the function to the 'Legal Name' column to identify matching terms
    # remove the extra dots for better matching
    df['Legal Name'] = df['Legal Name'].str.replace('.', '')
    df['matching_term'] = df['Legal Name'].apply(check_keywords)
    return df

# Main Streamlit code
def main():
    st.title('Keyword Matching App')

    # Sidebar - File Upload
    st.sidebar.title('Upload Files')
    uploaded_xlsx = st.sidebar.file_uploader('Upload .xlsx file', type=['xlsx'])
    uploaded_txt = st.sidebar.file_uploader('Upload keywords .txt file', type=['txt'])

    # Sidebar - Display keywords
    st.sidebar.title('Keywords')
    if uploaded_txt is not None:
        keywords = uploaded_txt.getvalue().decode('utf-8').splitlines()
        for keyword in keywords:
            st.sidebar.write(keyword)

    # Main Section - Process uploaded files
    if uploaded_xlsx is not None and uploaded_txt is not None:
        processing_msg = st.empty()
        processing_msg.info("Please wait while the processing is running...")
        df = pd.read_excel(uploaded_xlsx)
        df_processed = add_matching_term(df, uploaded_txt.name)
        processing_msg.empty()
        processing_msg.success("Processing completed!")
        st.write(df_processed)

        # Download button for processed DataFrame
        st.download_button(
            label='Download CSV',
            data=df_processed.to_csv(index=False),
            file_name='processed_data.csv',
            mime='text/csv'
        )

if __name__ == '__main__':
    main()
