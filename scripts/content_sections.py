"""Content sections for the Mech-Exosuit Design Document.
Functions return flowables that get appended to the story.
"""

from reportlab.platypus import Paragraph, Spacer, PageBreak, KeepTogether, CondPageBreak, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors

# Import sections
from sections.s01_concept import build_section_01
from sections.s02_architecture import build_section_02
from sections.s03_defs_xml import build_section_03
from sections.s04_damage_death import build_section_04
from sections.s05_bay_ui import build_section_05
from sections.s06_battery_bandwidth import build_section_06
from sections.s07_subcoreinfo_ce import build_section_07
from sections.s08_balancing import build_section_08
from sections.s09_tech_tree import build_section_09
from sections.s10_roadmap import build_section_10
from sections.s11_checklist import build_section_11
from sections.s12_glossary import build_section_12


def build_all_sections(story, ctx):
    """Build all 12 content sections and append to story."""
    sections = [
        build_section_01,
        build_section_02,
        build_section_03,
        build_section_04,
        build_section_05,
        build_section_06,
        build_section_07,
        build_section_08,
        build_section_09,
        build_section_10,
        build_section_11,
        build_section_12,
    ]
    
    for i, builder in enumerate(sections, start=1):
        builder(story, ctx)
        if i < len(sections):
            story.append(Spacer(1, 24))
    
    return story
