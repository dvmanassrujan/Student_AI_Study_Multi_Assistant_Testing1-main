"""
NEURAL NEXUS – AI COMMAND CENTER
Next-Generation UI/UX Design System & Premium Component Engine
for GenAI Video Intelligence Studio & Autonomous Production Platform.
"""

from typing import Dict, Any, List, Optional


# ==============================================================================
# 1. NEURAL NEXUS GLOBAL DESIGN SYSTEM (CSS)
# ==============================================================================

NEURAL_NEXUS_CSS = """
/* ==========================================================================
   NEURAL NEXUS – ENTERPRISE AI DESIGN SYSTEM
   Palette: Deep Midnight Navy (#070B18), Dark Indigo (#10172A),
            Electric Cyan (#00D9FF), Neon Violet (#8257FF),
            Royal Blue (#386BFF), Soft Magenta (#D65CFF)
   ========================================================================== */

:root {
  --nn-bg-midnight: #070B18;
  --nn-bg-navy: #0B1124;
  --nn-bg-indigo: #10172A;
  --nn-bg-card: rgba(16, 23, 42, 0.75);
  --nn-bg-card-hover: rgba(24, 34, 61, 0.88);
  --nn-bg-glass: rgba(255, 255, 255, 0.03);
  
  --nn-cyan: #00D9FF;
  --nn-cyan-glow: rgba(0, 217, 255, 0.35);
  --nn-violet: #8257FF;
  --nn-violet-glow: rgba(130, 87, 255, 0.35);
  --nn-blue: #386BFF;
  --nn-magenta: #D65CFF;
  --nn-emerald: #10B981;
  --nn-amber: #F59E0B;
  --nn-rose: #F43F5E;
  
  --nn-text-primary: #F5F7FF;
  --nn-text-secondary: #A7B1C8;
  --nn-text-muted: #64748B;
  
  --nn-border: rgba(255, 255, 255, 0.09);
  --nn-border-glow: rgba(0, 217, 255, 0.30);
  --nn-border-violet: rgba(130, 87, 255, 0.30);
  
  --nn-gradient-hero: linear-gradient(135deg, #00D9FF 0%, #386BFF 50%, #8257FF 100%);
  --nn-gradient-accent: linear-gradient(135deg, #00D9FF 0%, #8257FF 100%);
  --nn-gradient-magenta: linear-gradient(135deg, #8257FF 0%, #D65CFF 100%);
  --nn-gradient-emerald: linear-gradient(135deg, #10B981 0%, #00D9FF 100%);
  --nn-gradient-surface: linear-gradient(180deg, rgba(16, 23, 42, 0.85) 0%, rgba(11, 17, 36, 0.95) 100%);
  
  --nn-font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --nn-font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace;
}

/* Base Viewport & Body */
body, .gradio-container {
  background-color: var(--nn-bg-midnight) !important;
  background-image: 
    radial-gradient(circle at 12% 18%, rgba(56, 107, 255, 0.10) 0%, transparent 45%),
    radial-gradient(circle at 88% 22%, rgba(130, 87, 255, 0.09) 0%, transparent 45%),
    radial-gradient(circle at 50% 88%, rgba(0, 217, 255, 0.07) 0%, transparent 55%),
    linear-gradient(180deg, #070B18 0%, #090E20 100%) !important;
  color: var(--nn-text-primary) !important;
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
  background: #070B18;
}
::-webkit-scrollbar-thumb {
  background: rgba(56, 107, 255, 0.35);
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--nn-cyan);
}

/* Gradio Default Overrides */
footer { visibility: hidden !important; height: 0 !important; margin: 0 !important; }
.container { max-width: 1440px !important; margin: 0 auto !important; padding: 0 16px !important; }

/* ==========================================================================
   TABS STYLING – NEURAL NEXUS COMMAND BAR
   ========================================================================== */
.tabs {
  border-bottom: 1px solid var(--nn-border) !important;
  background: rgba(11, 17, 36, 0.60) !important;
  backdrop-filter: blur(12px) !important;
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
  color: var(--nn-text-secondary) !important;
  border: 1px solid transparent !important;
  border-radius: 10px 10px 0 0 !important;
  padding: 10px 16px !important;
  font-size: 13.5px !important;
  font-weight: 600 !important;
  letter-spacing: 0.3px !important;
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.tab-nav button:hover {
  color: var(--nn-text-primary) !important;
  background: rgba(255, 255, 255, 0.04) !important;
  border-color: rgba(255, 255, 255, 0.08) !important;
}

.tab-nav button.selected {
  color: #FFFFFF !important;
  background: linear-gradient(180deg, rgba(0, 217, 255, 0.15) 0%, rgba(130, 87, 255, 0.08) 100%) !important;
  border: 1px solid var(--nn-border-glow) !important;
  border-bottom: 2px solid var(--nn-cyan) !important;
  box-shadow: 0 -4px 16px -2px rgba(0, 217, 255, 0.25) !important;
}

/* Nested Sub-Tabs */
.tabs .tabs {
  background: rgba(7, 11, 24, 0.50) !important;
  border-radius: 8px !important;
  margin-top: 10px !important;
}

.tabs .tabs .tab-nav button {
  padding: 7px 14px !important;
  font-size: 12.5px !important;
}

.tabs .tabs .tab-nav button.selected {
  border-bottom: 2px solid var(--nn-violet) !important;
  box-shadow: 0 -4px 14px -2px rgba(130, 87, 255, 0.25) !important;
}

/* ==========================================================================
   CARDS, PANELS & ACCORDIONS (GLASSMORPHISM)
   ========================================================================== */
.gr-box, .gr-panel, div[class*="block"] {
  background-color: var(--nn-bg-card) !important;
  backdrop-filter: blur(16px) !important;
  border: 1px solid var(--nn-border) !important;
  border-radius: 14px !important;
  transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}

div[class*="block"]:hover {
  border-color: rgba(0, 217, 255, 0.20) !important;
}

/* Accordions */
.gr-accordion {
  background: var(--nn-bg-card) !important;
  border: 1px solid var(--nn-border) !important;
  border-radius: 12px !important;
  margin-bottom: 12px !important;
}

.gr-accordion > .label-wrap {
  background: rgba(255, 255, 255, 0.02) !important;
  padding: 10px 16px !important;
}

/* ==========================================================================
   INPUTS, TEXTAREAS & DROPDOWNS
   ========================================================================== */
input[type="text"], input[type="number"], textarea, select, .gr-input {
  background-color: rgba(7, 11, 24, 0.85) !important;
  color: var(--nn-text-primary) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: 10px !important;
  font-size: 13.5px !important;
  transition: all 0.2s ease !important;
}

input[type="text"]:focus, input[type="number"]:focus, textarea:focus, select:focus {
  border-color: var(--nn-cyan) !important;
  box-shadow: 0 0 0 3px rgba(0, 217, 255, 0.18) !important;
  outline: none !important;
}

/* Labels */
label span, .gr-form > label {
  color: var(--nn-text-secondary) !important;
  font-size: 12.5px !important;
  font-weight: 600 !important;
  letter-spacing: 0.4px !important;
  text-transform: uppercase !important;
  margin-bottom: 6px !important;
}

/* ==========================================================================
   BUTTONS (PRIMARY & SECONDARY)
   ========================================================================== */
button.primary, button.gr-button-primary {
  background: linear-gradient(135deg, #00D9FF 0%, #386BFF 50%, #8257FF 100%) !important;
  color: #FFFFFF !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  letter-spacing: 0.4px !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 11px 22px !important;
  box-shadow: 0 4px 18px -2px rgba(0, 217, 255, 0.35) !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
  cursor: pointer !important;
}

button.primary:hover, button.gr-button-primary:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 24px -2px rgba(0, 217, 255, 0.55), 0 0 12px rgba(130, 87, 255, 0.30) !important;
  filter: brightness(1.08) !important;
}

button.primary:active, button.gr-button-primary:active {
  transform: translateY(0) !important;
}

button.secondary, button.gr-button-secondary {
  background: rgba(16, 23, 42, 0.80) !important;
  color: var(--nn-text-primary) !important;
  border: 1px solid rgba(255, 255, 255, 0.14) !important;
  font-weight: 600 !important;
  font-size: 13.5px !important;
  border-radius: 10px !important;
  padding: 10px 20px !important;
  transition: all 0.2s ease !important;
}

button.secondary:hover, button.gr-button-secondary:hover {
  background: rgba(26, 36, 64, 0.95) !important;
  border-color: var(--nn-cyan) !important;
  color: var(--nn-cyan) !important;
  box-shadow: 0 0 14px rgba(0, 217, 255, 0.20) !important;
}

button.stop, button[variant="stop"] {
  background: linear-gradient(135deg, rgba(244, 63, 94, 0.2) 0%, rgba(225, 29, 72, 0.3) 100%) !important;
  border: 1px solid rgba(244, 63, 94, 0.45) !important;
  color: #FDA4AF !important;
  font-weight: 600 !important;
  border-radius: 10px !important;
  transition: all 0.2s ease !important;
}

button.stop:hover, button[variant="stop"]:hover {
  background: rgba(225, 29, 72, 0.4) !important;
  color: #FFFFFF !important;
  box-shadow: 0 0 16px rgba(244, 63, 94, 0.35) !important;
}

/* ==========================================================================
   CHATBOT STYLING
   ========================================================================== */
.chatbot {
  background: rgba(7, 11, 24, 0.70) !important;
  border: 1px solid var(--nn-border) !important;
  border-radius: 14px !important;
}

.chatbot .message.user, .chatbot [data-testid="user"] {
  background: linear-gradient(135deg, rgba(56, 107, 255, 0.25) 0%, rgba(130, 87, 255, 0.20) 100%) !important;
  border: 1px solid rgba(0, 217, 255, 0.25) !important;
  border-radius: 14px 14px 2px 14px !important;
  color: #FFFFFF !important;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2) !important;
}

.chatbot .message.bot, .chatbot [data-testid="bot"] {
  background: rgba(16, 23, 42, 0.85) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 14px 14px 14px 2px !important;
  color: var(--nn-text-primary) !important;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3) !important;
}

/* ==========================================================================
   KEYFRAME ANIMATIONS
   ========================================================================== */
@keyframes nnPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(0.92); }
}

@keyframes nnFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-6px); }
}

@keyframes nnGlowBorder {
  0%, 100% { border-color: rgba(0, 217, 255, 0.25); box-shadow: 0 0 16px rgba(0, 217, 255, 0.15); }
  50% { border-color: rgba(130, 87, 255, 0.40); box-shadow: 0 0 24px rgba(130, 87, 255, 0.25); }
}

@keyframes nnShimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.nn-pulse-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--nn-cyan);
  box-shadow: 0 0 10px var(--nn-cyan);
  animation: nnPulse 2s infinite ease-in-out;
  margin-right: 6px;
}

.nn-pulse-emerald {
  background-color: var(--nn-emerald) !important;
  box-shadow: 0 0 10px var(--nn-emerald) !important;
}
"""


# ==============================================================================
# 2. CINEMATIC TOP NAVIGATION & HERO SECTION
# ==============================================================================

def render_cinematic_hero(model_name: str = "llama3.2:latest", is_online: bool = True) -> str:
    """Renders the futuristic Neural Nexus Top Bar and Hero Section."""
    status_color = "#10B981" if is_online else "#F59E0B"
    status_label = "NEURAL ENGINE ONLINE" if is_online else "LOCAL FALLBACK MODE"
    
    return f"""
    <div style="font-family: system-ui, -apple-system, sans-serif; margin-bottom: 24px;">
      <!-- TOP NAVIGATION BAR -->
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px; padding: 14px 22px; background: rgba(11, 17, 36, 0.75); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; backdrop-filter: blur(20px); box-shadow: 0 8px 32px rgba(0,0,0,0.4); margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 14px;">
          <div style="width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, #00D9FF 0%, #386BFF 50%, #8257FF 100%); display: flex; align-items: center; justify-content: center; box-shadow: 0 0 20px rgba(0, 217, 255, 0.45);">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
              <polyline points="2 17 12 22 22 17"></polyline>
              <polyline points="2 12 12 17 22 12"></polyline>
            </svg>
          </div>
          <div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-size: 17px; font-weight: 800; letter-spacing: 0.8px; background: linear-gradient(135deg, #FFFFFF 30%, #00D9FF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">GENAI STUDIO</span>
              <span style="font-size: 10px; font-weight: 700; padding: 2px 7px; background: rgba(0, 217, 255, 0.15); border: 1px solid rgba(0, 217, 255, 0.35); border-radius: 6px; color: #00D9FF; letter-spacing: 0.6px;">ENTERPRISE v2.5</span>
            </div>
            <div style="font-size: 11px; color: #A7B1C8; font-weight: 500;">Autonomous Production & Video Intelligence Platform</div>
          </div>
        </div>

        <!-- ENGINE TELEMETRY PILL -->
        <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
          <div style="display: inline-flex; align-items: center; gap: 8px; padding: 7px 14px; background: rgba(7, 11, 24, 0.85); border: 1px solid rgba(0, 217, 255, 0.25); border-radius: 30px;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: {status_color}; box-shadow: 0 0 10px {status_color}; animation: nnPulse 2s infinite;"></span>
            <span style="font-size: 12px; font-weight: 700; color: #FFFFFF; letter-spacing: 0.4px;">{status_label}</span>
            <span style="font-size: 11px; padding: 2px 8px; background: rgba(130, 87, 255, 0.2); border-radius: 12px; color: #8257FF; font-family: monospace;">{model_name}</span>
          </div>
          <div style="display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px; background: rgba(7, 11, 24, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 30px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#00D9FF" stroke-width="2.2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 14 14"></polyline></svg>
            <span style="font-size: 11.5px; color: #A7B1C8; font-weight: 600;">Port 7860</span>
            <span style="font-size: 10px; color: #10B981; font-weight: 700;">● AUTO-RECOVER</span>
          </div>
        </div>
      </div>

      <!-- CINEMATIC HERO SECTION -->
      <div style="position: relative; overflow: hidden; padding: 48px 36px 42px 36px; background: radial-gradient(circle at 80% 20%, rgba(130, 87, 255, 0.15) 0%, transparent 50%), radial-gradient(circle at 20% 80%, rgba(0, 217, 255, 0.15) 0%, transparent 50%), linear-gradient(180deg, rgba(16, 23, 42, 0.85) 0%, rgba(7, 11, 24, 0.95) 100%); border: 1px solid rgba(0, 217, 255, 0.22); border-radius: 20px; box-shadow: 0 16px 48px -12px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.12);">
        <!-- Ambient Circuit Grid Lines (SVG Overlay) -->
        <svg style="position: absolute; right: 0; top: 0; width: 450px; height: 100%; opacity: 0.18; pointer-events: none;" viewBox="0 0 400 300" fill="none">
          <circle cx="200" cy="150" r="120" stroke="#00D9FF" stroke-width="1.5" stroke-dasharray="4 6"/>
          <circle cx="200" cy="150" r="60" stroke="#8257FF" stroke-width="1.5"/>
          <line x1="200" y1="30" x2="200" y2="270" stroke="#386BFF" stroke-width="1" stroke-dasharray="2 4"/>
          <line x1="80" y1="150" x2="320" y2="150" stroke="#386BFF" stroke-width="1" stroke-dasharray="2 4"/>
          <circle cx="200" cy="30" r="4" fill="#00D9FF"/>
          <circle cx="200" cy="270" r="4" fill="#8257FF"/>
          <circle cx="80" cy="150" r="4" fill="#D65CFF"/>
          <circle cx="320" cy="150" r="4" fill="#00D9FF"/>
        </svg>

        <div style="position: relative; z-index: 2; max-width: 900px;">
          <!-- Pre-badge -->
          <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px; background: rgba(0, 217, 255, 0.10); border: 1px solid rgba(0, 217, 255, 0.30); border-radius: 20px; margin-bottom: 18px;">
            <span style="font-size: 13px;">⚡</span>
            <span style="font-size: 11.5px; font-weight: 700; letter-spacing: 0.7px; color: #00D9FF; text-transform: uppercase;">Next-Gen Multimodal AI Ecosystem</span>
          </div>

          <!-- Main Heading -->
          <h1 style="font-size: 40px; font-weight: 900; line-height: 1.15; margin: 0 0 12px 0; letter-spacing: -0.5px; background: linear-gradient(135deg, #FFFFFF 20%, #E0F2FE 55%, #00D9FF 90%, #8257FF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            INTELLIGENCE THAT CREATES.<br/>AI THAT TRANSFORMS.
          </h1>

          <!-- Supporting Heading -->
          <h2 style="font-size: 18px; font-weight: 600; color: #386BFF; margin: 0 0 14px 0; letter-spacing: 0.2px;">
            GenAI Video Intelligence Studio & Autonomous Production Platform
          </h2>

          <!-- Description -->
          <p style="font-size: 15px; line-height: 1.6; color: #A7B1C8; margin: 0 0 24px 0; max-width: 780px;">
            Experience the next generation of autonomous AI production, multimodal intelligence, educational automation, and intelligent content creation. Orchestrating 11 specialized agent nodes with 16-stage video synthesis, neural dubbing, and real-time YouTube analytics.
          </p>

          <!-- Metrics Highlights -->
          <div style="display: flex; align-items: center; gap: 20px; flex-wrap: wrap; margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 10px;">
              <div style="font-size: 24px; font-weight: 800; color: #00D9FF;">16</div>
              <div style="font-size: 11.5px; color: #A7B1C8; line-height: 1.3;">Autonomous<br/>Studio Stages</div>
            </div>
            <div style="width: 1px; height: 32px; background: rgba(255,255,255,0.1);"></div>
            <div style="display: flex; align-items: center; gap: 10px;">
              <div style="font-size: 24px; font-weight: 800; color: #8257FF;">11</div>
              <div style="font-size: 11.5px; color: #A7B1C8; line-height: 1.3;">Multi-Agent<br/>Neural Nodes</div>
            </div>
            <div style="width: 1px; height: 32px; background: rgba(255,255,255,0.1);"></div>
            <div style="display: flex; align-items: center; gap: 10px;">
              <div style="font-size: 24px; font-weight: 800; color: #10B981;">30+</div>
              <div style="font-size: 11.5px; color: #A7B1C8; line-height: 1.3;">Multilingual<br/>Neural Dubs</div>
            </div>
            <div style="width: 1px; height: 32px; background: rgba(255,255,255,0.1);"></div>
            <div style="display: flex; align-items: center; gap: 10px;">
              <div style="font-size: 24px; font-weight: 800; color: #D65CFF;">&lt;50ms</div>
              <div style="font-size: 11.5px; color: #A7B1C8; line-height: 1.3;">Instant Stream<br/>Response</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    """


# ==============================================================================
# 3. SIX PREMIUM AI MODULES (INTERACTIVE ECOSYSTEM)
# ==============================================================================

def render_six_ai_module_cards() -> str:
    """Renders the 6 interactive module cards specified in Section 4."""
    modules = [
        {
            "id": "MOD 01",
            "title": "Autonomous Video Intelligence Studio",
            "icon": """<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#00D9FF" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect><line x1="7" y1="2" x2="7" y2="22"></line><line x1="17" y1="2" x2="17" y2="22"></line><line x1="2" y1="12" x2="22" y2="12"></line><line x1="2" y1="7" x2="7" y2="7"></line><line x1="2" y1="17" x2="7" y2="17"></line><line x1="17" y1="17" x2="22" y2="17"></line><line x1="17" y1="7" x2="22" y2="7"></line></svg>""",
            "accent": "#00D9FF",
            "badge": "16-STAGE PIPELINE",
            "desc": "An intelligent 16-stage video production pipeline that automates video editing, silence removal, caption synchronization, vertical shorts generation, and educational content production.",
            "tags": ["Silence Cut", "Shorts <60s", "Ruled Notes", "Cover Studio"]
        },
        {
            "id": "MOD 02",
            "title": "YouTube Intelligence",
            "icon": """<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#8257FF" stroke-width="2"><path d="M2.5 17a24.12 24.12 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.56 49.56 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.12 24.12 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.55 49.55 0 0 1-16.2 0A2 2 0 0 1 2.5 17"></path><polygon points="10 15 15 12 10 9 10 15"></polygon></svg>""",
            "accent": "#8257FF",
            "badge": "SENTIMENT & NLP",
            "desc": "Transform YouTube content into actionable intelligence through audience sentiment analysis, comment classification, engagement analytics, retention insights, and intelligent recommendations.",
            "tags": ["Sentiment AI", "Comment Mining", "Retention Curve", "Export CSV"]
        },
        {
            "id": "MOD 03",
            "title": "AI Chat & Multimodal Lab",
            "icon": """<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#386BFF" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path><circle cx="9" cy="10" r="1" fill="#386BFF"></circle><circle cx="12" cy="10" r="1" fill="#386BFF"></circle><circle cx="15" cy="10" r="1" fill="#386BFF"></circle></svg>""",
            "accent": "#386BFF",
            "badge": "MULTI-TURN PERSISTENT",
            "desc": "An intelligent multimodal workspace supporting conversational AI, persistent memory, image generation, image-to-video workflows, and coding assistance.",
            "tags": ["SQLite Memory", "Text → Image", "Text → Video", "<50ms Stream"]
        },
        {
            "id": "MOD 04",
            "title": "Coding Mentor & DSA Lab",
            "icon": """<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>""",
            "accent": "#10B981",
            "badge": "BIG-O ANALYZER",
            "desc": "An autonomous coding mentor providing programming guidance, debugging assistance, algorithm explanations, complexity analysis, and problem-solving support.",
            "tags": ["Debug Engine", "Big-O Analysis", "DSA Trainer", "Syntax Repair"]
        },
        {
            "id": "MOD 05",
            "title": "Exam Preparation & Quizzes",
            "icon": """<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path><polyline points="9 9 12 12 16 7"></polyline></svg>""",
            "accent": "#F59E0B",
            "badge": "ASSESSMENT ENGINE",
            "desc": "An AI-powered examination preparation system generating important questions, interactive quizzes, mock tests, and customized flashcards.",
            "tags": ["MCQ Generator", "Answer Keys", "Detailed Logic", "Mock Tests"]
        },
        {
            "id": "MOD 06",
            "title": "Professor Robocat 3D Studio",
            "icon": """<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#D65CFF" stroke-width="2"><circle cx="12" cy="12" r="9"></circle><path d="M9 10h.01"></path><path d="M15 10h.01"></path><path d="M8 15s1.5 2 4 2 4-2 4-2"></path><polyline points="7 4 9 8 5 8"></polyline><polyline points="17 4 15 8 19 8"></polyline></svg>""",
            "accent": "#D65CFF",
            "badge": "3D MULTILINGUAL",
            "desc": "An educational 3D video generation studio creating animated cartoon explainers with synchronized multilingual audio.",
            "tags": ["30+ Languages", "Storyboard AI", "3D Characters", "Neural Voice"]
        }
    ]
    
    cards_html = []
    for m in modules:
        tags_html = "".join([f'<span style="font-size: 11px; padding: 3px 8px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 6px; color: #A7B1C8;">{tag}</span>' for tag in m["tags"]])
        card = f"""
        <div style="background: rgba(16, 23, 42, 0.75); border: 1px solid rgba(255, 255, 255, 0.09); border-radius: 16px; padding: 22px; backdrop-filter: blur(16px); box-shadow: 0 8px 24px rgba(0,0,0,0.3); transition: all 0.25s ease; display: flex; flex-direction: column; justify-content: space-between; position: relative; overflow: hidden;">
          <div style="position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, {m["accent"]}, transparent);"></div>
          
          <div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;">
              <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(7, 11, 24, 0.85); border: 1px solid rgba(255, 255, 255, 0.12); display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 14px rgba(0,0,0,0.3);">
                {m["icon"]}
              </div>
              <div style="text-align: right;">
                <span style="font-size: 10px; font-weight: 800; color: #64748B; font-family: monospace; letter-spacing: 1px;">{m["id"]}</span>
                <div><span style="font-size: 10px; font-weight: 700; color: {m["accent"]}; padding: 2px 7px; background: rgba(255, 255, 255, 0.04); border: 1px solid {m["accent"]}44; border-radius: 12px;">{m["badge"]}</span></div>
              </div>
            </div>
            
            <h3 style="font-size: 17px; font-weight: 700; color: #F5F7FF; margin: 0 0 10px 0; letter-spacing: 0.1px;">{m["title"]}</h3>
            <p style="font-size: 13px; line-height: 1.55; color: #A7B1C8; margin: 0 0 16px 0;">{m["desc"]}</p>
          </div>
          
          <div>
            <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px;">
              {tags_html}
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding-top: 10px; border-top: 1px solid rgba(255, 255, 255, 0.06);">
              <span style="font-size: 11px; color: #10B981; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">
                <span style="width: 6px; height: 6px; border-radius: 50%; background: #10B981;"></span> OPERATIONAL
              </span>
              <span style="font-size: 11.5px; color: {m["accent"]}; font-weight: 700; letter-spacing: 0.2px;">Launch Tab →</span>
            </div>
          </div>
        </div>
        """
        cards_html.append(card)
        
    return f"""
    <div style="margin-bottom: 30px;">
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; flex-wrap: wrap; gap: 8px;">
        <div>
          <h2 style="font-size: 20px; font-weight: 800; color: #F5F7FF; margin: 0 0 4px 0; letter-spacing: 0.3px;">
            💎 SIX CORE AI INTELLIGENCE MODULES
          </h2>
          <div style="font-size: 13px; color: #A7B1C8;">Autonomous pipelines and interactive multimodal intelligence tools.</div>
        </div>
        <div style="font-size: 12px; color: #00D9FF; font-weight: 700; padding: 4px 12px; background: rgba(0, 217, 255, 0.08); border: 1px solid rgba(0, 217, 255, 0.25); border-radius: 20px;">
          ● 6 OF 6 WORKSPACES READY
        </div>
      </div>
      
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 18px;">
        {"".join(cards_html)}
      </div>
    </div>
    """


# ==============================================================================
# 4. MULTI-AGENT NEURAL INTELLIGENCE VISUALIZATION (11 NODES)
# ==============================================================================

def render_multi_agent_neural_visualization() -> str:
    """Renders the interactive SVG node-based multi-agent visualization."""
    agents = [
        {"name": "Study Concept Tutor", "role": "Step-by-step concept explanations & analogies", "id": "study_agent", "color": "#00D9FF"},
        {"name": "Study Plan Strategist", "role": "Day-by-day & week-by-week timetables & milestones", "id": "study_planner_agent", "color": "#386BFF"},
        {"name": "Assessment & Exam Coach", "role": "High-yield MCQs, answer keys & mock test generator", "id": "exam_agent", "color": "#F59E0B"},
        {"name": "Senior Coding Mentor", "role": "Algorithmic debugging & Big-O complexity analysis", "id": "coding_agent", "color": "#10B981"},
        {"name": "Full-Stack Project Architect", "role": "Module architecture & database schema blueprinting", "id": "project_agent", "color": "#8257FF"},
        {"name": "Document Intelligence", "role": "PDF, DOCX & paper extraction with summary synthesis", "id": "document_agent", "color": "#00D9FF"},
        {"name": "Neural Audio Narrator", "role": "Spoken-word instructional audio & script voiceover", "id": "audio_agent", "color": "#D65CFF"},
        {"name": "Cinematic Video Director", "role": "Visual cue generation & storyboard scene creation", "id": "video_agent", "color": "#F43F5E"},
        {"name": "Spaced Repetition Memory", "role": "Flashcard decks, mnemonics & cognitive retention", "id": "memory_agent", "color": "#386BFF"},
        {"name": "Adaptive Learning Coach", "role": "Progress telemetry & personalized weakness targeting", "id": "personalization_agent", "color": "#10B981"},
        {"name": "YouTube Video Intelligence", "role": "Sentiment mining, retention analysis & comment intelligence", "id": "youtube_agent", "color": "#8257FF"}
    ]
    
    agent_items_html = []
    for a in agents:
        agent_items_html.append(f"""
        <div style="background: rgba(7, 11, 24, 0.75); border: 1px solid rgba(255,255,255,0.08); border-left: 3px solid {a["color"]}; border-radius: 10px; padding: 10px 14px; display: flex; flex-direction: column; justify-content: space-between;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
            <span style="font-size: 13px; font-weight: 700; color: #FFFFFF;">{a["name"]}</span>
            <span style="font-size: 9.5px; font-weight: 700; color: #10B981; font-family: monospace;">ACTIVE</span>
          </div>
          <div style="font-size: 11.5px; color: #A7B1C8; line-height: 1.35; margin-bottom: 6px;">{a["role"]}</div>
          <div style="font-size: 10px; color: {a["color"]}; font-family: monospace; font-weight: 600;">id: {a["id"]}</div>
        </div>
        """)
        
    return f"""
    <div style="background: rgba(16, 23, 42, 0.85); border: 1px solid rgba(0, 217, 255, 0.20); border-radius: 18px; padding: 24px; backdrop-filter: blur(16px); box-shadow: 0 12px 36px rgba(0,0,0,0.4); margin-bottom: 30px;">
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, #8257FF 0%, #386BFF 100%); display: flex; align-items: center; justify-content: center;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>
          </div>
          <div>
            <h3 style="font-size: 18px; font-weight: 800; color: #FFFFFF; margin: 0; letter-spacing: 0.2px;">MULTI-AGENT NEURAL INTELLIGENCE CENTER</h3>
            <div style="font-size: 12px; color: #A7B1C8;">Autonomous LangGraph StateMachine orchestrating 11 specialized agent nodes in real time.</div>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 11px; padding: 4px 10px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 20px; color: #10B981; font-weight: 700;">
            ● 11/11 AGENTS ROUTED
          </span>
          <span style="font-size: 11px; padding: 4px 10px; background: rgba(0, 217, 255, 0.15); border: 1px solid rgba(0, 217, 255, 0.35); border-radius: 20px; color: #00D9FF; font-weight: 700;">
            FAST-PATH 0ms LATENCY
          </span>
        </div>
      </div>

      <!-- CENTRAL ORCHESTRATION BANNER -->
      <div style="background: radial-gradient(circle at center, rgba(56, 107, 255, 0.15) 0%, rgba(7, 11, 24, 0.85) 100%); border: 1px dashed rgba(0, 217, 255, 0.35); border-radius: 12px; padding: 14px 20px; text-align: center; margin-bottom: 20px;">
        <span style="font-size: 11px; font-weight: 800; color: #00D9FF; letter-spacing: 1.2px; text-transform: uppercase;">Central Orchestrator Core</span>
        <div style="font-size: 15px; font-weight: 700; color: #FFFFFF; margin-top: 2px;">LangGraph Router Node (StateGraph Entrypoint)</div>
        <div style="font-size: 12px; color: #A7B1C8; margin-top: 4px;">Direct state mapping: task_type ➔ next_agent ➔ specialized execution node ➔ SQLite persistence</div>
      </div>

      <!-- AGENT NODES GRID -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px;">
        {"".join(agent_items_html)}
      </div>
    </div>
    """


# ==============================================================================
# 5. 16-STAGE AUTONOMOUS VIDEO PRODUCTION PIPELINE VISUALIZER
# ==============================================================================

def render_16_stage_pipeline_visualizer() -> str:
    """Renders the 16-stage pipeline visualizer as requested in Section 7."""
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
        ("13", "Viral Hook & Title Gen", "Synthesizes high-CTR headlines with Ollama"),
        ("14", "Vertical Cover Art", "Renders 1080x1920 branded gradient covers"),
        ("15", "Ruled Notebook Notes", "Compiles handwritten-style revision study sheets"),
        ("16", "Master H.264 Export", "Encodes optimized MP4 for streaming & LMS")
    ]
    
    stage_cards = []
    for num, name, desc in stages:
        stage_cards.append(f"""
        <div style="background: rgba(7, 11, 24, 0.75); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 12px 14px; position: relative;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
            <span style="font-size: 11px; font-weight: 800; color: #00D9FF; font-family: monospace;">STAGE {num}</span>
            <span style="font-size: 9px; font-weight: 700; color: #10B981; padding: 1px 6px; background: rgba(16, 185, 129, 0.15); border-radius: 8px;">READY</span>
          </div>
          <div style="font-size: 13px; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">{name}</div>
          <div style="font-size: 11px; color: #A7B1C8; line-height: 1.35;">{desc}</div>
        </div>
        """)
        
    return f"""
    <div style="background: rgba(16, 23, 42, 0.85); border: 1px solid rgba(130, 87, 255, 0.25); border-radius: 18px; padding: 22px; backdrop-filter: blur(16px); box-shadow: 0 12px 36px rgba(0,0,0,0.4); margin-bottom: 26px;">
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; margin-bottom: 16px;">
        <div>
          <h3 style="font-size: 18px; font-weight: 800; color: #FFFFFF; margin: 0; letter-spacing: 0.2px;">
            🎬 16-STAGE AUTONOMOUS VIDEO PRODUCTION PIPELINE
          </h3>
          <div style="font-size: 12px; color: #A7B1C8;">Fully automated end-to-end studio pipeline executed via MoviePy 2.1.2 & FFmpeg 7.1.</div>
        </div>
        <div style="font-size: 11.5px; color: #8257FF; font-weight: 700; padding: 4px 12px; background: rgba(130, 87, 255, 0.12); border: 1px solid rgba(130, 87, 255, 0.3); border-radius: 20px;">
          ● SEQUENTIAL STAGE PIPELINE
        </div>
      </div>
      
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 10px;">
        {"".join(stage_cards)}
      </div>
    </div>
    """


# ==============================================================================
# 6. HACKATHON LIVE DEMO MODE & TECHNICAL ARCHITECTURE
# ==============================================================================

def render_hackathon_demo_panel() -> str:
    """Renders the Hackathon demonstration shortcuts and system architecture view."""
    return """
    <div style="background: linear-gradient(135deg, rgba(16, 23, 42, 0.9) 0%, rgba(7, 11, 24, 0.95) 100%); border: 1px solid rgba(0, 217, 255, 0.25); border-radius: 18px; padding: 22px; backdrop-filter: blur(16px); margin-bottom: 24px;">
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 14px;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span style="font-size: 20px;">🏆</span>
          <div>
            <h3 style="font-size: 17px; font-weight: 800; color: #FFFFFF; margin: 0;">HACKATHON EVALUATOR & LIVE DEMO SUITE</h3>
            <div style="font-size: 12px; color: #A7B1C8;">Technical architecture highlights & instant pre-configured demonstration pathways.</div>
          </div>
        </div>
        <span style="font-size: 11px; font-weight: 700; color: #00D9FF; padding: 4px 10px; background: rgba(0, 217, 255, 0.1); border: 1px solid rgba(0, 217, 255, 0.25); border-radius: 14px;">READY FOR DEMO</span>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; margin-top: 14px;">
        <div style="background: rgba(7, 11, 24, 0.7); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 14px;">
          <div style="font-size: 12px; font-weight: 700; color: #00D9FF; margin-bottom: 6px;">1. LangGraph Orchestrator</div>
          <div style="font-size: 12px; color: #A7B1C8; line-height: 1.45;">StateGraph multi-agent routing with instant keyword heuristics and fallback to local Meta Llama 3.2. Eliminates routing delay and delivers <50ms initial feedback.</div>
        </div>
        <div style="background: rgba(7, 11, 24, 0.7); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 14px;">
          <div style="font-size: 12px; font-weight: 700; color: #8257FF; margin-bottom: 6px;">2. Autonomous Video Studio</div>
          <div style="font-size: 12px; color: #A7B1C8; line-height: 1.45;">Full 16-stage pipeline powered by MoviePy 2.1.2 & FFmpeg 7.1. Trims silence, synchronizes bilingual subtitles, crops 1080x1920 mobile reels, and draws handwritten notebook notes.</div>
        </div>
        <div style="background: rgba(7, 11, 24, 0.7); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 14px;">
          <div style="font-size: 12px; font-weight: 700; color: #10B981; margin-bottom: 6px;">3. Multi-Turn SQLite Persistence</div>
          <div style="font-size: 12px; color: #A7B1C8; line-height: 1.45;">SQLite database backend (`chat_history.db`) preserving session histories, past context, multimodal attachments, and real-time generation states without external database latency.</div>
        </div>
      </div>
    </div>
    """


# ==============================================================================
# 7. WORKSPACE TAB HEADER GENERATOR
# ==============================================================================

def render_workspace_header(title: str, subtitle: str, badge: str, accent_color: str = "#00D9FF") -> str:
    """Generates a consistent, futuristic Neural Nexus header for individual workspace tabs."""
    return f"""
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; padding: 18px 22px; background: rgba(16, 23, 42, 0.75); border: 1px solid rgba(255, 255, 255, 0.08); border-left: 4px solid {accent_color}; border-radius: 14px; backdrop-filter: blur(16px); margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.25);">
      <div>
        <h2 style="font-size: 20px; font-weight: 800; color: #FFFFFF; margin: 0 0 4px 0; letter-spacing: 0.2px;">{title}</h2>
        <div style="font-size: 13px; color: #A7B1C8;">{subtitle}</div>
      </div>
      <span style="font-size: 11px; font-weight: 700; color: {accent_color}; padding: 5px 12px; background: rgba(255, 255, 255, 0.04); border: 1px solid {accent_color}44; border-radius: 20px; letter-spacing: 0.5px;">
        ● {badge}
      </span>
    </div>
    """
