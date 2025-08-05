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
                    canvas.drawString(x0 + bullet_indent, self._height - leading - y1, u"• ")
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
                    canvas.drawString(x0 + self.col_width + self.gap + bullet_indent, self._height - leading - y2, u"• ")
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
styles.add(ParagraphStyle(name='NormalText', fontName='Alice-Regular', fontSize=10.5, alignment=TA_LEFT, spaceBefore=3, spaceAfter=3, hyphenationLang='sv_SE'))
styles.add(ParagraphStyle(name='BulletText', fontName='Alice-Regular', fontSize=10.5, leftIndent=6, spaceAfter=2, alignment=TA_LEFT, hyphenationLang='sv_SE'))

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
right_col_width = 92  # narrow right column

main_frame_first = Frame(
    LEFT_MARGIN,
    BOTTOM_MARGIN,
    main_col_width,
    PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN - header_frame_height,
    id='main'
)
right_frame_first = Frame(
    LEFT_MARGIN + main_col_width + 8,
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

doc = BaseDocTemplate("Victor_Ek_CV_sv.pdf", pagesize=A4, leftMargin=LEFT_MARGIN, rightMargin=RIGHT_MARGIN, topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN)
from reportlab.platypus import NextPageTemplate
first_page_template = PageTemplate(id='HeaderAndTwoCol', frames=[header_frame, main_frame_first, right_frame_first])
rest_page_template = PageTemplate(id='TwoCol', frames=[main_frame_rest, right_frame_rest])
doc.addPageTemplates([first_page_template, rest_page_template])

def section_title(title):
    # Add spacer only if previous item is a paragraph (not a title)
    if main_story and (main_story[-1].style.name == 'NormalText' or main_story[-1].style.name == 'BulletText'):
        main_story.append(Spacer(1, 6))
    main_story.append(Paragraph(title, styles['SectionTitle']))

def subsection_title(subtitle, dates=None, first_col_width=0.68):
    # Add spacer only if previous item is a paragraph (not a title)
    if main_story and (main_story[-1].style.name == 'NormalText' or main_story[-1].style.name == 'BulletText'):
        main_story.append(Spacer(1, 6))
    if dates:
        # Heading and date on same line, date right-aligned
        from reportlab.platypus import Table, TableStyle
        heading = Paragraph(subtitle, styles['SubsectionTitle'])
        period = Paragraph(dates, styles['SubsectionDates'])
        t = Table([[heading, period]], colWidths=[main_col_width*first_col_width, main_col_width*(1-first_col_width)])
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
        '<font name="Bahnschrift-SemiBoldCondensed" size="12" color="#003366">Klarhetsskapare | Förbättringsfinnare</font>',
        styles['NormalText']
    ),
    Spacer(1, 6),
    Paragraph("victor.ek@gmail.com | 070-270 55 36 | <a href=\"https://linkedin.com/in/victorek\">linkedin.com/in/victorek</a> | Göteborg, Sverige", styles['HeaderContact'])
]

# Left column content (main)
main_story = []

# Professional Summary
section_title("Professionell Sammanfattning")
paragraph(
    "Kreativ och tekniskt grundad yrkesperson med en kandidatexamen i medieteknik och yrkesutbildning inom visuell kommunikation och mjukvarutestning. "
    "Över tio års erfarenhet av digital produktion, support och innehållsleverans inom offentlig sektor. "
    "Praktisk, samarbetsinriktad och fokuserad på tydlighet i system, visuella element och arbetsflöden. "
    "Van vid att överbrygga klyftan mellan tekniska och kreativa team för att leverera effektiva lösningar. "
    "Brinner för kontinuerligt lärande och att förbättra användarupplevelsen."
)

# Work Experience
section_title("Arbetslivserfarenhet")

subsection_title("Metodutvecklare / IT-support (första linjen)", "Kungsbacka kommun<br/>2020–2024")
paragraph(
    "Gav support för avdelningsspecifika administrativa system, hanterade åtkomstbehörigheter och utförde teknisk felsökning på både hård- och mjukvara. "
    "Utbildade intern personal i mobila system och konfigurerade Android-enheter. Genererade datarapporter från Combine-systemet med hjälp av SQL Server. "
    "Fungerade som tekniskt ansvarig för månatliga direktsändningar av kommunfullmäktiges möten."
)

subsection_title("Digital producent / Informatör / Grafisk formgivare", "Kungsbacka kommun<br/>2015–2020")
paragraph(
    "Producerade internt och externt kommunikationsmaterial. Designade layouter och grafik för både tryckta och digitala format. "
    "Stöttade kommunikationsavdelningar med publiceringsverktyg och digitala arbetsflöden, och upprätthöll en konsekvent visuell identitet över olika medier."
)

# Education
section_title("Utbildning")

subsection_title("YH-examen – Mjukvarutestare med testautomatisering", "IT-högskolan 2024–Pågående")
paragraph(
    "Yrkesprogram inom testautomatisering med tonvikt på kravbaserad, tidig och frekvent testning som en del av SDLC."
)
paragraph("Programmet omfattar:")
bullet_points([
    "Kravanalys och testdesign",
    "Testautomatisering",
    "Val av lämpliga testverktyg",
    "Kontinuerlig integration och testning",
    "Användning av TDD, BDD, ATDD",
    "Versionshantering i team",
])

subsection_title("Kandidatexamen i Medieteknik", "Blekinge Tekniska Högskola 2009–2012", first_col_width=0.5)
paragraph(
    "Programmet fokuserade på webbutveckling, användbarhet, användarcentrerad design och digital produktion. "
    "Det inkluderade både tekniska och designorienterade kurser och betonade projektbaserat lärande. "
    "Examensarbetet behandlade webbanvändbarhet i tillämpade miljöer."
)
paragraph("Kursinnehåll inkluderade:")
bullet_points([
    "Webbutveckling och skript (HTML, CSS, JavaScript, PHP, SQL)",
    "Java och objektorienterad programmering",
    "Digital medieproduktion och tillämpad webbteknik",
    "Visuell design och retorik",
])

main_story.append(Spacer(1, 6))

subsection_title("YH-examen – Visuell kommunikation och projektledning", "Mediability 2007–2009")
paragraph(
    "Program inom grafisk design, kommunikationsstrategi och projektbaserad produktion."
)
paragraph("Läroplanen inkluderade:")
bullet_points([
    "Grafisk design, fokus på kreativitet, målgrupp och användningskontext",
    "Projektledning för strukturerat teamarbete i kreativa miljöer",
    "Marknads- och trendanalys för att förutse utvecklingen i designbranschen",
    "Entreprenörskap i frilans- eller företagssammanhang",
    "Grafisk produktion från idé till färdig produkt",
    "Marknadskommunikation, utveckling av marknads- och affärsplaner"
])
paragraph("Programmet betonade anpassningsförmåga, samarbete och praktisk erfarenhet.")

# Right column content (skills/languages)

SKILL_COLOR = '#003366'  # blue used for section titles
right_story = []
right_story.append(Paragraph("Kompetenser", styles['SectionTitle']))
right_story.append(Paragraph(
    f"<font color='{SKILL_COLOR}'><b>Testautomatisering:</b></font> Pipelines, TDD, BDD, testfallsdesign, Selenium, Robot framework, <br/>"
    f"<font color='{SKILL_COLOR}'><b>Verktyg och system:</b></font><br/>SQL Server, MySQL, Git, Azure DevOps, Agentic AI<br/>"
    f"<font color='{SKILL_COLOR}'><b>Arbetsflöde och samarbete:</b></font> Agila metoder, internkommunikation, dokumentation<br/>"
    f"<font color='{SKILL_COLOR}'><b>Webb och gränssnittsutveckling:</b></font> HTML, CSS, JavaScript, PHP, Python, ASP.NET WebAPI, Java<br/>"
    f"<font color='{SKILL_COLOR}'><b>Design och innehållsproduktion:</b></font> Adobe Creative Suite, UX/UI, tryck- och webblayout",
    styles['NormalText']))
right_story.append(Spacer(1, 12))
right_story.append(Paragraph("Språk", styles['SectionTitle']))
right_story.append(Paragraph("Svenska (modersmål)<br/>Engelska (flytande)", styles['NormalText']))

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
