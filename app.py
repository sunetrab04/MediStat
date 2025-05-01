import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Set up the page layout and title with improved styling
st.set_page_config(
    page_title="MediStat - Medical Data Analyzer", 
    layout="wide",
    page_icon="🧬"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .main {background-color: #f9f9f9;}
        .stButton>button {border-radius: 8px; padding: 8px 16px;}
        .stDownloadButton>button {background-color: #4CAF50; color: white;}
        .stSelectbox, .stSlider {padding: 8px; border-radius: 6px;}
        .stDataFrame {border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);}
        .stMarkdown h1 {color: #2e7d32; margin-top: 0;}
        .stMarkdown h2 {color: #388e3c; border-bottom: 2px solid #e0e0e0; padding-bottom: 8px; margin-top: 1.5rem;}
        .info-box {background-color: #00008B; padding: 16px; border-radius: 8px; margin-bottom: 16px;}
        .metric-box {background-color: #00008B; border-radius: 8px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 8px;}
        .stTabs [data-baseweb="tab-list"] {gap: 8px;}
        .stTabs [data-baseweb="tab"] {padding: 8px 16px; border-radius: 8px;}
        .stTabs [aria-selected="true"] {background-color: #e8f5e9;}
        .stSidebar [data-testid="stVerticalBlock"] {gap: 16px;}
        .st-expander {margin-bottom: 16px;}
    </style>
""", unsafe_allow_html=True)

# Header with better visual hierarchy
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://img.icons8.com/color/96/medical-doctor.png", width=80)
with col2:
    st.title("MediStat - Medical Research Data Analyzer")
    st.caption("Advanced analytics for cardiovascular health research")

# Add Biocontrol System Insights section in an expandable container
with st.expander("🔬 Biocontrol System Insights - Click to expand", expanded=True):
    st.markdown("""
    <div class="info-box">
        <h4 style="color: white; margin-top: 0;">Understanding Biological Control Systems</h4>
        <ul style="color: white;">
            <li>A biocontrol system maintains physiological variables (like heart rate or glucose) within healthy ranges</li>
            <li>This app mimics such behavior using control logic to simulate feedback (like Proportional Control)</li>
            <li>Visualize how risk metrics respond to age, BP, and cholesterol — similar to biological regulation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# File upload section with improved visual feedback
st.markdown("## 📂 Data Upload & Processing")
uploaded_file = st.file_uploader(
    "Upload your CSV file for analysis", 
    type="csv",
    help="Please upload a CSV file containing medical research data with columns like 'sex', 'cp', and 'num'"
)

if uploaded_file is not None:
    # Try loading the file with better error handling
    with st.spinner("Processing your data..."):
        try:
            df = pd.read_csv(uploaded_file)
            st.success("Data loaded successfully!")
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.stop()

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Sidebar with improved organization
    with st.sidebar:
        st.markdown("## 🛠️ Analysis Controls")
        
        # Show column names in a more organized way
        with st.expander("📋 Data Columns"):
            st.write(df.columns.tolist())
        
        # Check for essential columns with better visual feedback
        required_cols = ['sex', 'cp', 'num']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {', '.join(missing_cols)}")
            st.stop()
        
        # Drop rows with NaN in important columns
        df_clean = df.dropna(subset=required_cols)
        
        # Filters section with better labels
        st.markdown("### 🔍 Data Filters")
        sex_choice = st.selectbox(
            "Select Gender",
            ["All"] + df_clean['sex'].dropna().unique().tolist(),
            help="Filter data by gender"
        )
        cp_choice = st.selectbox(
            "Select Chest Pain Type",
            ["All"] + df_clean['cp'].dropna().unique().tolist(),
            help="Filter data by type of chest pain"
        )
        
        # Apply filters
        filtered_df = df_clean.copy()
        if sex_choice != "All":
            filtered_df = filtered_df[filtered_df['sex'] == sex_choice]
        if cp_choice != "All":
            filtered_df = filtered_df[filtered_df['cp'] == cp_choice]
        
        # Show filter summary
        st.markdown(f"**Filtered Data:** {len(filtered_df)} records")
    
    # Main content area with tabbed interface for better organization
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Data", "📈 Visualizations", "🔍 Insights", "📄 Report"])
    
    with tab1:
        st.markdown("### Raw Data Preview")
        st.dataframe(df_clean.style.background_gradient(cmap='Blues'), use_container_width=True)
        
        st.markdown("### Filtered Data View")
        st.dataframe(filtered_df.style.background_gradient(cmap='Greens'), use_container_width=True)
    
    with tab2:
        # Plot disease distribution ('num')
        st.markdown("### Disease Diagnosis Distribution")
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        filtered_df['num'].value_counts().sort_index().plot(kind='bar', color='#4CAF50', ax=ax1)
        ax1.set_xlabel("Diagnosis Code", fontsize=12)
        ax1.set_ylabel("Count", fontsize=12)
        ax1.set_title("Number of Patients per Diagnosis", fontsize=14)
        plt.tight_layout()
        st.pyplot(fig1)
        
        # Comparison of Age Distribution by Gender
        st.markdown("### Age Distribution by Gender")
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        sns.histplot(filtered_df, x='age', hue='sex', kde=True, palette=['#FF6D00', '#2962FF'], ax=ax2)
        ax2.set_title("Age Distribution by Gender", fontsize=14)
        ax2.set_xlabel("Age", fontsize=12)
        ax2.set_ylabel("Count", fontsize=12)
        plt.tight_layout()
        st.pyplot(fig2)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Chest Pain Type vs Disease Diagnosis
            st.markdown("### Chest Pain Type vs Diagnosis")
            fig3, ax3 = plt.subplots(figsize=(8, 5))
            sns.countplot(data=filtered_df, x='cp', hue='num', palette='viridis', ax=ax3)
            ax3.set_title("Chest Pain Type vs Disease Diagnosis", fontsize=12)
            plt.tight_layout()
            st.pyplot(fig3)
        
        with col2:
            # Average Age per Chest Pain Type
            st.markdown("### Average Age by Chest Pain")
            fig4, ax4 = plt.subplots(figsize=(8, 5))
            sns.barplot(x='cp', y='age', data=filtered_df, palette='coolwarm', ax=ax4)
            ax4.set_title("Average Age per Chest Pain Type", fontsize=12)
            plt.tight_layout()
            st.pyplot(fig4)
    
    with tab3:
        st.markdown("## 🔑 Key Insights")
        
        # Metrics in cards
        min_age = filtered_df['age'].min()
        peak_age = filtered_df['age'].mode()[0]
        gender_dist = filtered_df['sex'].value_counts(normalize=True) * 100
        cp_dist = filtered_df['cp'].value_counts()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <h4 style="color: white; margin-top: 0;">👨‍⚕️ Gender Distribution</h4>
                <p style="color: white; margin-bottom: 4px;">Male: {gender_dist.get(1, 0):.1f}%</p>
                <p style="color: white; margin-bottom: 0;">Female: {gender_dist.get(0, 0):.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-box">
                <h4 style="color: white; margin-top: 0;">📊 Age Statistics</h4>
                <p style="color: white; margin-bottom: 4px;">Min Age: {min_age}</p>
                <p style="color: white; margin-bottom: 4px;">Peak Age: {peak_age}</p>
                <p style="color: white; margin-bottom: 0;">Mean Age: {filtered_df['age'].mean():.1f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-box">
                <h4 style="color: white; margin-top: 0;">💓 Chest Pain Types</h4>
                <p style="color: white; margin-bottom: 4px;">Asymptomatic: {cp_dist.get(0, 0)}</p>
                <p style="color: white; margin-bottom: 4px;">Atypical Angina: {cp_dist.get(1, 0)}</p>
                <p style="color: white; margin-bottom: 4px;">Non-Anginal: {cp_dist.get(2, 0)}</p>
                <p style="color: white; margin-bottom: 0;">Typical Angina: {cp_dist.get(3, 0)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed insights in expandable sections
        with st.expander("📌 Demographic Insights"):
            st.markdown(f"""
            - Minimum age for heart disease: **{min_age} years**
            - Peak age for heart disease: **{peak_age} years**
            - Most cases occur at age **54-55** for both males and females
            - Significant variation in male numbers across regions
            """)
        
        with st.expander("📌 Clinical Metrics"):
            st.markdown(f"""
            - Mean Cholesterol level: **{filtered_df['chol'].mean():.2f} mg/dL**
            - Mean Resting Blood Pressure: **{filtered_df['trestbps'].mean():.2f} mmHg**
            - Highest number of individuals from Cleveland
            - Lowest number from Switzerland
            """)
    
    with tab4:
        st.markdown("## 📄 Generate Report")
        
        # Enhanced PDF generation with more options
        with st.form("report_form"):
            st.markdown("Select report options:")
            include_data = st.checkbox("Include raw data summary", True)
            include_stats = st.checkbox("Include statistical analysis", True)
            include_plots = st.checkbox("Include visualizations", True)
            report_title = st.text_input("Report title", "Medical Data Analysis Report")
            
            if st.form_submit_button("Generate PDF Report"):
                with st.spinner("Generating report..."):
                    # PDF generation function
                    def generate_pdf():
                        pdf_buffer = BytesIO()
                        c = canvas.Canvas(pdf_buffer, pagesize=letter)
                        
                        # Title page
                        c.setFont("Helvetica-Bold", 18)
                        c.drawCentredString(300, 750, report_title)
                        c.setFont("Helvetica", 12)
                        c.drawString(50, 720, f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
                        c.drawString(50, 700, f"Total records analyzed: {filtered_df.shape[0]}")
                        
                        # Add filters used
                        c.drawString(50, 670, "Filters Applied:")
                        c.drawString(70, 650, f"Gender: {sex_choice}")
                        c.drawString(70, 630, f"Chest Pain Type: {cp_choice}")
                        
                        # Add statistics if selected
                        if include_stats:
                            c.showPage()
                            c.setFont("Helvetica-Bold", 16)
                            c.drawString(50, 780, "Statistical Summary")
                            c.setFont("Helvetica", 12)
                            
                            # Age statistics
                            age_stats = filtered_df['age'].describe()
                            c.drawString(50, 750, "Age Statistics:")
                            y_pos = 730
                            for stat, value in age_stats.items():
                                c.drawString(70, y_pos, f"{stat}: {value:.2f}")
                                y_pos -= 20
                            
                            # Gender distribution
                            c.drawString(50, y_pos-30, "Gender Distribution:")
                            c.drawString(70, y_pos-50, f"Male: {gender_dist.get(1, 0):.1f}%")
                            c.drawString(70, y_pos-70, f"Female: {gender_dist.get(0, 0):.1f}%")
                        
                        # Add plots if selected
                        if include_plots:
                            c.showPage()
                            c.setFont("Helvetica-Bold", 16)
                            c.drawString(50, 780, "Data Visualizations")
                            
                            # Save and add each plot
                            plot_files = []
                            for i, fig in enumerate([fig1, fig2, fig3, fig4]):
                                plot_filename = f"plot_{i}.png"
                                fig.savefig(plot_filename, bbox_inches='tight', dpi=300)
                                plot_files.append(plot_filename)
                            
                            # Add plots to PDF with proper spacing
                            y_position = 750
                            for i, plot_file in enumerate(plot_files):
                                if y_position < 150:
                                    c.showPage()
                                    y_position = 750
                                c.drawImage(plot_file, 50, y_position-250, width=500, height=250)
                                y_position -= 300
                        
                        c.save()
                        pdf_buffer.seek(0)
                        return pdf_buffer
                    
                    pdf_buffer = generate_pdf()
                    st.success("Report generated successfully!")
                    
                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=pdf_buffer,
                        file_name=f"{report_title.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        help="Click to download the generated report"
                    )

else:
    # Improved upload prompt
    st.markdown("""
    <div style="text-align: center; padding: 50px; border: 2px dashed #cccccc; border-radius: 10px; margin-top: 20px;">
        <h3 style="margin-top: 0;">📤 Upload a CSV file to begin analysis</h3>
        <p>Drag and drop your medical research data file above or click to browse</p>
        <p style="margin-bottom: 0;"><small>Supported formats: CSV (comma-separated values)</small></p>
    </div>
    """, unsafe_allow_html=True)