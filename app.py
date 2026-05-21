import os
import streamlit as st
from datetime import datetime


st.set_page_config(
    page_title="File Metadata Uploader",
    page_icon="📁",
    layout="centered"
)


if "metadata_db" not in st.session_state:
    st.session_state.metadata_db = []


MAX_FILE_SIZE_MB = 5  
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024 



def load_external_files():
    """Reads HTML and CSS components into the application."""
    try:
        with open("static/style.css", "r") as css_file:
            css_content = css_file.read()
            
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
            
        with open("static/header.html", "r") as html_file:
            html_content = html_file.read()
            st.markdown(html_content, unsafe_allow_html=True)
    except FileNotFoundError as e:
        st.error(f"Missing required static asset file: {e.filename}")


load_external_files()


st.info(f"💡 **Note:** File bytes are skipped entirely. Maximum simulated file upload size is set to **{MAX_FILE_SIZE_MB} MB**.")



uploaded_file = st.file_uploader(
    "Choose a file to extract metadata...", 
    type=None, 
    accept_multiple_files=False
)

if uploaded_file is not None:
    file_size_bytes = uploaded_file.size
    
    
    if file_size_bytes > MAX_FILE_SIZE_BYTES:
        st.error(f"❌ Error: File size exceeds the maximum allowed limit of {MAX_FILE_SIZE_MB}MB.")
    else:
        # Extract metadata
        file_name = uploaded_file.name
        file_type = uploaded_file.type if uploaded_file.type else "Unknown / Extension Missing"
        uploaded_at = datetime.now().strftime("%d-%b-%Y %I:%M:%S %p")
        
        file_record = {
            "name": file_name,
            "size": f"{file_size_bytes / 1024:.2f} KB",
            "type": file_type,
            "uploaded_at": uploaded_at
        }
        
        
        is_duplicate = any(
            record["name"] == file_record["name"] and record["size"] == file_record["size"] 
            for record in st.session_state.metadata_db
        )
        
        if not is_duplicate:
            st.session_state.metadata_db.append(file_record)
            st.success(f"🎉 Successfully captured metadata for: **{file_name}**")



st.markdown("---")
st.subheader("📋 Historical Uploaded Metadata Logs")

if len(st.session_state.metadata_db) == 0:
    st.info("No file logs recorded in this session yet.")
else:
    
    for record in reversed(st.session_state.metadata_db):
        card_html = f"""
        <div class="metadata-card">
            <div class="file-name">📄 {record['name']}</div>
            <div class="meta-details">
                <div class="meta-item"><strong>Size:</strong> {record['size']}</div>
                <div class="meta-item"><strong>MIME Type:</strong> {record['type']}</div>
                <div class="meta-item"><strong>Uploaded At:</strong> {record['uploaded_at']}</div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    
    if st.button("Clear History Logs", type="secondary"):
        st.session_state.metadata_db = []
        st.rerun()