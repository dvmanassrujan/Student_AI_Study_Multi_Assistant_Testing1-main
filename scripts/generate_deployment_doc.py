"""
Generates the comprehensive Word document: Free_Deployment_Guide_Llama3.2.docx
"""

import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_document():
    doc = docx.Document()

    # Set page margins (1 inch)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # Document Header / Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("100% Free Deployment Guide: AI Multi-Study Assistant")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(18)
    run_sub = sub_p.add_run("Complete Step-by-Step Blueprint for Hosting Meta Llama 3.2:latest with Zero API Keys & Zero Infrastructure Cost")
    run_sub.font.size = Pt(13)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # Metadata Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Target Project:", "AI Multi-Study Assistant & Autonomous Video Studio"),
        ("Pretrained Model:", "Meta Llama 3.2:latest (3B parameters, Q4_K_M via Ollama)"),
        ("Budget Constraint:", "$0.00 / Fully Free (Zero API Keys & Zero Subscription Fees)"),
        ("Deployment Targets:", "Local Cloudflare Tunnel, Hugging Face Spaces (16GB RAM), Oracle Cloud Always-Free, Google Colab")
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.0)
        c1.width = Inches(4.5)
        set_cell_background(c0, "F0F4F8")
        set_cell_background(c1, "FAFAFA")
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(label)
        r0.font.bold = True
        p1 = c1.paragraphs[0]
        p1.add_run(val)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # SECTION 1: Sentence Analysis & Correction
    # -------------------------------------------------------------
    h1 = doc.add_heading("1. Analysis & Linguistic Correction of Your Request", level=1)
    h1.style.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    doc.add_paragraph(
        "Below is the grammatical analysis and formal technical revision of your original prompt."
    )

    # Original vs Corrected Box
    callout_table = doc.add_table(rows=2, cols=1)
    callout_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    c_orig = callout_table.rows[0].cells[0]
    set_cell_background(c_orig, "FFF3CD")
    p_orig = c_orig.paragraphs[0]
    r_o_lbl = p_orig.add_run("Original User Sentence:\n")
    r_o_lbl.font.bold = True
    p_orig.add_run('"analyse above project and currently i am using pretrained model of llama3.2:latest , and i have no api keys, , i want to deploy whole model free , i need list of deployment tools that support fully free access that supports  llama3.2:latest pre trained fully free, i need step by step procedure in one word document analyse above sentence and correct it if any mistake"')

    c_corr = callout_table.rows[1].cells[0]
    set_cell_background(c_corr, "D4EDDA")
    p_corr = c_corr.paragraphs[0]
    r_c_lbl = p_corr.add_run("Professionally Corrected Sentence (Recommended):\n")
    r_c_lbl.font.bold = True
    p_corr.add_run('"Please analyze my project. I am currently using the pretrained Meta Llama 3.2:latest model locally without any paid API keys. I would like to deploy the entire application and model completely free of cost. Please provide a curated list of zero-cost deployment platforms that support Llama 3.2:latest, along with a comprehensive step-by-step deployment guide compiled into a single Word document."')

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "Key Linguistic & Structural Corrections Made:\n"
        "• Capitalization: Replaced lowercase 'i' with 'I' and capitalized proper nouns ('Meta Llama 3.2').\n"
        "• Redundancy: Removed repeated occurrences of 'fully free' and double commas (', ,').\n"
        "• Run-On Sentence: Split the continuous clause into well-formed, professional imperative sentences.\n"
        "• Subject-Verb Agreement: Corrected 'list of deployment tools that support... that supports' to 'zero-cost deployment platforms that support'."
    )

    # -------------------------------------------------------------
    # SECTION 2: Project Architecture & Deployment Reality Check
    # -------------------------------------------------------------
    h2 = doc.add_heading("2. Technical Reality Check: Hosting LLMs on Free Tiers", level=1)
    h2.style.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    doc.add_paragraph(
        "Before selecting a host, it is critical to understand the technical boundary between standard web apps and Large Language Model (LLM) backends:"
    )

    p_facts = doc.add_paragraph()
    p_facts.add_run("1. Model RAM Footprint: ").bold = True
    p_facts.add_run("Meta Llama 3.2 (3B parameters quantized to Q4_K_M) requires approximately 2.0 GB of disk storage and 2.2 GB - 2.8 GB of active system RAM during inference.\n")
    p_facts.add_run("2. The Free Cloud Trap: ").bold = True
    p_facts.add_run("Traditional free hosting services (Render, Railway, Vercel, Netlify, Heroku) restrict free containers to 512 MB of RAM. Attempting to run Ollama or load Llama 3.2 weights on these tiers results in an immediate Out-Of-Memory (OOM) SIGKILL error.\n")
    p_facts.add_run("3. The Solution: ").bold = True
    p_facts.add_run("You must use platforms that provide at least 4 GB - 16 GB of free RAM or utilize secure tunneling from your local workstation.")

    # -------------------------------------------------------------
    # SECTION 3: The 4 Best 100% Free Deployment Platforms
    # -------------------------------------------------------------
    h3 = doc.add_heading("3. Curated List of 100% Free Deployment Platforms", level=1)
    h3.style.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    # Platform Table
    plat_table = doc.add_table(rows=5, cols=5)
    plat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Platform", "Free Hardware Specs", "LLM Compatibility", "Cost & Card Policy", "Best Use Case"]
    hdr_row = plat_table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr_row.cells[i]
        set_cell_background(cell, "003366")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    plat_rows = [
        ("Cloudflare Tunnel (Local Self-Host)", "Uses your PC CPU + 8GB RAM", "Native (Already running Ollama llama3.2)", "100% Free Forever\n(No credit card)", "Production, Demos, 24/7 personal access"),
        ("Hugging Face Spaces (Gradio SDK)", "2 vCPU, 16 GB RAM, 50 GB Disk", "Native Gradio SDK + User-space Ollama", "100% Free\n(No credit card)", "Public Web Demos, Portfolios, Student Showcases"),
        ("Oracle Cloud Always-Free", "4 OCPUs ARM, 24 GB RAM, 200 GB Disk", "Autonomous Ollama server 24/7", "100% Free Forever\n(Credit card for verification)", "Full 24/7 autonomous production cloud server"),
        ("Google Colab / Kaggle", "Free T4 GPU (16 GB VRAM) + 12 GB RAM", "Fast GPU inference for Llama 3.2", "100% Free\n(No credit card)", "High-speed testing, presentations, GPU benchmarks")
    ]

    for idx, row_data in enumerate(plat_rows, start=1):
        row = plat_table.rows[idx]
        for col_idx, text in enumerate(row_data):
            cell = row.cells[col_idx]
            set_cell_background(cell, "F9FBFD" if idx % 2 == 1 else "FFFFFF")
            p = cell.paragraphs[0]
            p.add_run(text)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # SECTION 4: Step-by-Step Deployment Procedures
    # -------------------------------------------------------------
    h4 = doc.add_heading("4. Step-by-Step Deployment Procedures", level=1)
    h4.style.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    # --- Method 1 ---
    doc.add_heading("Strategy 1: Local Machine + Cloudflare Tunnel (Zero Cost & Easiest)", level=2)
    doc.add_paragraph(
        "This is the recommended path because your computer already has Ollama and llama3.2:latest installed and operating smoothly. A Cloudflare Tunnel provides a secure, public HTTPS URL without needing a public IP, dynamic DNS, or router port-forwarding."
    )
    doc.add_paragraph(
        "Step 1: Download Cloudflare Tunnel Executable\n"
        "• Download 'cloudflared-windows-amd64.exe' from Cloudflare's official GitHub releases.\n"
        "• Rename the file to 'cloudflared.exe' and place it in your project folder or Windows PATH.\n\n"
        "Step 2: Ensure Local Services Are Running\n"
        "• Terminal 1: Run 'ollama serve'\n"
        "• Terminal 2: Run 'python frontend/app.py' (Gradio launches on http://localhost:7860)\n\n"
        "Step 3: Expose Application with One Command\n"
        "• Open a new PowerShell terminal and run:\n"
        "    cloudflared tunnel --url http://localhost:7860\n\n"
        "Step 4: Access Worldwide via HTTPS\n"
        "• Cloudflare will output a public URL (e.g., https://random-name.trycloudflare.com).\n"
        "• Anyone on mobile, tablet, or external networks can now use your AI Multi-Study Assistant with live Meta Llama 3.2 inference!"
    )

    # --- Method 2 ---
    doc.add_heading("Strategy 2: Hugging Face Spaces using Native Gradio SDK (No Docker Required)", level=2)
    doc.add_paragraph(
        "Hugging Face Spaces provides a native 'Gradio SDK' environment with 16 GB of free RAM and 50 GB disk. By selecting the Gradio SDK instead of Docker, Hugging Face manages Python dependencies and web serving automatically without requiring any container build scripts."
    )
    doc.add_paragraph(
        "Step 1: Create a Hugging Face Space with Gradio SDK\n"
        "• Navigate to https://huggingface.co/spaces and click 'Create new Space'.\n"
        "• Space Name: 'student-ai-assistant'\n"
        "• Space SDK: Select 'Gradio' (DO NOT select Docker).\n"
        "• Space Hardware: Select 'CPU basic - 2 vCPU · 16 GB RAM · Free'.\n\n"
        "Step 2: Add System Packages via 'packages.txt'\n"
        "Hugging Face Gradio Spaces install Linux dependencies from 'packages.txt'. Ensure 'packages.txt' in the project root contains:\n"
        "    ffmpeg\n"
        "    curl\n\n"
        "Step 3: Root Entrypoint ('app.py') with Auto-Bootstrapped Ollama\n"
        "Hugging Face Gradio SDK looks for 'app.py' in the root folder. The project includes an auto-bootstrapping root 'app.py' that automatically:\n"
        "1. Detects the Linux Hugging Face Space environment.\n"
        "2. Downloads the standalone user-space Ollama binary to /tmp/ollama_bin (requiring zero sudo/root privileges).\n"
        "3. Starts 'ollama serve' in the background.\n"
        "4. Automatically pulls 'llama3.2:latest' into the 16 GB RAM space.\n"
        "5. Launches your complete Multi-Assistant Gradio UI.\n\n"
        "Step 4: Push to Hugging Face Spaces\n"
        "Run the following git commands in your terminal:\n"
        "    git remote add space https://huggingface.co/spaces/YOUR_USERNAME/student-ai-assistant\n"
        "    git add .\n"
        "    git commit -m 'Deploy to Hugging Face Space with Gradio SDK'\n"
        "    git push space main\n\n"
        "Step 5: Live Public Access\n"
        "Hugging Face will automatically install requirements.txt, launch app.py, and give you a permanent, free public URL (https://YOUR_USERNAME-student-ai-assistant.hf.space)."
    )

    # --- Method 3 ---
    doc.add_heading("Strategy 3: Oracle Cloud Always-Free Compute (24 GB RAM, 24/7 Uptime)", level=2)
    doc.add_paragraph(
        "Oracle Cloud Infrastructure (OCI) offers an unmatched Always-Free tier that gives you a dedicated server running 24 hours a day, 7 days a week, forever without cost."
    )
    doc.add_paragraph(
        "Step 1: Create Always-Free Instance\n"
        "• Sign up at https://www.oracle.com/cloud/free/.\n"
        "• Create a VM Instance: Shape 'VM.Standard.A1.Flex' (Ampere ARM).\n"
        "• Configure with 4 OCPUs and 24 GB RAM (100% free under Always-Free limits).\n"
        "• Select OS: Ubuntu 22.04 LTS.\n\n"
        "Step 2: Install Ollama and Project Dependencies\n"
        "• SSH into your server: ssh ubuntu@YOUR_SERVER_IP\n"
        "• Install Ollama: curl -fsSL https://ollama.com/install.sh | sh\n"
        "• Download Model: ollama pull llama3.2:latest\n"
        "• Clone Project and install requirements: pip install -r requirements.txt\n\n"
        "Step 3: Run as a Background Service\n"
        "• Use systemd or screen/tmux to run: python frontend/app.py\n"
        "• Open ingress port 7860 in Oracle Cloud Virtual Cloud Network (VCN) security list.\n"
        "• Your application is now accessible 24/7 on your server's public IP or custom domain."
    )

    # --- Method 4 ---
    doc.add_heading("Strategy 4: Google Colab / Kaggle (Free 16GB GPU for Demonstrations)", level=2)
    doc.add_paragraph(
        "When presenting live projects or needing fast GPU inference for video transcription and editing alongside Llama 3.2:"
    )
    doc.add_paragraph(
        "Step 1: Open Google Colab and set Runtime -> Change runtime type -> T4 GPU.\n"
        "Step 2: In a code cell, execute:\n"
        "    !curl -fsSL https://ollama.com/install.sh | sh\n"
        "    import subprocess, time\n"
        "    subprocess.Popen(['ollama', 'serve'])\n"
        "    time.sleep(4)\n"
        "    !ollama pull llama3.2:latest\n\n"
        "Step 3: Run the Gradio App with Built-in Share Tunnel:\n"
        "    # In frontend/app.py change demo.launch() to:\n"
        "    demo.launch(share=True)\n"
        "    !python frontend/app.py\n\n"
        "Step 4: Gradio automatically generates a public https://xxxx.gradio.live link valid for 72 hours with full GPU acceleration."
    )

    # -------------------------------------------------------------
    # SECTION 5: Configuration & Security Best Practices
    # -------------------------------------------------------------
    h5 = doc.add_heading("5. Production Configuration & Security Checklist", level=1)
    h5.style.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    doc.add_paragraph(
        "1. Environment File (.env):\n"
        "   Ensure your .env defines:\n"
        "   MODEL_NAME=llama3.2:latest\n"
        "   OLLAMA_MODEL=llama3.2:latest\n"
        "   OLLAMA_BASE_URL=http://localhost:11434\n"
        "   MAX_CONCURRENT_JOBS=1\n\n"
        "2. Concurrency Control:\n"
        "   Because Meta Llama 3.2 uses CPU or single-GPU inference, keep MAX_CONCURRENT_JOBS=1 to prevent multiple users from causing server thread thrashing.\n\n"
        "3. Automated Diagnostics Verification:\n"
        "   Always run python scripts/check_ollama.py before deploying to confirm all 4 diagnostic queries (Q&A, math, code, summary) pass 100%."
    )

    # Save document
    output_path = Path(r"C:\Users\dvman\Downloads\Student_AI_Study_Multi_Assistant_Testing1-main\Student_AI_Study_Multi_Assistant_Testing1-main\Free_Deployment_Guide_Llama3.2.docx")
    doc.save(str(output_path))
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    create_document()

