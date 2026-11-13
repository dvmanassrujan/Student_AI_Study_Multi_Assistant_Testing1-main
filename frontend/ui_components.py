"""
NEURAL NEXUS – PROFESSIONAL MEDIUM-DARK BLUE DESIGN SYSTEM
Next-Generation UI/UX Design System & Accessible Component Engine
for GenAI Video Intelligence Studio & Autonomous Multi-Study Platform.
"""

from typing import Dict, Any, List, Optional


# ==============================================================================
# 1. PROFESSIONAL MEDIUM-DARK BLUE DESIGN SYSTEM (CSS)
# ==============================================================================

NEURAL_NEXUS_CSS = """
/* ==========================================================================
   PROFESSIONAL MEDIUM-DARK BLUE DESIGN SYSTEM
   Palette: Rich Medium-Dark Blue Canvas (#0c1526, #0f1c32),
            Surface Card Blue (#15243e, #17284a),
            Elevated Active Blue (#1e355b, #223c67),
            Input & Box Background (#111f35),
            Accent Royal & Sky Blue (#2563eb, #38bdf8),
            High-Contrast Text (#FFFFFF, #F8FAFC, #E2E8F0, #CBD5E1),
            Crisp Defined Borders (#274170, #2b4980)
   ========================================================================== */

:root, .dark, body, .gradio-container {
  /* Core Theme Colors - Professional Medium-Dark Blue */
  --nn-bg-midnight: #0c1526;
  --nn-bg-navy: #0f1c32;
  --nn-bg-indigo: #13223f;
  --nn-bg-card: #17284a;
  --nn-bg-card-hover: #1e355b;
  --nn-bg-glass: rgba(23, 40, 74, 0.92);
  --nn-bg-input: #111f35;
  
  --nn-cyan: #38bdf8;
  --nn-cyan-glow: rgba(56, 189, 248, 0.30);
  --nn-violet: #60a5fa;
  --nn-violet-glow: rgba(96, 165, 250, 0.30);
  --nn-blue: #2563eb;
  --nn-blue-light: #93c5fd;
  --nn-magenta: #38bdf8;
  --nn-emerald: #10b981;
  --nn-amber: #f59e0b;
  --nn-rose: #ef4444;
  
  /* Text Colors - High Visibility & Maximum Contrast */
  --nn-text-primary: #FFFFFF;
  --nn-text-secondary: #E2E8F0;
  --nn-text-muted: #CBD5E1;
  
  /* Crisp Visible Borders */
  --nn-border: #274170;
  --nn-border-glow: #38bdf8;
  --nn-border-violet: #60a5fa;
  
  /* Gradients */
  --nn-gradient-hero: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #0284c7 100%);
  --nn-gradient-accent: linear-gradient(135deg, #2563eb 0%, #38bdf8 100%);
  --nn-gradient-magenta: linear-gradient(135deg, #1d4ed8 0%, #38bdf8 100%);
  --nn-gradient-emerald: linear-gradient(135deg, #10b981 0%, #38bdf8 100%);
  --nn-gradient-surface: linear-gradient(180deg, #17284a 0%, #13223f 100%);
  
  --nn-font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --nn-font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace;

  /* Gradio Native System Overrides */
  --body-background-fill: #0c1526 !important;
  --body-text-color: #F8FAFC !important;
  --body-text-color-subdued: #CBD5E1 !important;
  --background-fill-primary: #17284a !important;
  --background-fill-secondary: #13223f !important;
  --border-color-primary: #274170 !important;
  --border-color-accent: #38bdf8 !important;
  --block-background-fill: #17284a !important;
  --block-border-color: #274170 !important;
  --block-border-width: 1px !important;
  --block-label-background-fill: #13223f !important;
  --block-label-text-color: #F1F5F9 !important;
  --block-title-text-color: #FFFFFF !important;
  --input-background-fill: #111f35 !important;
  --input-border-color: #274170 !important;
  --input-border-color-focus: #38bdf8 !important;
  --input-placeholder-color: #94a3b8 !important;
  --input-text-color: #FFFFFF !important;
  --table-border-color: #274170 !important;
  --table-even-background-fill: #142340 !important;
  --table-odd-background-fill: #17284a !important;
  --table-row-focus: #1e355b !important;
  --button-primary-background-fill: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #0284c7 100%) !important;
  --button-primary-text-color: #FFFFFF !important;
  --button-secondary-background-fill: #182b49 !important;
  --button-secondary-text-color: #FFFFFF !important;
  --button-secondary-border-color: #274170 !important;
  --button-cancel-background-fill: linear-gradient(135deg, #991b1b 0%, #dc2626 100%) !important;
  --button-cancel-text-color: #FFFFFF !important;
}

/* Base Viewport & Body */
body, .gradio-container {
  background-color: #0c1526 !important;
  background-image: 
    radial-gradient(circle at 12% 16%, rgba(37, 99, 235, 0.12) 0%, transparent 45%),
    radial-gradient(circle at 88% 20%, rgba(56, 189, 248, 0.10) 0%, transparent 45%),
    linear-gradient(180deg, #0c1526 0%, #0f1c32 100%) !important;
  color: #F8FAFC !important;
  font-family: var(--nn-font-sans) !important;
  min-height: 100vh;
  margin: 0;
  padding: 0;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: #0c1526;
}
::-webkit-scrollbar-thumb {
  background: #274170;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #38bdf8;
}

/* Gradio Default Overrides */
footer { visibility: hidden !important; height: 0 !important; margin: 0 !important; }
.container { max-width: 1440px !important; margin: 0 auto !important; padding: 0 16px !important; }

/* ==========================================================================
   TABS STYLING – MEDIUM-DARK BLUE
   ========================================================================== */
.tabs {
  border-bottom: 2px solid #274170 !important;
  background: #13223f !important;
  border-radius: 14px 14px 0 0 !important;
  padding: 8px 12px 0 12px !important;
  gap: 6px !important;
}

.tab-nav {
  border: none !important;
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 6px !important;
}

.tab-nav button {
  background: transparent !important;
  color: #CBD5E1 !important;
  border: 1px solid transparent !important;
  border-radius: 10px 10px 0 0 !important;
  padding: 10px 18px !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  letter-spacing: 0.3px !important;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.tab-nav button:hover {
  color: #FFFFFF !important;
  background: #182b49 !important;
  border-color: #274170 !important;
}

.tab-nav button.selected {
  color: #FFFFFF !important;
  background: #17284a !important;
  border: 1px solid #274170 !important;
  border-bottom: 3px solid #38bdf8 !important;
  box-shadow: 0 -2px 14px rgba(56, 189, 248, 0.22) !important;
}

/* Nested Sub-Tabs */
.tabs .tabs {
  background: #0f1c32 !important;
  border-radius: 10px !important;
  margin-top: 10px !important;
  padding: 6px 8px 0 8px !important;
  border-bottom: 1px solid #274170 !important;
}

.tabs .tabs .tab-nav button {
  padding: 7px 15px !important;
  font-size: 13px !important;
}

.tabs .tabs .tab-nav button.selected {
  background: #17284a !important;
  border-bottom: 3px solid #60a5fa !important;
  color: #FFFFFF !important;
}

/* ==========================================================================
   CARDS, PANELS & BLOCKS
   ========================================================================== */
.gr-box, .gr-panel, div[class*="block"], .block {
  background-color: #17284a !important;
  border: 1px solid #274170 !important;
  border-radius: 14px !important;
  color: #F8FAFC !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

div[class*="block"]:hover {
  border-color: #3b82f6 !important;
}

/* Accordions */
.gr-accordion {
  background: #17284a !important;
  border: 1px solid #274170 !important;
  border-radius: 12px !important;
  margin-bottom: 12px !important;
}

.gr-accordion > .label-wrap {
  background: #13223f !important;
  padding: 10px 16px !important;
  color: #FFFFFF !important;
  font-weight: 600 !important;
}

/* ==========================================================================
   INPUTS, TEXTAREAS & DROPDOWNS – CRISP CONTRAST
   ========================================================================== */
input[type="text"], input[type="number"], textarea, select, .gr-input, .gr-textbox input, .gr-textbox textarea {
  background-color: #111f35 !important;
  color: #FFFFFF !important;
  border: 1px solid #274170 !important;
  border-radius: 10px !important;
  font-size: 14px !important;
  transition: all 0.2s ease !important;
}

input::placeholder, textarea::placeholder {
  color: #94a3b8 !important;
  opacity: 1 !important;
}

input:focus, textarea:focus, select:focus {
  border-color: #38bdf8 !important;
  box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25) !important;
  outline: none !important;
}

/* Labels */
label span, .gr-form > label, .block-title, label, .label-wrap {
  color: #F1F5F9 !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  letter-spacing: 0.3px !important;
  text-transform: uppercase !important;
  margin-bottom: 6px !important;
}

/* Dropdown Elements */
.dropdown, select, .gr-dropdown {
  background-color: #111f35 !important;
  color: #FFFFFF !important;
}
.dropdown-menu, ul[role="listbox"], .options {
  background-color: #17284a !important;
  border: 1px solid #274170 !important;
  color: #FFFFFF !important;
}
li[role="option"], .item {
  color: #E2E8F0 !important;
}
li[role="option"]:hover, .item:hover {
  background-color: #1e355b !important;
  color: #38bdf8 !important;
}
li[role="option"].selected, .item.selected {
  background-color: #2563eb !important;
  color: #FFFFFF !important;
}

/* Checkboxes and Radios */
label.checkbox-label, .gr-checkbox label, .gr-radio label {
  color: #E2E8F0 !important;
  font-weight: 500 !important;
}
input[type="checkbox"], input[type="radio"] {
  accent-color: #2563eb !important;
  background-color: #111f35 !important;
  border: 1px solid #274170 !important;
}

/* ==========================================================================
   BUTTONS (PRIMARY, SECONDARY, STOP)
   ========================================================================== */
button.primary, button.gr-button-primary {
  background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #0284c7 100%) !important;
  color: #FFFFFF !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  letter-spacing: 0.4px !important;
  border: 1px solid #60a5fa !important;
  border-radius: 10px !important;
  padding: 11px 22px !important;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
  cursor: pointer !important;
}

button.primary:hover, button.gr-button-primary:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6) !important;
  filter: brightness(1.1) !important;
}

button.primary:active, button.gr-button-primary:active {
  transform: translateY(0) !important;
}

button.secondary, button.gr-button-secondary {
  background: #182b49 !important;
  color: #FFFFFF !important;
  border: 1px solid #274170 !important;
  font-weight: 600 !important;
  font-size: 13.5px !important;
  border-radius: 10px !important;
  padding: 10px 20px !important;
  transition: all 0.2s ease !important;
}

button.secondary:hover, button.gr-button-secondary:hover {
  background: #1e355b !important;
  border-color: #38bdf8 !important;
  color: #38bdf8 !important;
}

button.stop, button[variant="stop"] {
  background: linear-gradient(135deg, #991b1b 0%, #dc2626 100%) !important;
  border: 1px solid #ef4444 !important;
  color: #FFFFFF !important;
  font-weight: 700 !important;
  border-radius: 10px !important;
  transition: all 0.2s ease !important;
}

button.stop:hover, button[variant="stop"]:hover {
  background: #ef4444 !important;
  color: #FFFFFF !important;
  box-shadow: 0 0 16px rgba(239, 68, 68, 0.5) !important;
}

/* ==========================================================================
   CHATBOT STYLING – HIGH READABILITY
   ========================================================================== */
.chatbot, [data-testid="chatbot"] {
  background: #111f35 !important;
  border: 1px solid #274170 !important;
  border-radius: 14px !important;
}

.chatbot .message.user, [data-testid="user"] {
  background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%) !important;
  border: 1px solid #3b82f6 !important;
  border-radius: 14px 14px 2px 14px !important;
  color: #FFFFFF !important;
  box-shadow: 0 4px 12px rgba(12, 21, 38, 0.4) !important;
}

.chatbot .message.user *, [data-testid="user"] * {
  color: #FFFFFF !important;
}

.chatbot .message.bot, [data-testid="bot"] {
  background: #17284a !important;
  border: 1px solid #274170 !important;
  border-radius: 14px 14px 14px 2px !important;
  color: #F8FAFC !important;
  box-shadow: 0 4px 12px rgba(12, 21, 38, 0.4) !important;
}

.chatbot .message.bot *, [data-testid="bot"] * {
  color: #F1F5F9 !important;
}

.chatbot .message.bot h1, .chatbot .message.bot h2, .chatbot .message.bot h3, 
[data-testid="bot"] h1, [data-testid="bot"] h2, [data-testid="bot"] h3 {
  color: #FFFFFF !important;
}

.chatbot .message.bot strong, [data-testid="bot"] strong {
  color: #FFFFFF !important;
}

.chatbot .message.bot code, [data-testid="bot"] code {
  background: #111f35 !important;
  color: #38bdf8 !important;
  border: 1px solid #274170 !important;
  padding: 2px 6px !important;
  border-radius: 4px !important;
}

/* ==========================================================================
   MARKDOWN, TABLES & DATAFRAMES
   ========================================================================== */
.gr-markdown, .markdown, .prose {
  color: #F1F5F9 !important;
}

.gr-markdown h1, .gr-markdown h2, .gr-markdown h3, .gr-markdown h4, .gr-markdown h5, .gr-markdown h6,
.markdown h1, .markdown h2, .markdown h3, .markdown h4, .markdown h5, .markdown h6 {
  color: #FFFFFF !important;
  font-weight: 700 !important;
}

.gr-markdown p, .gr-markdown li, .markdown p, .markdown li {
  color: #E2E8F0 !important;
  line-height: 1.6 !important;
}

.gr-markdown strong, .markdown strong {
  color: #FFFFFF !important;
}

.gr-markdown a, .markdown a {
  color: #38bdf8 !important;
  text-decoration: underline !important;
}

.gr-markdown code, .markdown code {
  background: #111f35 !important;
  color: #38bdf8 !important;
  border: 1px solid #274170 !important;
  padding: 2px 6px !important;
  border-radius: 6px !important;
}

.dataframe, table, .gr-dataframe {
  background-color: #142340 !important;
  color: #F1F5F9 !important;
  border: 1px solid #274170 !important;
}

thead, tr:first-child th, th {
  background-color: #1e355b !important;
  color: #FFFFFF !important;
  font-weight: 700 !important;
  border-bottom: 2px solid #274170 !important;
}

tbody tr {
  background-color: #142340 !important;
  color: #F1F5F9 !important;
  border-bottom: 1px solid #274170 !important;
}

tbody tr:nth-child(even) {
  background-color: #17284a !important;
}

tbody tr:hover {
  background-color: #1e355b !important;
}

td {
  color: #F1F5F9 !important;
  border: 1px solid #274170 !important;
}

/* ==========================================================================
   GLOBAL OVERRIDES FOR STATUS CARDS & EMBEDDED CONTAINERS
   ========================================================================== */
div[style*="background: #0f172a"], div[style*="background:#0f172a"] {
  background-color: #17284a !important;
  border-color: #274170 !important;
  color: #F1F5F9 !important;
}

div[style*="background: #1e293b"], div[style*="background:#1e293b"] {
  background-color: #13223f !important;
  border-color: #274170 !important;
  color: #F1F5F9 !important;
}

div[style*="color: #64748b"], span[style*="color: #64748b"] {
  color: #CBD5E1 !important;
}

div[style*="color: #94a3b8"], span[style*="color: #94a3b8"], p[style*="color: #94a3b8"] {
  color: #E2E8F0 !important;
}

div[style*="color: #A7B1C8"], span[style*="color: #A7B1C8"], p[style*="color: #A7B1C8"] {
  color: #E2E8F0 !important;
}

/* ==========================================================================
   KEYFRAME ANIMATIONS
   ========================================================================== */
@keyframes nnPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(0.92); }
}

.nn-pulse-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #38bdf8;
  box-shadow: 0 0 10px #38bdf8;
  animation: nnPulse 2s infinite ease-in-out;
  margin-right: 6px;
}

.nn-pulse-emerald {
  background-color: #10b981 !important;
  box-shadow: 0 0 10px #10b981 !important;
}
"""


# ==============================================================================
# 2. TOP NAVIGATION & HERO SECTION (MEDIUM-DARK BLUE)
# ==============================================================================

def render_cinematic_hero(model_name: str = "deepseek-coder:1.3b", is_online: bool = True) -> str:
    """Renders the professional Medium-Dark Blue Top Bar and Hero Section."""
    status_color = "#10B981" if is_online else "#F59E0B"
    status_label = "INTELLIGENCE ENGINE ACTIVE" if is_online else "LOCAL FALLBACK MODE"
    
    return f"""
    <div style="font-family: system-ui, -apple-system, sans-serif; margin-bottom: 24px;">
      <!-- TOP NAVIGATION BAR -->
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px; padding: 14px 22px; background: #13223f; border: 1px solid #274170; border-radius: 16px; box-shadow: 0 8px 24px rgba(12, 21, 38, 0.45); margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 14px;">
          <div style="width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #38bdf8 100%); display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 14px rgba(37, 99, 235, 0.45);">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
              <polyline points="2 17 12 22 22 17"></polyline>
              <polyline points="2 12 12 17 22 12"></polyline>
            </svg>
          </div>
          <div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-size: 18px; font-weight: 800; letter-spacing: 0.6px; color: #FFFFFF;">STUDENT AI ASSISTANT</span>
              <span style="font-size: 11px; font-weight: 700; padding: 2px 8px; background: rgba(56, 189, 248, 0.18); border: 1px solid #38bdf8; border-radius: 6px; color: #38bdf8; letter-spacing: 0.5px;">STUDY SUITE v2.5</span>
            </div>
            <div style="font-size: 12px; color: #CBD5E1; font-weight: 500;">Multi-Study Assistant, Coding Lab & Video Studio Platform</div>
          </div>
        </div>

        <!-- ENGINE TELEMETRY PILL -->
        <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
          <div style="display: inline-flex; align-items: center; gap: 8px; padding: 7px 14px; background: #111f35; border: 1px solid #274170; border-radius: 30px;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: {status_color}; box-shadow: 0 0 10px {status_color}; animation: nnPulse 2s infinite;"></span>
            <span style="font-size: 12px; font-weight: 700; color: #FFFFFF; letter-spacing: 0.3px;">{status_label}</span>
            <span style="font-size: 11px; padding: 2px 8px; background: #17284a; border: 1px solid #274170; border-radius: 12px; color: #93c5fd; font-family: monospace;">{model_name}</span>
          </div>
          <div style="display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px; background: #111f35; border: 1px solid #274170; border-radius: 30px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 14 14"></polyline></svg>
            <span style="font-size: 12px; color: #CBD5E1; font-weight: 600;">Port 7860</span>
            <span style="font-size: 10px; color: #34d399; font-weight: 700;">● AUTO-RECOVER</span>
          </div>
        </div>
      </div>

      <!-- CINEMATIC HERO SECTION -->
      <div style="position: relative; overflow: hidden; padding: 44px 36px 40px 36px; background: linear-gradient(135deg, #13223f 0%, #17284a 50%, #1e355b 100%); border: 1px solid #2b4980; border-radius: 20px; box-shadow: 0 16px 48px -12px rgba(12, 21, 38, 0.7);">
        <!-- Ambient Circuit Grid Lines (SVG Overlay) -->
        <svg style="position: absolute; right: 0; top: 0; width: 450px; height: 100%; opacity: 0.15; pointer-events: none;" viewBox="0 0 400 300" fill="none">
          <circle cx="200" cy="150" r="120" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4 6"/>
          <circle cx="200" cy="150" r="60" stroke="#60a5fa" stroke-width="1.5"/>
          <line x1="200" y1="30" x2="200" y2="270" stroke="#2563eb" stroke-width="1" stroke-dasharray="2 4"/>
          <line x1="80" y1="150" x2="320" y2="150" stroke="#2563eb" stroke-width="1" stroke-dasharray="2 4"/>
          <circle cx="200" cy="30" r="4" fill="#38bdf8"/>
          <circle cx="200" cy="270" r="4" fill="#60a5fa"/>
          <circle cx="80" cy="150" r="4" fill="#38bdf8"/>
          <circle cx="320" cy="150" r="4" fill="#60a5fa"/>
        </svg>

        <div style="position: relative; z-index: 2; max-width: 900px;">
          <!-- Pre-badge -->
          <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px; background: rgba(56, 189, 248, 0.15); border: 1px solid #38bdf8; border-radius: 20px; margin-bottom: 16px;">
            <span style="font-size: 13px;">⚡</span>
            <span style="font-size: 12px; font-weight: 700; letter-spacing: 0.6px; color: #38bdf8; text-transform: uppercase;">Next-Gen Multimodal Study Ecosystem</span>
          </div>

          <!-- Main Heading -->
          <h1 style="font-size: 38px; font-weight: 900; line-height: 1.2; margin: 0 0 12px 0; color: #FFFFFF; letter-spacing: -0.3px;">
            INTELLIGENCE THAT CREATES.<br/>AI THAT TRANSFORMS.
          </h1>

          <!-- Supporting Heading -->
          <h2 style="font-size: 18px; font-weight: 700; color: #38bdf8; margin: 0 0 14px 0; letter-spacing: 0.2px;">
            AI Multi-Study Assistant, Coding Lab & Video Production Studio
          </h2>

          <!-- Description -->
          <p style="font-size: 15px; line-height: 1.65; color: #E2E8F0; margin: 0 0 24px 0; max-width: 780px;">
            Experience the next generation of autonomous study tools, multimodal intelligence, coding labs, and educational production. Orchestrating 11 specialized agent nodes with study planning, exam prep, AST code mentoring, and real-time document search.
          </p>

          <!-- Metrics Highlights -->
          <div style="display: flex; align-items: center; gap: 20px; flex-wrap: wrap; margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 10px;">
              <div style="font-size: 26px; font-weight: 800; color: #38bdf8;">16</div>
              <div style="font-size: 12px; color: #CBD5E1; line-height: 1.35;">Autonomous<br/>Studio Stages</div>
            </div>
            <div style="width: 1px; height: 32px; background: #274170;"></div>
            <div style="display: flex; align-items: center; gap: 10px;">
              <div style="font-size: 26px; font-weight: 800; color: #60a5fa;">11</div>
              <div style="font-size: 12px; color: #CBD5E1; line-height: 1.35;">Multi-Agent<br/>Study Nodes</div>
            </div>
            <div style="width: 1px; height: 32px; background: #274170;"></div>
            <div style="display: flex; align-items: center; gap: 10px;">
              <div style="font-size: 26px; font-weight: 800; color: #34d399;">30+</div>
              <div style="font-size: 12px; color: #CBD5E1; line-height: 1.35;">Multilingual<br/>Audio Voices</div>
            </div>
            <div style="width: 1px; height: 32px; background: #274170;"></div>
            <div style="display: flex; align-items: center; gap: 10px;">
              <div style="font-size: 26px; font-weight: 800; color: #38bdf8;">&lt;15ms</div>
              <div style="font-size: 12px; color: #CBD5E1; line-height: 1.35;">Instant Engine<br/>Response</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    """


# ==============================================================================
# 3. SIX AI MODULE CARDS (MEDIUM-DARK BLUE)
# ==============================================================================

def render_six_ai_module_cards() -> str:
    """Renders the 6 interactive module cards in Medium-Dark Blue styling."""
    modules = [
        {
            "id": "MOD 01",
            "title": "Autonomous Video Intelligence Studio",
            "icon": """<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect><line x1="7" y1="2" x2="7" y2="22"></line><line x1="17" y1="2" x2="17" y2="22"></line><line x1="2" y1="12" x2="22" y2="12"></line><line x1="2" y1="7" x2="7" y2="7"></line><line x1="2" y1="17" x2="7" y2="17"></line><line x1="17" y1="17" x2="22" y2="17"></line><line x1="17" y1="7" x2="22" y2="7"></line></svg>""",
            "accent": "#38bdf8",
            "badge": "16-STAGE PIPELINE",
            "desc": "An intelligent 16-stage video production pipeline that automates video editing, silence removal, caption synchronization, vertical shorts generation, and educational content production.",
            "tags": ["Silence Cut", "Shorts <60s", "Ruled Notes", "Cover Studio"]
        },
        {
            "id": "MOD 02",
            "title": "YouTube Intelligence",
            "icon": """<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#60a5fa" stroke-width="2"><path d="M2.5 17a24.12 24.12 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.56 49.56 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.12 24.12 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.55 49.55 0 0 1-16.2 0A2 2 0 0 1 2.5 17"></path><polygon points="10 15 15 12 10 9 10 15"></polygon></svg>""",
            "accent": "#60a5fa",
            "badge": "SENTIMENT & NLP",
            "desc": "Transform YouTube content into actionable intelligence through audience sentiment analysis, comment classification, engagement analytics, retention insights, and intelligent recommendations.",
            "tags": ["Sentiment AI", "Comment Mining", "Retention Curve", "Export CSV"]
        },
        {
            "id": "MOD 03",
            "title": "AI Chat & Multimodal Lab",
            "icon": """<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path><circle cx="9" cy="10" r="1" fill="#38bdf8"></circle><circle cx="12" cy="10" r="1" fill="#38bdf8"></circle><circle cx="15" cy="10" r="1" fill="#38bdf8"></circle></svg>""",
            "accent": "#2563eb",
            "badge": "MULTI-TURN PERSISTENT",
            "desc": "An intelligent multimodal workspace supporting conversational AI, persistent memory, image generation, image-to-video workflows, and coding assistance.",
            "tags": ["SQLite Memory", "Text → Image", "Text → Video", "Instant Stream"]
        },
        {
            "id": "MOD 04",
            "title": "Coding Mentor & DSA Lab",
            "icon": """<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>""",
            "accent": "#10b981",
            "badge": "AST & BIG-O",
            "desc": "An autonomous coding mentor providing programming guidance, AST debugging assistance, algorithm explanations, complexity analysis, and problem-solving support.",
            "tags": ["AST Debug", "Big-O Analysis", "DSA Masterclass", "Caret Error Pointer"]
        },
        {
            "id": "MOD 05",
            "title": "Exam Preparation & Quizzes",
            "icon": """<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path><polyline points="9 9 12 12 16 7"></polyline></svg>""",
            "accent": "#f59e0b",
            "badge": "ASSESSMENT ENGINE",
            "desc": "An AI-powered examination preparation system generating important questions, interactive quizzes, mock tests, and customized flashcards.",
            "tags": ["MCQ Generator", "Answer Keys", "Detailed Logic", "Mock Tests"]
        },
        {
            "id": "MOD 06",
            "title": "Professor Robocat 3D Studio",
            "icon": """<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><circle cx="12" cy="12" r="9"></circle><path d="M9 10h.01"></path><path d="M15 10h.01"></path><path d="M8 15s1.5 2 4 2 4-2 4-2"></path><polyline points="7 4 9 8 5 8"></polyline><polyline points="17 4 15 8 19 8"></polyline></svg>""",
            "accent": "#38bdf8",
            "badge": "3D MULTILINGUAL",
            "desc": "An educational 3D video generation studio creating animated cartoon explainers with synchronized multilingual audio.",
            "tags": ["30+ Languages", "Storyboard AI", "3D Characters", "Neural Voice"]
        }
    ]
    
    cards_html = []
    for m in modules:
        tags_html = "".join([f'<span style="font-size: 11px; padding: 3px 8px; background: #13223f; border: 1px solid #274170; border-radius: 6px; color: #CBD5E1;">{tag}</span>' for tag in m["tags"]])
        card = f"""
        <div style="background: #17284a; border: 1px solid #274170; border-radius: 16px; padding: 22px; box-shadow: 0 8px 24px rgba(12, 21, 38, 0.4); display: flex; flex-direction: column; justify-content: space-between; position: relative; overflow: hidden;">
          <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, transparent, {m["accent"]}, transparent);"></div>
          
          <div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;">
              <div style="width: 48px; height: 48px; border-radius: 12px; background: #111f35; border: 1px solid #274170; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(12, 21, 38, 0.3);">
                {m["icon"]}
              </div>
              <div style="text-align: right;">
                <span style="font-size: 11px; font-weight: 800; color: #94a3b8; font-family: monospace; letter-spacing: 1px;">{m["id"]}</span>
                <div><span style="font-size: 10.5px; font-weight: 700; color: {m["accent"]}; padding: 2px 8px; background: #13223f; border: 1px solid {m["accent"]}55; border-radius: 12px;">{m["badge"]}</span></div>
              </div>
            </div>
            
            <h3 style="font-size: 17px; font-weight: 700; color: #FFFFFF; margin: 0 0 10px 0; letter-spacing: 0.1px;">{m["title"]}</h3>
            <p style="font-size: 13.5px; line-height: 1.6; color: #E2E8F0; margin: 0 0 16px 0;">{m["desc"]}</p>
          </div>
          
          <div>
            <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px;">
              {tags_html}
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding-top: 10px; border-top: 1px solid #274170;">
              <span style="font-size: 11.5px; color: #34d399; font-weight: 700; display: inline-flex; align-items: center; gap: 5px;">
                <span style="width: 6px; height: 6px; border-radius: 50%; background: #34d399;"></span> READY
              </span>
              <span style="font-size: 12px; color: {m["accent"]}; font-weight: 700; letter-spacing: 0.2px;">Launch Tab →</span>
            </div>
          </div>
        </div>
        """
        cards_html.append(card)
        
    return f"""
    <div style="margin-bottom: 30px;">
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; flex-wrap: wrap; gap: 8px;">
        <div>
          <h2 style="font-size: 20px; font-weight: 800; color: #FFFFFF; margin: 0 0 4px 0; letter-spacing: 0.3px;">
            💎 SIX CORE AI INTELLIGENCE MODULES
          </h2>
          <div style="font-size: 13.5px; color: #CBD5E1;">Autonomous study pipelines and interactive multimodal intelligence tools.</div>
        </div>
        <div style="font-size: 12px; color: #38bdf8; font-weight: 700; padding: 4px 12px; background: #13223f; border: 1px solid #38bdf8; border-radius: 20px;">
          ● 6 OF 6 WORKSPACES READY
        </div>
      </div>
      
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 18px;">
        {"".join(cards_html)}
      </div>
    </div>
    """


# ==============================================================================
# 4. MULTI-AGENT NEURAL INTELLIGENCE VISUALIZATION (MEDIUM-DARK BLUE)
# ==============================================================================

def render_multi_agent_neural_visualization() -> str:
    """Renders the interactive multi-agent visualization in Medium-Dark Blue styling."""
    agents = [
        {"name": "Study Concept Tutor", "role": "Step-by-step concept explanations & analogies", "id": "study_agent", "color": "#38bdf8"},
        {"name": "Study Plan Strategist", "role": "Day-by-day & week-by-week timetables & milestones", "id": "study_planner_agent", "color": "#60a5fa"},
        {"name": "Assessment & Exam Coach", "role": "High-yield MCQs, answer keys & mock test generator", "id": "exam_agent", "color": "#f59e0b"},
        {"name": "Senior Coding Mentor", "role": "AST static analysis, debugging & Big-O complexity", "id": "coding_agent", "color": "#10b981"},
        {"name": "Full-Stack Project Architect", "role": "Module architecture & database schema blueprinting", "id": "project_agent", "color": "#38bdf8"},
        {"name": "Document Intelligence", "role": "PDF, DOCX & paper extraction with BM25+TF-IDF search", "id": "document_agent", "color": "#60a5fa"},
        {"name": "Neural Audio Narrator", "role": "Spoken-word instructional audio & script voiceover", "id": "audio_agent", "color": "#38bdf8"},
        {"name": "Cinematic Video Director", "role": "Visual cue generation & storyboard scene creation", "id": "video_agent", "color": "#f43f5e"},
        {"name": "Spaced Repetition Memory", "role": "Flashcard decks, mnemonics & Ebbinghaus intervals", "id": "memory_agent", "color": "#60a5fa"},
        {"name": "Adaptive Learning Coach", "role": "Progress telemetry & personalized weakness targeting", "id": "personalization_agent", "color": "#10b981"},
        {"name": "YouTube Video Intelligence", "role": "Sentiment mining, retention analysis & comment intelligence", "id": "youtube_agent", "color": "#38bdf8"}
    ]
    
    agent_items_html = []
    for a in agents:
        agent_items_html.append(f"""
        <div style="background: #111f35; border: 1px solid #274170; border-left: 3px solid {a["color"]}; border-radius: 10px; padding: 11px 14px; display: flex; flex-direction: column; justify-content: space-between;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
            <span style="font-size: 13.5px; font-weight: 700; color: #FFFFFF;">{a["name"]}</span>
            <span style="font-size: 9.5px; font-weight: 700; color: #34d399; font-family: monospace;">ACTIVE</span>
          </div>
          <div style="font-size: 12px; color: #CBD5E1; line-height: 1.4; margin-bottom: 6px;">{a["role"]}</div>
          <div style="font-size: 10.5px; color: {a["color"]}; font-family: monospace; font-weight: 600;">id: {a["id"]}</div>
        </div>
        """)
        
    return f"""
    <div style="background: #17284a; border: 1px solid #274170; border-radius: 18px; padding: 24px; box-shadow: 0 12px 36px rgba(12, 21, 38, 0.4); margin-bottom: 30px;">
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%); display: flex; align-items: center; justify-content: center;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>
          </div>
          <div>
            <h3 style="font-size: 18px; font-weight: 800; color: #FFFFFF; margin: 0; letter-spacing: 0.2px;">MULTI-AGENT NEURAL INTELLIGENCE CENTER</h3>
            <div style="font-size: 12.5px; color: #CBD5E1;">Autonomous LangGraph StateMachine orchestrating 11 specialized agent nodes in real time.</div>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 11px; padding: 4px 10px; background: rgba(16, 185, 129, 0.18); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 20px; color: #34d399; font-weight: 700;">
            ● 11/11 AGENTS ROUTED
          </span>
          <span style="font-size: 11px; padding: 4px 10px; background: #13223f; border: 1px solid #38bdf8; border-radius: 20px; color: #38bdf8; font-weight: 700;">
            FAST-PATH 0ms LATENCY
          </span>
        </div>
      </div>

      <!-- CENTRAL ORCHESTRATION BANNER -->
      <div style="background: #13223f; border: 1px dashed #38bdf8; border-radius: 12px; padding: 14px 20px; text-align: center; margin-bottom: 20px;">
        <span style="font-size: 11px; font-weight: 800; color: #38bdf8; letter-spacing: 1.2px; text-transform: uppercase;">Central Orchestrator Core</span>
        <div style="font-size: 15px; font-weight: 700; color: #FFFFFF; margin-top: 2px;">LangGraph Router Node (StateGraph Entrypoint)</div>
        <div style="font-size: 12.5px; color: #CBD5E1; margin-top: 4px;">Direct state mapping: task_type ➔ next_agent ➔ specialized execution node ➔ SQLite persistence</div>
      </div>

      <!-- AGENT NODES GRID -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px;">
        {"".join(agent_items_html)}
      </div>
    </div>
    """


# ==============================================================================
# 5. 16-STAGE AUTONOMOUS VIDEO PRODUCTION PIPELINE VISUALIZER (MEDIUM-DARK BLUE)
# ==============================================================================

def render_16_stage_pipeline_visualizer() -> str:
    """Renders the 16-stage pipeline visualizer in Medium-Dark Blue styling."""
    stages = [
        ("01", "Video Ingestion", "Probes media containers, fps, resolution & duration"),
        ("02", "Silence Detection", "Analyzes audio waveform & flags dead-air intervals"),
        ("03", "Awkward Pause Cut", "Splices gaps >0.8s without audio clipping"),
        ("04", "Audio Mastering", "Normalizes loudness & removes vocal hiss"),
        ("05", "Whisper STT Transcribe", "Extracts verbatim timestamps & vocabulary"),
        ("06", "Speaker Diarization", "Identifies instructor vs student vocal roles"),
        ("07", "Dynamic SRT Generation", "Syncs word-level subtitles & highlight styling"),
        ("08", "Multilingual Translation", "Converts script into target language grammar"),
        ("09", "Neural TTS Dubbing", "Synthesizes high-fidelity voiceover in 30+ voices"),
        ("10", "Lip & Audio Alignment", "Time-stretches audio to match frame transitions"),
        ("11", "Vertical Crop 1080x1920", "Smart-centers speaker frame for mobile view"),
        ("12", "Reel / Short Extraction", "Cuts viral educational highlights <60s"),
        ("13", "Viral Hook & Title Gen", "Synthesizes high-CTR headlines with model-free engine"),
        ("14", "Vertical Cover Art", "Renders 1080x1920 branded gradient covers"),
        ("15", "Ruled Notebook Notes", "Compiles handwritten-style revision study sheets"),
        ("16", "Master H.264 Export", "Encodes optimized MP4 for streaming & LMS")
    ]
    
    stage_cards = []
    for num, name, desc in stages:
        stage_cards.append(f"""
        <div style="background: #111f35; border: 1px solid #274170; border-radius: 10px; padding: 12px 14px; position: relative;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
            <span style="font-size: 11px; font-weight: 800; color: #38bdf8; font-family: monospace;">STAGE {num}</span>
            <span style="font-size: 9.5px; font-weight: 700; color: #34d399; padding: 2px 7px; background: rgba(16, 185, 129, 0.18); border-radius: 8px;">READY</span>
          </div>
          <div style="font-size: 13.5px; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">{name}</div>
          <div style="font-size: 11.5px; color: #CBD5E1; line-height: 1.4;">{desc}</div>
        </div>
        """)
        
    return f"""
    <div style="background: #17284a; border: 1px solid #274170; border-radius: 18px; padding: 22px; box-shadow: 0 12px 36px rgba(12, 21, 38, 0.4); margin-bottom: 26px;">
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; margin-bottom: 16px;">
        <div>
          <h3 style="font-size: 18px; font-weight: 800; color: #FFFFFF; margin: 0; letter-spacing: 0.2px;">
            🎬 16-STAGE AUTONOMOUS VIDEO PRODUCTION PIPELINE
          </h3>
          <div style="font-size: 12.5px; color: #CBD5E1;">Fully automated end-to-end studio pipeline executed via MoviePy & FFmpeg.</div>
        </div>
        <div style="font-size: 11.5px; color: #38bdf8; font-weight: 700; padding: 4px 12px; background: #13223f; border: 1px solid #38bdf8; border-radius: 20px;">
          ● SEQUENTIAL STAGE PIPELINE
        </div>
      </div>
      
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 10px;">
        {"".join(stage_cards)}
      </div>
    </div>
    """


# ==============================================================================
# 6. HACKATHON LIVE DEMO PANEL (MEDIUM-DARK BLUE)
# ==============================================================================

def render_hackathon_demo_panel() -> str:
    """Renders the demonstration panel in Medium-Dark Blue styling."""
    return """
    <div style="background: #17284a; border: 1px solid #274170; border-radius: 18px; padding: 22px; margin-bottom: 24px; box-shadow: 0 8px 24px rgba(12, 21, 38, 0.35);">
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 14px;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span style="font-size: 20px;">🏆</span>
          <div>
            <h3 style="font-size: 17px; font-weight: 800; color: #FFFFFF; margin: 0;">TECHNICAL ARCHITECTURE & DEMO SUITE</h3>
            <div style="font-size: 12.5px; color: #CBD5E1;">Core system architecture highlights & instant pre-configured demonstration pathways.</div>
          </div>
        </div>
        <span style="font-size: 11.5px; font-weight: 700; color: #38bdf8; padding: 4px 10px; background: #13223f; border: 1px solid #38bdf8; border-radius: 14px;">READY FOR DEMO</span>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; margin-top: 14px;">
        <div style="background: #111f35; border: 1px solid #274170; border-radius: 12px; padding: 15px;">
          <div style="font-size: 12.5px; font-weight: 700; color: #38bdf8; margin-bottom: 6px;">1. Model-Free Orchestrator</div>
          <div style="font-size: 12.5px; color: #E2E8F0; line-height: 1.5;">StateGraph multi-agent routing with deterministic keyword heuristics, BM25 indexing, and TextRank graph centrality. Eliminates routing delay and delivers sub-15ms responses.</div>
        </div>
        <div style="background: #111f35; border: 1px solid #274170; border-radius: 12px; padding: 15px;">
          <div style="font-size: 12.5px; font-weight: 700; color: #60a5fa; margin-bottom: 6px;">2. Autonomous Video Studio</div>
          <div style="font-size: 12.5px; color: #E2E8F0; line-height: 1.5;">Full 16-stage pipeline powered by MoviePy & FFmpeg. Trims silence, synchronizes bilingual subtitles, crops 1080x1920 mobile reels, and draws handwritten notebook notes.</div>
        </div>
        <div style="background: #111f35; border: 1px solid #274170; border-radius: 12px; padding: 15px;">
          <div style="font-size: 12.5px; font-weight: 700; color: #34d399; margin-bottom: 6px;">3. Multi-Turn SQLite Persistence</div>
          <div style="font-size: 12.5px; color: #E2E8F0; line-height: 1.5;">SQLite database backend (`chat_history.db`) preserving session histories, past context, multimodal attachments, and real-time generation states without external database latency.</div>
        </div>
      </div>
    </div>
    """


# ==============================================================================
# 7. WORKSPACE TAB HEADER GENERATOR (MEDIUM-DARK BLUE)
# ==============================================================================

def render_workspace_header(title: str, subtitle: str, badge: str, accent_color: str = "#38bdf8") -> str:
    """Generates a consistent header for individual workspace tabs in Medium-Dark Blue styling."""
    return f"""
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; padding: 18px 22px; background: #17284a; border: 1px solid #274170; border-left: 4px solid {accent_color}; border-radius: 14px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(12, 21, 38, 0.35);">
      <div>
        <h2 style="font-size: 20px; font-weight: 800; color: #FFFFFF; margin: 0 0 4px 0; letter-spacing: 0.2px;">{title}</h2>
        <div style="font-size: 13.5px; color: #CBD5E1;">{subtitle}</div>
      </div>
      <span style="font-size: 11.5px; font-weight: 700; color: {accent_color}; padding: 5px 12px; background: #111f35; border: 1px solid #274170; border-radius: 20px; letter-spacing: 0.5px;">
        ● {badge}
      </span>
    </div>
    """
