from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key-change-me')

# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# --- Data ---
PERSONAL_INFO = {
    "name": "Pradip Pandey", 
    "title": "Digital Engagement Officer & Cybersecurity Specialist",
    "tagline": "Bridging the gap between complex IT infrastructure and community digital literacy.",
    "summary": "I am a versatile IT professional with a unique blend of cybersecurity expertise and hands‑on technical support experience. My background spans network engineering, system administration, hardware/software troubleshooting, and end‑user support — making me an adaptable asset to any IT team.",
    "email": "pradippandey555@gmail.com",
    "github": "pradippandey555",
    "linkedin": "pradip-pandey-317997195"
}

SKILLS_DATA = [
    {
        "category": "Operating Systems",
        "icon": "fa-desktop",
        "color": "border-green-500",
        "items": [
            "Windows Server 2019/2022: AD, Group Policy, DNS, DHCP",
            "Windows 10/11 installation, administration & troubleshooting",
            "Linux (Ubuntu, CentOS): Server config, shell scripting",
            "macOS basic administration & cross‑platform support"
        ]
    },
    {
        "category": "Networking & Security",
        "icon": "fa-network-wired",
        "color": "border-blue-500",
        "items": [
            "Cisco routing & switching: VLANs, OSPF, EIGRP, ACLs",
            "Firewall configuration: Windows Firewall, Cisco ASA basics",
            "VPN setup: Site‑to‑site & remote access",
            "Access control in Microsoft environments",
            "Network monitoring (SIEM, NetFlow)",
            "Endpoint protection & security hardening"
        ]
    },
    {
        "category": "Virtualization & Cloud",
        "icon": "fa-cloud",
        "color": "border-purple-500",
        "items": [
            "VMware & VirtualBox lab creation",
            "Hyper‑V basics",
            "Azure & AWS fundamentals (VMs, storage, RBAC)",
            "VM deployment, snapshots, optimisation"
        ]
    },
    {
        "category": "Programming & Development",
        "icon": "fa-code",
        "color": "border-orange-500",
        "items": [
            "Python automation, log parsing, CSV data processing",
            "JavaScript, HTML5, CSS3 for responsive design",
            "Flask web app development & deployment",
            "Secure coding aligned with OWASP Top 10"
        ]
    },
    {
        "category": "IT Support & Troubleshooting",
        "icon": "fa-headset",
        "color": "border-indigo-500",
        "items": [
            "Level 1 & 2 help desk support",
            "Incident logging & resolution tracking",
            "Hardware diagnostics, repairs, maintenance",
            "Peripheral & network device configuration",
            "Software installation & version management"
        ]
    },
    {
        "category": "IT & Cybersecurity Management",
        "icon": "fa-shield-halved",
        "color": "border-red-500",
        "items": [
            "Risk assessment & security policy development",
            "Incident response planning & reporting",
            "System analysis & SDLC documentation",
            "IT asset lifecycle management & compliance"
        ]
    },
    {
        "category": "Soft Skills",
        "icon": "fa-people-group",
        "color": "border-teal-500",
        "items": [
            "Clear communication & customer service",
            "Problem‑solving under time pressure",
            "Adaptability across technologies",
            "Collaborative teamwork & knowledge sharing"
        ]
    }
]

CERTIFICATES = [
    { 
        "id": 1, 
        "title": "Network Analysis Using Wireshark 3", 
        "issuer": "Network Security", 
        "src": "Wireshark 3.jpg",
        "description": "Practical packet capture and traffic analysis skills."
    },
    { 
        "id": 2, 
        "title": "Wireless Penetration Using Kali Linux", 
        "issuer": "Penetration Testing", 
        "src": "Kali Wireless Pen Test.jpg",
        "description": "Hands‑on wireless network auditing and security testing."
    },
    { 
        "id": 3, 
        "title": "Cyber Security Fundamentals", 
        "issuer": "Cyber Security", 
        "src": "Cyber.jpg",
        "description": "Core concepts in security frameworks and risk mitigation."
    },
    { 
        "id": 4, 
        "title": "Metasploit Testing Recipes", 
        "issuer": "Vulnerability Assessment", 
        "src": "Metasploit Testing Recipes.jpg",
        "description": "Exploitation and vulnerability assessment techniques."
    },
    { 
        "id": 5, 
        "title": "Outlook Essentials", 
        "issuer": "Productivity", 
        "src": "Outlook.jpg",
        "description": "Efficient email, calendar, and task management skills."
    },
    { 
        "id": 6, 
        "title": "Network Scanning With NMAP", 
        "issuer": "Network Recon", 
        "src": "Network Scanning With NMAP.jpg",
        "description": "Proficiency in network reconnaissance and mapping."
    },
    { 
        "id": 7, 
        "title": "Comptia Network Certification Exam Essentials", 
        "issuer": "Networking", 
        "src": "Comptia Network Certification Exam Essentials.jpg",
        "description": "Fundamental networking knowledge and exam preparation."
    }
]

EDUCATION = [
    {
        "degree": "Bachelor of Cybersecurity (Current)",
        "institution": "Charles Sturt University",
        "year": "2023 - Present (2nd Year Completed)",
        "details": "Advanced focus on Digital Forensics, Network Security, and System Analysis. Consistent high achiever in Programming Principles and Database Systems.",
        "tags": ["Digital Forensics", "Network Defense", "System Analysis"]
    },
    {
        "degree": "Diploma of Information Technology (Networking)",
        "institution": "TAFE NSW",
        "year": "2022",
        "details": "Specialized in advanced network configuration, server management (Windows/Linux), and cybersecurity management protocols.",
        "tags": ["Cisco Networking", "Server Admin", "Virtualization"]
    },
    {
        "degree": "Certificate IV in Information Technology",
        "institution": "TAFE NSW",
        "year": "2021",
        "details": "Foundation in IT support, web development, and database administration.",
        "tags": ["Web Dev", "IT Support", "SQL"]
    },
    {
        "degree": "Certificate III in Information, Digital Media & Technology",
        "institution": "TAFE NSW",
        "year": "2020",
        "details": "Entry-level desktop support and operating system fundamentals.",
        "tags": ["Desktop Support", "OS Config"]
    }
]

PROJECTS = [
    {
        "title": "Linux Server Administration",
        "role": "SysAdmin",
        "category": "Operating Systems",
        "description": "Deployed and managed Ubuntu and CentOS servers for user account management, file sharing, and service hosting. Configured permissions, automated backups, and implemented shell scripting for system monitoring.",
        "tech": ["Ubuntu", "CentOS", "Shell Scripting", "User Mgmt"],
        "icon": "fa-server",
        "color": "border-green-500/50",
        "youtube_id": "dQw4w9WgXcQ", 
        "github_url": "https://github.com/pradippandey555"
    },
    {
        "title": "Virtualization & Infrastructure Labs",
        "role": "Infrastructure Engineer",
        "category": "Cloud & Virtualization",
        "description": "Built virtual lab environments using VirtualBox and VMware to simulate multi‑OS networks for testing and training. Configured virtual switches, NAT, and cloned VM templates for rapid deployment.",
        "tech": ["VMware", "VirtualBox", "Networking", "Virtualization"],
        "icon": "fa-cloud",
        "color": "border-purple-500/50",
        "youtube_id": "", 
        "github_url": "https://github.com/pradippandey555"
    },
    {
        "title": "Windows Server & AD Management",
        "role": "Network Admin",
        "category": "Networking",
        "description": "Installed and configured Windows Server with AD, Group Policy, DNS, DHCP, and access controls. Integrated Defender AV and configured Windows Firewall for network protection.",
        "tech": ["Active Directory", "Group Policy", "DNS/DHCP", "Windows Server"],
        "icon": "fa-network-wired",
        "color": "border-blue-500/50",
        "youtube_id": "",
        "github_url": "https://github.com/pradippandey555"
    },
    {
        "title": "IT Project Management Simulation",
        "role": "Project Manager",
        "category": "Cybersecurity",
        "description": "Led a simulated IT upgrade project using Waterfall & Agile. Managed timelines, stakeholder communications, and documented risk assessments for a server migration plan.",
        "tech": ["Agile", "Waterfall", "Risk Assessment", "Migration"],
        "icon": "fa-tasks",
        "color": "border-red-500/50",
        "youtube_id": "",
        "github_url": "https://github.com/pradippandey555"
    },
    {
        "title": "Python Automation & Scripting",
        "role": "Developer",
        "category": "Development",
        "description": "Developed Python scripts to automate log analysis, parse CSV network reports, and send alerts for anomalies. Built CLI utilities for system checks and file management automation.",
        "tech": ["Python", "Automation", "Log Analysis", "Scripting"],
        "icon": "fa-code",
        "color": "border-orange-500/50",
        "youtube_id": "", 
        "github_url": "https://github.com/pradippandey555"
    },
    {
        "title": "Full Stack Web Development",
        "role": "Web Developer",
        "category": "Development",
        "description": "Created responsive websites using HTML, CSS, JS, and Flask. Integrated authentication, CRUD operations, and basic security against SQL injection and XSS.",
        "tech": ["HTML/CSS/JS", "Flask", "Web Security", "CRUD"],
        "icon": "fa-laptop-code",
        "color": "border-orange-500/50",
        "youtube_id": "", 
        "github_url": "https://github.com/pradippandey555"
    },
    {
        "title": "System Analysis & Design",
        "role": "Analyst",
        "category": "Cybersecurity",
        "description": "Produced SDLC documentation, including requirements gathering, UML diagrams, DB design, and functional testing procedures.",
        "tech": ["SDLC", "UML", "DB Design", "Documentation"],
        "icon": "fa-file-contract",
        "color": "border-red-500/50",
        "youtube_id": "", 
        "github_url": "https://github.com/pradippandey555"
    },
    {
        "title": "Advanced Routing & Switching",
        "role": "Network Engineer",
        "category": "Networking",
        "description": "Configured Cisco routers/switches for VLANs, OSPF, EIGRP, and implemented ACLs and port security to restrict unauthorized access.",
        "tech": ["Cisco", "VLANs", "OSPF/EIGRP", "Port Security"],
        "icon": "fa-network-wired",
        "color": "border-blue-500/50",
        "youtube_id": "", 
        "github_url": "https://github.com/pradippandey555"
    },
    {
        "title": "MS Access Control Management",
        "role": "Security Admin",
        "category": "Networking",
        "description": "Applied NTFS permissions, user rights assignments, and multi-level access policies in Windows environments to uphold least privilege.",
        "tech": ["NTFS", "Access Control", "Windows Security", "Least Privilege"],
        "icon": "fa-key",
        "color": "border-blue-500/50",
        "youtube_id": "", 
        "github_url": "https://github.com/pradippandey555"
    },
    {
        "title": "Cybersecurity Management Simulation",
        "role": "Security Manager",
        "category": "Cybersecurity",
        "description": "Developed security policies and incident response plans for a simulated organisation. Conducted risk assessments and ISO 27001 compliance checks.",
        "tech": ["Policy Dev", "Incident Response", "ISO 27001", "Compliance"],
        "icon": "fa-shield-virus",
        "color": "border-red-500/50",
        "youtube_id": "", 
        "github_url": "https://github.com/pradippandey555"
    },
    {
        "title": "IT Help Desk Support Lab",
        "role": "Support Specialist",
        "category": "IT Support",
        "description": "Provided L1 & L2 support in a simulated service desk, resolving hardware/software issues, imaging devices, and handling installations.",
        "tech": ["Help Desk", "Troubleshooting", "Imaging", "L1/L2 Support"],
        "icon": "fa-headset",
        "color": "border-indigo-500/50",
        "youtube_id": "", 
        "github_url": "https://github.com/pradippandey555"
    },
    {
        "title": "Firewall & Endpoint Security",
        "role": "Security Analyst",
        "category": "Cybersecurity",
        "description": "Configured advanced Windows Firewall rules, tested application whitelisting, and deployed Microsoft Defender for Endpoint features.",
        "tech": ["Firewalls", "Whitelisting", "Defender", "Endpoint Security"],
        "icon": "fa-lock",
        "color": "border-red-500/50",
        "youtube_id": "", 
        "github_url": "https://github.com/pradippandey555"

    }
]

# Route Definitions
@app.route('/')
def home():
    return render_template('home.html', 
                           personal_info=PERSONAL_INFO,
                           skills=SKILLS_DATA,
                           projects=PROJECTS,
                           certificates=CERTIFICATES,
                           education=EDUCATION)

@app.route('/annapurna')
def annapurna():
    return render_template('annapurna.html')

@app.route('/projects')
def projects():
    # You can extend PROJECTS with video links and github urls here or in the data above
    return render_template('projects.html', projects=PROJECTS) # Passing same projects for now, will enhance

@app.route('/submit-help-request', methods=['POST'])
def submit_help_request():
    if request.method == 'POST':
        name = request.form.get('name')
        arrival_date = request.form.get('arrival_date')
        contact_info = request.form.get('contact_info')
        message = request.form.get('message')
        
        # Email Logic
        try:
            msg = Message(f"New Help Request from {name}",
                          recipients=['annapurnaaspirations@gmail.com'])
            msg.body = f"""
            Name: {name}
            Arrival Date: {arrival_date}
            Contact Info: {contact_info}
            Message: {message}
            """
            mail.send(msg)
            flash("Your request has been sent successfully!", "success")
        except Exception as e:
            print(f"Error sending email: {e}")
            flash("There was an error sending your request. Please try again later.", "error")
            
        return redirect(url_for('annapurna'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
