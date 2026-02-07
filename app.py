import streamlit as st
import google.generativeai as genai

# --- 1. การตั้งค่าหน้าเว็บ (Page Configuration) ---
st.set_page_config(
    page_title="DevSecOps Config Auditor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ฟังก์ชันสำหรับเชื่อมต่อ Gemini API ---
def analyze_config(api_key, content, context_type):
    """
    ฟังก์ชันส่งข้อมูลไปให้ Gemini วิเคราะห์
    """
    try:
        # ตั้งค่า API Key
        genai.configure(api_key=api_key)
        
        # เลือก Model (ใช้ gemini-1.5-flash เพื่อความรวดเร็ว หรือ pro เพื่อความละเอียด)
        model = genai.GenerativeModel('gemini-2.5-flash')

        # สร้าง Prompt แบบละเอียด (System Prompting)
        prompt = f"""
        Act as a Senior DevSecOps Engineer and Network Specialist. 
        Your task is to audit the following configuration file (Context: {context_type}).
        
        Please provide the output in the following Markdown format:
        
        ## 📊 Analysis Summary
        (Briefly explain what this configuration does)

        ## 🚨 Security Risks & Vulnerabilities
        (List potential security issues, e.g., running as root, weak encryption, exposed ports. Use bullet points with High/Medium/Low severity tags)

        ## ✅ Best Practices Recommendations
        (Suggest improvements for performance, maintainability, and standard DevSecOps practices)

        ## 🛠️ Refactored Configuration
        (Provide the corrected code block with comments explaining changes)

        ---
        **Input Configuration:**
        ```
        {content}
        ```
        """
        
        # ส่งคำสั่งไปที่ AI
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error: {str(e)}"

# --- 3. ส่วนติดต่อผู้ใช้ (UI Layout) ---

# Header
st.title("🛡️ DevSecOps Config Auditor")
st.markdown("""
**Application for Computer Engineering:** เครื่องมือตรวจสอบความปลอดภัยและมาตรฐานของ Configuration Files 
ด้วย AI (Powered by Google Gemini)
""")

# Sidebar: ตั้งค่า API Key
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("กรุณาใส่ Google Gemini API Key เพื่อเริ่มต้นใช้งาน")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.markdown("[👉 รับ API Key ฟรีที่นี่ (Google AI Studio)](https://aistudio.google.com/app/apikey)")
    st.divider()
    st.markdown("### Supported Formats:")
    st.markdown("- 🐳 **Docker:** Dockerfile, docker-compose.yml")
    st.markdown("- ☸️ **Kubernetes:** K8s Manifests (.yaml)")
    st.markdown("- 🌐 **Network:** Cisco IOS, Juniper, OSPF/BGP Configs")
    st.markdown("- ☁️ **IaC:** Terraform (.tf), Ansible Playbooks")

# Main Content: แบ่งเป็น Tabs
tab1, tab2 = st.tabs(["📝 Paste Configuration", "📂 Upload File"])

config_content = ""
context_type = "General Configuration"

# Tab 1: วางโค้ดโดยตรง
with tab1:
    st.subheader("Paste your config here")
    text_input = st.text_area("Input Code:", height=300, placeholder="FROM ubuntu:latest\nRUN apt-get update...")
    if text_input:
        config_content = text_input
        context_type = "Pasted Text"

# Tab 2: อัปโหลดไฟล์
with tab2:
    st.subheader("Upload configuration file")
    uploaded_file = st.file_uploader("Choose a file", type=['txt', 'yaml', 'yml', 'dockerfile', 'tf', 'conf', 'json'])
    
    if uploaded_file is not None:
        # อ่านไฟล์และแปลงเป็น String
        try:
            stringio = uploaded_file.getvalue().decode("utf-8")
            config_content = stringio
            context_type = f"Uploaded File ({uploaded_file.name})"
            st.success(f"File '{uploaded_file.name}' loaded successfully!")
            with st.expander("Preview File Content"):
                st.code(config_content)
        except Exception as e:
            st.error("Error reading file. Please make sure it is a text-based file.")

# --- 4. ปุ่ม Action และการแสดงผล ---
st.divider()

if st.button("🚀 Analyze Configuration", type="primary"):
    if not api_key:
        st.warning("⚠️ กรุณาใส่ API Key ในแถบด้านซ้ายก่อน (Please enter API Key in the sidebar)")
    elif not config_content:
        st.warning("⚠️ กรุณาใส่ข้อมูล Configuration หรืออัปโหลดไฟล์ (Please provide input)")
    else:
        with st.spinner('🤖 AI กำลังวิเคราะห์ช่องโหว่และความปลอดภัย (Analyzing Security & Compliance)...'):
            # เรียกฟังก์ชัน AI
            result = analyze_config(api_key, config_content, context_type)
            
            # แสดงผลลัพธ์
            st.success("✅ Analysis Complete!")
            st.markdown("---")
            st.markdown(result)