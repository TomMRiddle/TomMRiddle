from reportlab.platypus import Flowable
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, FrameBreak
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.units import mm
from reportlab.lib import colors

# Custom Flowable for two-column bullet lists
class TwoColumnBullets(Flowable):
    def __init__(self, items, style, width, gap=12):
        Flowable.__init__(self)
        self.items = items
        self.style = style
        self.width = width
        self.gap = gap
        self.col_count = 2
        split = (len(items) + 1) // self.col_count
        self.col1 = items[:split]
        self.col2 = items[split:]
        self.col_width = (self.width - self.gap) / self.col_count

    def wrap(self, availWidth, availHeight):
        # Calculate required height for both columns
        from reportlab.lib.utils import simpleSplit
        fontName = self.style.fontName
        fontSize = self.style.fontSize
        leading = self.style.leading if hasattr(self.style, 'leading') else fontSize + 2
        col1_height = 0
        col2_height = 0
        for item in self.col1:
            lines = simpleSplit(item, fontName, fontSize, self.col_width)
            col1_height += leading * len(lines)
        for item in self.col2:
            lines = simpleSplit(item, fontName, fontSize, self.col_width)
            col2_height += leading * len(lines)
        self._height = max(col1_height, col2_height)
        return self.width, self._height

    def draw(self):
        from reportlab.lib.utils import simpleSplit
        canvas = self.canv
        x0 = 0
        fontName = self.style.fontName
        fontSize = self.style.fontSize
        leading = self.style.leading if hasattr(self.style, 'leading') else fontSize + 2
        textColor = self.style.textColor if hasattr(self.style, 'textColor') else colors.black
        canvas.saveState()
        canvas.setFont(fontName, fontSize)
        canvas.setFillColor(textColor)
        # Draw first column
        y1 = 0
        bullet_indent = -10  # negative to hang outside
        text_indent = 0      # start text at column edge
        for item in self.col1:
            lines = simpleSplit(item, fontName, fontSize, self.col_width)
            for idx, line in enumerate(lines):
                if idx == 0:
                    # Draw bullet hanging outside and first line flush left
                    canvas.drawString(x0 + bullet_indent, self._height - leading - y1, u"\u2022 ")
                    canvas.drawString(x0 + text_indent, self._height - leading - y1, line)
                else:
                    # Draw subsequent lines flush left
                    canvas.drawString(x0 + text_indent, self._height - leading - y1, line)
                y1 += leading
        # Draw second column
        y2 = 0
        for item in self.col2:
            lines = simpleSplit(item, fontName, fontSize, self.col_width)
            for idx, line in enumerate(lines):
                if idx == 0:
                    canvas.drawString(x0 + self.col_width + self.gap + bullet_indent, self._height - leading - y2, u"\u2022 ")
                    canvas.drawString(x0 + self.col_width + self.gap + text_indent, self._height - leading - y2, line)
                else:
                    canvas.drawString(x0 + self.col_width + self.gap + text_indent, self._height - leading - y2, line)
                y2 += leading
        canvas.restoreState()

styles = getSampleStyleSheet()
pdfmetrics.registerFont(TTFont('Alice-Regular', r'C:\USERS\PC\FONTBASE\PROVIDERS\GOOGLE\ALICE-REGULAR.TTF'))
pdfmetrics.registerFont(TTFont('Bahnschrift-SemiBoldCondensed', r'C:\WINDOWS\FONTS\BAHNSCHRIFT.TTF'))
styles.add(ParagraphStyle(name='HeaderName', fontName='Bahnschrift-SemiBoldCondensed', fontSize=18, alignment=TA_LEFT, spaceAfter=2))
styles.add(ParagraphStyle(name='HeaderContact', fontName='Alice-Regular', fontSize=10.5, alignment=TA_LEFT, textColor=colors.HexColor('#444444'), spaceAfter=2))
styles.add(ParagraphStyle(name='SectionTitle', fontName='Bahnschrift-SemiBoldCondensed', fontSize=13, alignment=TA_LEFT, spaceBefore=0, spaceAfter=0, textColor=colors.HexColor('#003366')))
styles.add(ParagraphStyle(name='SubsectionTitle', fontName='Bahnschrift-SemiBoldCondensed', fontSize=11, alignment=TA_LEFT, spaceBefore=0, spaceAfter=0, leftIndent=6, textColor=colors.HexColor('#222222')))
styles.add(ParagraphStyle(name='SubsectionDates', fontName='Alice-Regular', fontSize=9, alignment=TA_RIGHT, spaceAfter=0, leading=10, textColor=colors.HexColor('#666666')))
styles.add(ParagraphStyle(name='NormalText', fontName='Alice-Regular', fontSize=10.5, alignment=TA_LEFT, spaceBefore=3, spaceAfter=3))
styles.add(ParagraphStyle(name='BulletText', fontName='Alice-Regular', fontSize=10.5, leftIndent=6, spaceAfter=2, alignment=TA_LEFT))

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_MARGIN = 15 * mm
RIGHT_MARGIN = 15 * mm
TOP_MARGIN = 12 * mm
BOTTOM_MARGIN = 12 * mm

# Define frames for header and two columns
header_frame_height = 45  # increased for name, contact, and spacing
header_frame = Frame(
    LEFT_MARGIN,
    PAGE_HEIGHT - TOP_MARGIN - header_frame_height,
    PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN,
    header_frame_height,
    id='header',
)

main_col_width = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN - 90  # wide left column
right_col_width = 90  # narrow right column

main_frame_first = Frame(
    LEFT_MARGIN,
    BOTTOM_MARGIN,
    main_col_width,
    PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN - header_frame_height,
    id='main'
)
right_frame_first = Frame(
    LEFT_MARGIN + main_col_width + 10,
    BOTTOM_MARGIN,
    right_col_width,
    PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN - header_frame_height,
    id='right'
)
main_frame_rest = Frame(
    LEFT_MARGIN,
    BOTTOM_MARGIN,
    main_col_width,
    PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN,
    id='main'
)
right_frame_rest = Frame(
    LEFT_MARGIN + main_col_width + 10,
    BOTTOM_MARGIN,
    right_col_width,
    PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN,
    id='right'
)

doc = BaseDocTemplate("Victor_Ek_CV.pdf", pagesize=A4, leftMargin=LEFT_MARGIN, rightMargin=RIGHT_MARGIN, topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN)
from reportlab.platypus import NextPageTemplate
first_page_template = PageTemplate(id='HeaderAndTwoCol', frames=[header_frame, main_frame_first, right_frame_first])
rest_page_template = PageTemplate(id='TwoCol', frames=[main_frame_rest, right_frame_rest])
doc.addPageTemplates([first_page_template, rest_page_template])

def section_title(title):
    # Add spacer only if previous item is a paragraph (not a title)
    if main_story and isinstance(main_story[-1], Paragraph) and main_story[-1].style.name == 'NormalText':
        main_story.append(Spacer(1, 6))
    main_story.append(Paragraph(title, styles['SectionTitle']))

def subsection_title(subtitle, dates=None):
    # Add spacer only if previous item is a paragraph (not a title)
    if main_story and isinstance(main_story[-1], Paragraph) and (main_story[-1].style.name == 'NormalText' or main_story[-1].style.name == 'BulletText'):
        main_story.append(Spacer(1, 6))
    if dates:
        # Heading and date on same line, date right-aligned
        from reportlab.platypus import Table, TableStyle
        heading = Paragraph(subtitle, styles['SubsectionTitle'])
        period = Paragraph(dates, styles['SubsectionDates'])
        t = Table([[heading, period]], colWidths=[main_col_width*0.68, main_col_width*0.32])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('ALIGN', (1,0), (1,0), 'RIGHT'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        main_story.append(t)
    else:
        main_story.append(Paragraph(subtitle, styles['SubsectionTitle']))

def paragraph(text):
    main_story.append(Paragraph(text, styles['NormalText']))

def bullet_points(items):
    # Use custom Flowable for true two-column bullets
    para_width = main_col_width  # match paragraph width
    gap = 18  # gap between columns
    main_story.append(TwoColumnBullets(items, styles['BulletText'], para_width, gap=gap))
    main_story.append(Spacer(1, 3))



# Header content (full width)
header_story = [
    Paragraph(
        '<font name="Bahnschrift-SemiBoldCondensed" size="18" color="#000000">Victor Ek </font>'
        '<font name="Bahnschrift-SemiBoldCondensed" size="12" color="#003366">Clarity Creator | Improvement Finder</font>',
        styles['NormalText']
    ),
    Spacer(1, 6),
    Paragraph("victor.ek@gmail.com | +46702705536 | <a href=\"https://linkedin.com/in/victorek\">linkedin.com/in/victorek</a> | Gothenburg, Sweden", styles['HeaderContact'])
]

# Left column content (main)
main_story = []

# Professional Summary
section_title("Professional Summary")
paragraph(
    "Creative and technically grounded professional with a Bachelor's in Media Technology and vocational training in visual communication and software testing. "
    "Over ten years' experience in public sector digital production, support, and content delivery. "
    "Practical, collaborative, and focused on clarity in systems, visuals, and workflows. "
    "Skilled in bridging technical and creative teams to deliver effective solutions. "
    "Passionate about continuous learning and improving user experience."
)

# Work Experience
section_title("Work Experience")

subsection_title("Method Developer / First-Line IT Support", "Kungsbacka Municipality<br/>2020–2024")
paragraph(
    "Provided support for department-specific administrative systems, handled access permissions, and performed technical troubleshooting on both hardware and software. "
    "Trained internal staff on mobile systems and configured Android devices. Generated data reports from the Combine system using SQL Server. "
    "Served as technical lead for monthly live-streams of municipal council meetings."
)

subsection_title("Digital Producer / Information Officer / Graphic Designer", "Kungsbacka Municipality<br/>2015–2020")
paragraph(
    "Produced internal and external communication materials. Designed layouts and graphics for both print and digital formats. "
    "Supported communication departments with publishing tools and digital workflows, maintaining consistent visual identity across media."
)

# Education
section_title("Education")

subsection_title("YH Diploma – Software Testing with Test Automation", "IT-högskolan<br/>2024–Ongoing")
paragraph(
    "Vocational program in test automation, emphasizing requirements-based, early and frequent testing as part of the SDLC."
)
paragraph("The program covers:")
bullet_points([
    "Requirements analysis and test design",
    "Test automation",
    "Choosing suitable test tools",
    "Continuous integration and testing",
    "Using TDD, BDD, ATDD",
    "Version control in teams",
])

subsection_title("Bachelor’s Degree in Media Technology", "Blekinge Institute of Technology<br/>2009–2012")
paragraph(
    "This program focused on web development, usability, user-centered design, and digital production. "
    "It included both technical and design-oriented coursework and emphasized project-based learning. "
    "The final thesis addressed web usability in applied settings."
)
paragraph("Coursework included:")
bullet_points([
    "Web development and scripting (HTML, CSS, JavaScript, PHP, SQL)",
    "Java and object-oriented programming",
    "Digital media production and applied web technology",
    "Visual design and rhetoric",
])

main_story.append(Spacer(1, 6))

subsection_title("YH Diploma – Visual Communication and Project Management", "Mediability<br/>2007–2009")
paragraph(
    "Program in graphic design, communication strategy, and project-based production."
)
paragraph("The curriculum included:")
bullet_points([
    "Graphic design, focus on creativity, target audience, and use context",
    "Project management for structured teamwork in creative environments",
    "Market and trend analysis to anticipate developments in the design industry",
    "Entrepreneurial skills in freelance or business contexts",
    "Graphic production from idea to finished product",
    "Marketing communication, development of marketing and business plans"
])
paragraph("The program emphasized adaptability, collaboration, and practical experience.")

# Right column content (skills/languages)

SKILL_COLOR = '#003366'  # blue used for section titles
right_story = []
right_story.append(Paragraph("Skills", styles['SectionTitle']))
right_story.append(Paragraph(
    f"<font color='{SKILL_COLOR}'><b>Test automation:</b></font> Pipelines, TDD, BDD, test case design, Selenium, Robot framework, <br/>"
    f"<font color='{SKILL_COLOR}'><b>Tools and systems:</b></font><br/>SQL Server, MySQL, Git, Azure DevOps, Agentic AI<br/>"
    f"<font color='{SKILL_COLOR}'><b>Workflow and collaboration:</b></font> Agile methods, internal communications, documentation<br/>"
    f"<font color='{SKILL_COLOR}'><b>Web and interface development:</b></font> HTML, CSS, JavaScript, PHP, Python, ASP.NET WebAPI, Java<br/>"
    f"<font color='{SKILL_COLOR}'><b>Design and content production:</b></font> Adobe Creative Suite, UX/UI, print and web layout",
    styles['NormalText']))
right_story.append(Spacer(1, 12))
right_story.append(Paragraph("Languages", styles['SectionTitle']))
right_story.append(Paragraph("Swedish (native)<br/>English (fluent)", styles['NormalText']))

# Combine header, then FrameBreak, then main_story, then FrameBreak, then right_story
from reportlab.platypus import FrameBreak, NextPageTemplate
story = []
story.extend(header_story)
story.append(FrameBreak())
story.append(NextPageTemplate('TwoCol'))
story.extend(main_story)
story.append(FrameBreak())
story.extend(right_story)
doc.build(story)