"""
MCP Server for Electoral Dashboard UI/UX Analysis and Improvements

This server provides tools to analyze and improve the Dash/Plotly electoral dashboard
with focus on:
- Responsive design
- Color consistency (political party colors)
- Accessibility (WCAG 2.1 AA compliance)
- Modern UI/UX best practices
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any
import sys
import asyncio

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent, Resource
    import mcp.server.stdio
except ImportError:
    print("Error: MCP package not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Initialize MCP Server
server = Server("electoral-dashboard-designer")

# Load design system configuration
CONFIG_PATH = Path(__file__).parent / "config" / "design_system.json"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    DESIGN_SYSTEM = json.load(f)

PARTY_COLORS = DESIGN_SYSTEM["party_colors"]
RESPONSIVE_BREAKPOINTS = DESIGN_SYSTEM["responsive_breakpoints"]
ACCESSIBILITY_RULES = DESIGN_SYSTEM["accessibility_rules"]
UI_BEST_PRACTICES = DESIGN_SYSTEM["ui_best_practices"]
DASHBOARD_SPECIFIC = DESIGN_SYSTEM["dashboard_specific"]


# ============================================================================
# TOOLS
# ============================================================================

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List all available UI/UX analysis tools"""
    return [
        Tool(
            name="analyze_responsive_design",
            description="Analyze Dash dashboard code for responsive design patterns using Bootstrap grid system",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code of the Dash dashboard (app.py)"
                    }
                },
                "required": ["code"]
            }
        ),
        Tool(
            name="validate_party_colors",
            description="Validate that political party colors match the defined design system",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code containing PARTY_COLORS dictionary"
                    }
                },
                "required": ["code"]
            }
        ),
        Tool(
            name="check_accessibility",
            description="Check dashboard for WCAG 2.1 AA accessibility compliance",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Dash dashboard code to analyze"
                    }
                },
                "required": ["code"]
            }
        ),
        Tool(
            name="suggest_ui_improvements",
            description="Suggest modern UI/UX improvements for the dashboard",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Dashboard code to analyze"
                    },
                    "focus_area": {
                        "type": "string",
                        "enum": ["layout", "typography", "colors", "spacing", "charts", "all"],
                        "description": "Specific area to focus on (default: all)"
                    }
                },
                "required": ["code"]
            }
        ),
        Tool(
            name="get_design_recommendations",
            description="Get specific design recommendations based on current trends and best practices",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["responsive", "colors", "typography", "spacing", "charts", "cards", "maps"],
                        "description": "Category of design recommendations"
                    }
                },
                "required": ["category"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute the requested tool"""

    if name == "analyze_responsive_design":
        return await analyze_responsive_design(arguments.get("code", ""))

    elif name == "validate_party_colors":
        return await validate_party_colors(arguments.get("code", ""))

    elif name == "check_accessibility":
        return await check_accessibility(arguments.get("code", ""))

    elif name == "suggest_ui_improvements":
        return await suggest_ui_improvements(
            arguments.get("code", ""),
            arguments.get("focus_area", "all")
        )

    elif name == "get_design_recommendations":
        return await get_design_recommendations(arguments.get("category", "responsive"))

    else:
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"Unknown tool: {name}"})
        )]


async def analyze_responsive_design(code: str) -> List[TextContent]:
    """Analyze responsive design patterns in Dash code"""
    issues = []
    recommendations = []
    score = 100

    # Check Bootstrap grid usage
    if "dbc.Row" not in code:
        issues.append({
            "severity": "high",
            "message": "No Bootstrap Row components found",
            "recommendation": "Use dbc.Row for responsive grid layouts"
        })
        score -= 20

    if "dbc.Col" not in code:
        issues.append({
            "severity": "high",
            "message": "No Bootstrap Col components found",
            "recommendation": "Use dbc.Col with responsive breakpoints (xs, sm, md, lg, xl)"
        })
        score -= 20

    # Check for responsive column definitions
    responsive_patterns = ["md=", "lg=", "sm=", "xs=", "xl="]
    has_responsive = any(pattern in code for pattern in responsive_patterns)

    if not has_responsive:
        issues.append({
            "severity": "medium",
            "message": "No responsive breakpoints defined in columns",
            "recommendation": "Add responsive breakpoints: dbc.Col(..., xs=12, md=6, lg=4)",
            "example": "dbc.Col(content, xs=12, sm=6, md=4, lg=3)"
        })
        score -= 15

    # Check container usage
    if "container-fluid" not in code and "fluid=True" not in code:
        recommendations.append({
            "type": "enhancement",
            "message": "Consider using fluid container for full-width layouts",
            "code": "dbc.Container([...], fluid=True)"
        })
        score -= 5

    # Check for fixed heights that break responsiveness
    fixed_height_pattern = r'style=\{[^}]*["\']height["\']\s*:\s*["\'](\d+)px'
    fixed_heights = re.findall(fixed_height_pattern, code)
    if fixed_heights:
        issues.append({
            "severity": "medium",
            "message": f"Found {len(fixed_heights)} fixed pixel heights",
            "recommendation": "Use relative units (%, vh) or let content determine height",
            "locations": fixed_heights[:3]  # Show first 3 examples
        })
        score -= 10

    # Check for viewport meta tag (should be in HTML head, might not be in app.py)
    if "viewport" not in code.lower():
        recommendations.append({
            "type": "info",
            "message": "Ensure viewport meta tag is present in HTML",
            "note": "Dash usually handles this automatically"
        })

    result = {
        "score": max(0, score),
        "status": "excellent" if score >= 90 else "good" if score >= 70 else "needs_improvement",
        "issues": issues,
        "recommendations": recommendations,
        "responsive_breakpoints": RESPONSIVE_BREAKPOINTS,
        "summary": f"Found {len(issues)} issues and {len(recommendations)} recommendations"
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2, ensure_ascii=False)
    )]


async def validate_party_colors(code: str) -> List[TextContent]:
    """Validate political party colors against design system"""
    violations = []
    warnings = []
    valid_colors = set()

    # Extract PARTY_COLORS dictionary from code
    party_colors_pattern = r'PARTY_COLORS\s*=\s*\{([^}]+)\}'
    match = re.search(party_colors_pattern, code, re.DOTALL)

    if not match:
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": "PARTY_COLORS dictionary not found in code",
                "recommendation": "Define PARTY_COLORS at the top of your app.py"
            })
        )]

    colors_block = match.group(1)

    # Extract each party and its color
    color_entries = re.findall(r"['\"]([^'\"]+)['\"]\s*:\s*['\"]([#\w]+)['\"]", colors_block)

    for party, color in color_entries:
        party_clean = party.strip()
        color_clean = color.strip().upper()

        # Check if party exists in design system
        if party_clean in PARTY_COLORS:
            expected_color = PARTY_COLORS[party_clean]["primary"].upper()

            if color_clean != expected_color:
                violations.append({
                    "party": party_clean,
                    "current_color": color_clean,
                    "expected_color": expected_color,
                    "severity": "high",
                    "fix": f"Change '{party_clean}': '{color_clean}' to '{expected_color}'"
                })
            else:
                valid_colors.add(party_clean)
        else:
            warnings.append({
                "party": party_clean,
                "message": f"Party '{party_clean}' not in design system",
                "color": color_clean,
                "suggestion": "Add to design system or verify party name spelling"
            })

    # Check for missing parties
    defined_parties = {party for party, _ in color_entries}
    expected_parties = set(PARTY_COLORS.keys()) - {"DEFAULT"}
    missing_parties = expected_parties - defined_parties

    if missing_parties:
        warnings.append({
            "type": "missing_parties",
            "parties": list(missing_parties),
            "message": f"{len(missing_parties)} parties from design system not defined in code"
        })

    result = {
        "valid": len(violations) == 0,
        "validation_score": (len(valid_colors) / len(PARTY_COLORS)) * 100 if PARTY_COLORS else 0,
        "violations": violations,
        "warnings": warnings,
        "valid_parties": list(valid_colors),
        "summary": f"{len(valid_colors)} valid, {len(violations)} violations, {len(warnings)} warnings",
        "design_system_reference": {
            party: data["primary"]
            for party, data in PARTY_COLORS.items()
        }
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2, ensure_ascii=False)
    )]


async def check_accessibility(code: str) -> List[TextContent]:
    """Check WCAG 2.1 AA accessibility compliance"""
    issues = []
    score = 100

    # Check for ARIA labels
    if "aria-label" not in code.lower():
        issues.append({
            "severity": "medium",
            "wcag_criterion": "1.3.1 Info and Relationships",
            "message": "No ARIA labels found",
            "recommendation": "Add aria-label to interactive elements for screen readers",
            "example": "dcc.Graph(..., config={'displayModeBar': False}, aria={'label': 'Electoral map'})"
        })
        score -= 15

    # Check for alt text on images (if any)
    if "<img" in code or "html.Img" in code:
        if "alt=" not in code:
            issues.append({
                "severity": "high",
                "wcag_criterion": "1.1.1 Non-text Content",
                "message": "Images without alt text detected",
                "recommendation": "Add alt attribute to all images",
                "example": "html.Img(src='...', alt='Description of image')"
            })
            score -= 20

    # Check heading structure
    heading_pattern = r'html\.H([1-6])\('
    headings = re.findall(heading_pattern, code)
    if headings:
        heading_levels = [int(h) for h in headings]
        # Check if headings are in sequential order
        for i in range(len(heading_levels) - 1):
            if heading_levels[i+1] - heading_levels[i] > 1:
                issues.append({
                    "severity": "medium",
                    "wcag_criterion": "1.3.1 Info and Relationships",
                    "message": f"Heading levels skip from H{heading_levels[i]} to H{heading_levels[i+1]}",
                    "recommendation": "Use sequential heading levels (H1 → H2 → H3, not H1 → H3)"
                })
                score -= 10
                break
    else:
        issues.append({
            "severity": "low",
            "wcag_criterion": "1.3.1 Info and Relationships",
            "message": "No semantic headings found",
            "recommendation": "Use html.H1-H6 for headings instead of styled divs"
        })
        score -= 5

    # Check color contrast (basic check for hex colors)
    color_pattern = r'["\']color["\']\s*:\s*["\']#([0-9A-Fa-f]{6})["\']'
    colors_found = re.findall(color_pattern, code)

    if colors_found:
        # Basic luminance check (this is simplified, real contrast requires background color)
        low_contrast_colors = []
        for color in colors_found:
            # Convert hex to RGB and calculate relative luminance (simplified)
            r = int(color[0:2], 16) / 255
            g = int(color[2:4], 16) / 255
            b = int(color[4:6], 16) / 255
            luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b

            # Very dark or very light colors might have contrast issues
            if luminance < 0.1 or luminance > 0.9:
                low_contrast_colors.append(f"#{color}")

        if low_contrast_colors:
            issues.append({
                "severity": "medium",
                "wcag_criterion": "1.4.3 Contrast (Minimum)",
                "message": f"Potential contrast issues with {len(low_contrast_colors)} colors",
                "recommendation": "Verify contrast ratio is at least 4.5:1 for normal text",
                "tool": "Use https://webaim.org/resources/contrastchecker/",
                "colors": low_contrast_colors[:5]
            })
            score -= 10

    # Check keyboard navigation support
    if "tabIndex" not in code and "tab_index" not in code:
        issues.append({
            "severity": "low",
            "wcag_criterion": "2.1.1 Keyboard",
            "message": "No explicit keyboard navigation support found",
            "recommendation": "Ensure interactive elements are keyboard accessible",
            "note": "Dash components usually handle this automatically"
        })
        score -= 5

    # Check for focus indicators
    if "focus" not in code.lower():
        issues.append({
            "severity": "low",
            "wcag_criterion": "2.4.7 Focus Visible",
            "message": "No custom focus indicators defined",
            "recommendation": "Ensure focus indicators are visible (browser defaults usually sufficient)",
            "note": "CSS: :focus { outline: 2px solid #005fcc; }"
        })
        score -= 5

    result = {
        "accessibility_score": max(0, score),
        "compliance_level": "AA" if score >= 80 else "Partial AA" if score >= 60 else "Needs Work",
        "issues": issues,
        "total_issues": len(issues),
        "high_severity": len([i for i in issues if i["severity"] == "high"]),
        "medium_severity": len([i for i in issues if i["severity"] == "medium"]),
        "low_severity": len([i for i in issues if i["severity"] == "low"]),
        "summary": f"Accessibility score: {score}/100 - {len(issues)} issues found",
        "wcag_reference": "https://www.w3.org/WAI/WCAG21/quickref/"
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2, ensure_ascii=False)
    )]


async def suggest_ui_improvements(code: str, focus_area: str = "all") -> List[TextContent]:
    """Suggest UI/UX improvements based on modern best practices"""
    suggestions = []

    areas_to_check = [focus_area] if focus_area != "all" else ["layout", "typography", "colors", "spacing", "charts"]

    for area in areas_to_check:
        if area == "layout":
            suggestions.extend(analyze_layout(code))
        elif area == "typography":
            suggestions.extend(analyze_typography(code))
        elif area == "colors":
            suggestions.extend(analyze_colors(code))
        elif area == "spacing":
            suggestions.extend(analyze_spacing(code))
        elif area == "charts":
            suggestions.extend(analyze_charts(code))

    result = {
        "focus_area": focus_area,
        "total_suggestions": len(suggestions),
        "suggestions": suggestions,
        "priority_actions": [s for s in suggestions if s.get("priority") == "high"][:5],
        "design_system_reference": UI_BEST_PRACTICES
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2, ensure_ascii=False)
    )]


def analyze_layout(code: str) -> List[Dict]:
    """Analyze layout patterns"""
    suggestions = []

    # Check for proper grid usage
    if "dbc.Row" in code and "dbc.Col" not in code:
        suggestions.append({
            "category": "layout",
            "priority": "high",
            "message": "Using dbc.Row without dbc.Col",
            "recommendation": "Always wrap content in dbc.Col within dbc.Row",
            "example": "dbc.Row([dbc.Col(content, md=6), dbc.Col(content2, md=6)])"
        })

    # Check for container usage
    if "dbc.Container" not in code:
        suggestions.append({
            "category": "layout",
            "priority": "medium",
            "message": "No dbc.Container wrapper found",
            "recommendation": "Wrap your layout in dbc.Container for proper margins",
            "example": "app.layout = dbc.Container([...], fluid=True)"
        })

    # Check for spacing utilities
    if "className" in code and "mb-" not in code and "mt-" not in code:
        suggestions.append({
            "category": "layout",
            "priority": "low",
            "message": "Not using Bootstrap spacing utilities",
            "recommendation": "Use Bootstrap margin classes for consistent spacing",
            "example": "dbc.Card(..., className='mb-3 mt-2')",
            "reference": "mb-1 to mb-5 for bottom margin, mt-1 to mt-5 for top margin"
        })

    return suggestions


def analyze_typography(code: str) -> List[Dict]:
    """Analyze typography usage"""
    suggestions = []

    # Check for heading hierarchy
    if "html.H1" not in code:
        suggestions.append({
            "category": "typography",
            "priority": "medium",
            "message": "No H1 heading found",
            "recommendation": "Add a main H1 heading for your dashboard title",
            "example": "html.H1('Dashboard Electoral Córdoba Capital', className='text-center mb-4')"
        })

    # Check for text utilities
    if "text-center" not in code and "text-left" not in code:
        suggestions.append({
            "category": "typography",
            "priority": "low",
            "message": "Not using text alignment utilities",
            "recommendation": "Use Bootstrap text utilities for better alignment",
            "example": "className='text-center' or 'text-muted' or 'text-primary'"
        })

    return suggestions


def analyze_colors(code: str) -> List[Dict]:
    """Analyze color usage"""
    suggestions = []

    # Check for hardcoded colors outside PARTY_COLORS
    color_pattern = r'["\']#([0-9A-Fa-f]{6})["\']'
    colors = re.findall(color_pattern, code)

    # Get party colors to exclude from check
    party_color_values = {data["primary"].replace("#", "").upper() for data in PARTY_COLORS.values()}

    non_party_colors = [f"#{c}" for c in colors if c.upper() not in party_color_values]

    if len(non_party_colors) > 10:
        suggestions.append({
            "category": "colors",
            "priority": "medium",
            "message": f"Found {len(non_party_colors)} hardcoded colors",
            "recommendation": "Create a color palette variable for non-party colors",
            "example": "CHART_COLORS = {'background': '#FFFFFF', 'border': '#2E86AB', 'text': '#333333'}"
        })

    # Check for color consistency
    if "#000000" in code or "#FFFFFF" in code:
        suggestions.append({
            "category": "colors",
            "priority": "low",
            "message": "Using pure black/white colors",
            "recommendation": "Consider using softer shades for better visual comfort",
            "example": "Use #1a1a1a instead of #000000, #f8f9fa instead of #ffffff"
        })

    return suggestions


def analyze_spacing(code: str) -> List[Dict]:
    """Analyze spacing patterns"""
    suggestions = []

    # Check for margin usage in style dicts
    margin_pattern = r'["\']margin["\']\s*:\s*["\']?(\d+)px'
    margins = re.findall(margin_pattern, code)

    if margins:
        # Check if using 8px grid
        non_grid_margins = [m for m in margins if int(m) % 8 != 0]
        if non_grid_margins:
            suggestions.append({
                "category": "spacing",
                "priority": "low",
                "message": f"Found {len(non_grid_margins)} margins not on 8px grid",
                "recommendation": "Use 8px base unit for consistent spacing",
                "scale": UI_BEST_PRACTICES["spacing"]["scale"],
                "example": "Use 8, 16, 24, 32 instead of arbitrary values"
            })

    return suggestions


def analyze_charts(code: str) -> List[Dict]:
    """Analyze chart configurations"""
    suggestions = []

    # Check for Plotly deprecation warnings
    if "choroplethmapbox" in code.lower():
        suggestions.append({
            "category": "charts",
            "priority": "high",
            "message": "Using deprecated choroplethmapbox",
            "recommendation": "Update to choroplethmap (MapLibre)",
            "migration": "https://plotly.com/python/mapbox-to-maplibre/",
            "example": "go.Choroplethmap(...) instead of go.Choroplethmapbox(...)"
        })

    if "scattermapbox" in code.lower():
        suggestions.append({
            "category": "charts",
            "priority": "high",
            "message": "Using deprecated scattermapbox",
            "recommendation": "Update to scattermap (MapLibre)",
            "migration": "https://plotly.com/python/mapbox-to-maplibre/",
            "example": "go.Scattermap(...) instead of go.Scattermapbox(...)"
        })

    # Check for chart responsiveness
    if "dcc.Graph" in code:
        if "responsive=True" not in code and "config={" not in code:
            suggestions.append({
                "category": "charts",
                "priority": "medium",
                "message": "Charts may not be fully responsive",
                "recommendation": "Add responsive config to dcc.Graph",
                "example": "dcc.Graph(..., config={'responsive': True})"
            })

    # Check for proper chart sizing
    if 'style={"height"' in code and "vh" not in code:
        suggestions.append({
            "category": "charts",
            "priority": "medium",
            "message": "Using fixed pixel heights for charts",
            "recommendation": "Consider using viewport units for better responsiveness",
            "example": 'style={"height": "60vh"} instead of "600px"'
        })

    return suggestions


async def get_design_recommendations(category: str) -> List[TextContent]:
    """Get design recommendations for specific category"""
    recommendations = {}

    if category == "responsive":
        recommendations = {
            "category": "Responsive Design",
            "best_practices": [
                "Use Bootstrap grid system (dbc.Row + dbc.Col) for all layouts",
                "Define breakpoints for all columns: xs=12, md=6, lg=4",
                "Test on mobile (375px), tablet (768px), and desktop (1200px)",
                "Use relative units (%, rem, vh/vw) instead of fixed pixels",
                "Ensure touch targets are at least 44x44px on mobile"
            ],
            "breakpoints": RESPONSIVE_BREAKPOINTS,
            "code_examples": {
                "basic_grid": "dbc.Row([dbc.Col(content, xs=12, md=6, lg=4)])",
                "responsive_spacing": "className='mb-3 mb-md-4 mb-lg-5'",
                "fluid_container": "dbc.Container([...], fluid=True)"
            }
        }

    elif category == "colors":
        recommendations = {
            "category": "Color System",
            "party_colors": PARTY_COLORS,
            "best_practices": [
                "Always use PARTY_COLORS dictionary for political party colors",
                "Maintain contrast ratio >= 4.5:1 for text (WCAG AA)",
                "Use softer shades (#f8f9fa) instead of pure white",
                "Use near-black (#1a1a1a) instead of pure black",
                "Ensure color-blind accessibility with patterns/labels"
            ],
            "recommended_palette": {
                "background": "#F8F9FA",
                "text": "#1A1A1A",
                "border": "#2E86AB",
                "muted": "#6C757D",
                "success": "#28A745",
                "warning": "#FFC107",
                "error": "#DC3545"
            }
        }

    elif category == "typography":
        recommendations = {
            "category": "Typography",
            "font_stack": UI_BEST_PRACTICES["typography"]["font_family"],
            "scale": UI_BEST_PRACTICES["typography"]["scale"],
            "best_practices": [
                "Use semantic headings (H1-H6) in sequential order",
                "Set base font size to 14-16px for dashboard readability",
                "Maintain 1.5 line-height for body text",
                "Use font-weight: 500-600 for emphasis, not just bold (700)",
                "Ensure sufficient contrast for all text (4.5:1 minimum)"
            ],
            "code_examples": {
                "heading": "html.H1('Title', className='text-center mb-4')",
                "subtitle": "html.H5('Subtitle', className='text-muted')",
                "small_text": "html.Small('Footnote', className='text-muted')"
            }
        }

    elif category == "spacing":
        recommendations = {
            "category": "Spacing System",
            "base_unit": UI_BEST_PRACTICES["spacing"]["base_unit"],
            "scale": UI_BEST_PRACTICES["spacing"]["scale"],
            "best_practices": [
                "Use 8px base unit for all spacing (margin, padding)",
                "Apply spacing scale: 4, 8, 12, 16, 24, 32, 48, 64px",
                "Use Bootstrap spacing utilities: m-0 to m-5, p-0 to p-5",
                "Maintain consistent spacing within cards and sections",
                "Increase spacing on larger screens (responsive spacing)"
            ],
            "bootstrap_classes": {
                "margin": "m-1 (4px), m-2 (8px), m-3 (16px), m-4 (24px), m-5 (48px)",
                "padding": "p-1 (4px), p-2 (8px), p-3 (16px), p-4 (24px), p-5 (48px)",
                "gap": "g-1 to g-5 for grid gaps in Row/Col"
            }
        }

    elif category == "charts":
        recommendations = {
            "category": "Chart Design",
            "plotly_config": DASHBOARD_SPECIFIC,
            "best_practices": [
                "Update from choroplethmapbox to choroplethmap (MapLibre)",
                "Update from scattermapbox to scattermap (MapLibre)",
                "Use responsive: True in graph config",
                "Set proper aspect ratios for different chart types",
                "Add clear axis labels and titles",
                "Use party colors consistently in charts",
                "Enable hover tooltips with formatted data"
            ],
            "code_examples": {
                "responsive_graph": "dcc.Graph(figure=fig, config={'responsive': True})",
                "map_style": "go.Choroplethmap(geojson=..., marker_line_width=1.5)",
                "layout": "fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))"
            },
            "migration_guide": "https://plotly.com/python/mapbox-to-maplibre/"
        }

    elif category == "cards":
        recommendations = {
            "category": "Card Design",
            "card_styles": DASHBOARD_SPECIFIC["card_styles"],
            "best_practices": [
                "Use dbc.Card for grouping related content",
                "Add subtle shadows for depth (0 2px 4px rgba(0,0,0,0.1))",
                "Use 8-12px border-radius for modern look",
                "Maintain consistent padding (16-24px)",
                "Add hover effects for interactive cards",
                "Use CardHeader for section titles"
            ],
            "code_examples": {
                "basic_card": "dbc.Card([dbc.CardHeader('Title'), dbc.CardBody(content)], className='mb-3')",
                "metric_card": "dbc.Card(dbc.CardBody([html.H6('Metric'), html.H3(value)]))"
            }
        }

    elif category == "maps":
        recommendations = {
            "category": "Map Design",
            "map_config": DASHBOARD_SPECIFIC["map_styles"],
            "best_practices": [
                "Use elegant border width (1.5-2px) for seccional boundaries",
                "Set border color to subtle blue (#2E86AB) not harsh black",
                "Use 0.6 fill opacity for visibility with underlying map",
                "Increase hover opacity to 0.8 for interactivity",
                "Add clear tooltips with seccional name, party, votes",
                "Include permanent labels for seccional numbers",
                "Center map on Córdoba coordinates (-31.4201, -64.1888)",
                "Set appropriate zoom level (11-12 for city view)"
            ],
            "code_examples": {
                "choropleth": "go.Choroplethmap(..., marker_opacity=0.6, marker_line_width=1.5)",
                "labels": "go.Scattermap(mode='text', text=labels, textfont=dict(size=11))"
            }
        }

    return [TextContent(
        type="text",
        text=json.dumps(recommendations, indent=2, ensure_ascii=False)
    )]


# ============================================================================
# RESOURCES
# ============================================================================

@server.list_resources()
async def list_resources() -> List[Resource]:
    """List available design system resources"""
    return [
        Resource(
            uri="design://system",
            name="Complete Design System",
            mimeType="application/json",
            description="Full design system configuration including colors, spacing, typography"
        ),
        Resource(
            uri="design://party-colors",
            name="Political Party Color Palette",
            mimeType="application/json",
            description="Official colors for all political parties"
        ),
        Resource(
            uri="design://responsive-breakpoints",
            name="Responsive Breakpoints",
            mimeType="application/json",
            description="Bootstrap breakpoints for responsive design"
        ),
        Resource(
            uri="design://accessibility-rules",
            name="Accessibility Guidelines",
            mimeType="application/json",
            description="WCAG 2.1 AA compliance rules"
        )
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read design system resource"""
    if uri == "design://system":
        return json.dumps(DESIGN_SYSTEM, indent=2, ensure_ascii=False)
    elif uri == "design://party-colors":
        return json.dumps(PARTY_COLORS, indent=2, ensure_ascii=False)
    elif uri == "design://responsive-breakpoints":
        return json.dumps(RESPONSIVE_BREAKPOINTS, indent=2, ensure_ascii=False)
    elif uri == "design://accessibility-rules":
        return json.dumps(ACCESSIBILITY_RULES, indent=2, ensure_ascii=False)
    else:
        raise ValueError(f"Unknown resource URI: {uri}")


# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
