"""
PDF Generator Service for CBT System
Provides utilities for generating professional PDF reports with school logo
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from django.conf import settings
import os
from datetime import datetime


class PDFGenerator:
    """Base class for generating PDF reports with consistent styling"""
    
    # Color constants
    PRIMARY_COLOR = colors.HexColor('#0066CC')
    SUCCESS_COLOR = colors.HexColor('#28A745')
    WARNING_COLOR = colors.HexColor('#FFC107')
    DANGER_COLOR = colors.HexColor('#DC3545')
    GRAY_COLOR = colors.HexColor('#6C757D')
    LIGHT_GRAY = colors.HexColor('#F8F9FA')
    
    def __init__(self, buffer, title="Laporan"):
        """
        Initialize PDF generator
        Args:
            buffer: BytesIO buffer for PDF output
            title: Document title
        """
        self.buffer = buffer
        self.title = title
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Setup document with margins
        self.doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
            title=title
        )
        
        self.elements = []
        self.logo_path = os.path.join(settings.BASE_DIR, 'static', 'logo', 'logo_sman1.png')
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=self.PRIMARY_COLOR,
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.GRAY_COLOR,
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Info style
        self.styles.add(ParagraphStyle(
            name='InfoText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            fontName='Helvetica'
        ))
    
    def add_header(self, school_name="SMAN 1 KRAGILAN", school_address="Banten", report_title="LAPORAN"):
        """
        Add header with logo and school information
        Args:
            school_name: Name of the school
            school_address: School address
            report_title: Title of the report
        """
        # Add logo if exists
        if os.path.exists(self.logo_path):
            logo = Image(self.logo_path, width=2*cm, height=2*cm)
            logo.hAlign = 'CENTER'
            self.elements.append(logo)
            self.elements.append(Spacer(1, 0.3*cm))
        
        # School name
        school_para = Paragraph(f"<b>{school_name}</b>", self.styles['CustomTitle'])
        self.elements.append(school_para)
        
        # School address
        address_para = Paragraph(school_address, self.styles['CustomSubtitle'])
        self.elements.append(address_para)
        
        # Separator line
        self.elements.append(Spacer(1, 0.5*cm))
        line_data = [['_' * 100]]
        line_table = Table(line_data, colWidths=[self.width - 4*cm])
        line_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), self.GRAY_COLOR),
            ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        self.elements.append(line_table)
        self.elements.append(Spacer(1, 0.5*cm))
        
        # Report title
        title_para = Paragraph(f"<b>{report_title}</b>", self.styles['CustomTitle'])
        self.elements.append(title_para)
        self.elements.append(Spacer(1, 0.5*cm))
    
    def add_info_section(self, info_dict):
        """
        Add information section with key-value pairs
        Args:
            info_dict: Dictionary of information {key: value}
        """
        for key, value in info_dict.items():
            info_para = Paragraph(f"<b>{key}:</b> {value}", self.styles['InfoText'])
            self.elements.append(info_para)
        
        self.elements.append(Spacer(1, 0.5*cm))
    
    def add_table(self, data, col_widths=None, header_color=None, alternating_rows=True):
        """
        Add a styled table to the document
        Args:
            data: 2D list of table data (first row is header)
            col_widths: List of column widths (optional)
            header_color: Color for header row (default: PRIMARY_COLOR)
            alternating_rows: Whether to use alternating row colors
        """
        if not data:
            return
        
        if header_color is None:
            header_color = self.PRIMARY_COLOR
        
        # Create table
        table = Table(data, colWidths=col_widths, repeatRows=1)
        
        # Base table style
        table_style = [
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), header_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows styling
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, self.GRAY_COLOR),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
        
        # Alternating row colors
        if alternating_rows and len(data) > 1:
            for i in range(1, len(data)):
                if i % 2 == 0:
                    table_style.append(('BACKGROUND', (0, i), (-1, i), self.LIGHT_GRAY))
        
        table.setStyle(TableStyle(table_style))
        self.elements.append(table)
        self.elements.append(Spacer(1, 0.5*cm))
    
    def add_footer(self):
        """Add footer with timestamp in a more professional format"""
        timestamp = datetime.now().strftime('%d %B %Y, %H:%M:%S')
        
        # Add separator line before footer
        self.elements.append(Spacer(1, 0.8*cm))
        line_data = [['─' * 120]]
        line_table = Table(line_data, colWidths=[self.width - 4*cm])
        line_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), self.GRAY_COLOR),
            ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 6),
        ]))
        self.elements.append(line_table)
        
        # Footer text
        self.elements.append(Spacer(1, 0.3*cm))
        footer_style = ParagraphStyle(
            name='FooterStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=self.GRAY_COLOR,
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        footer_text = f"Dokumen ini dicetak pada {timestamp}"
        footer_para = Paragraph(footer_text, footer_style)
        self.elements.append(footer_para)
    
    def add_statistics(self, stats_dict):
        """
        Add statistics section
        Args:
            stats_dict: Dictionary of statistics {label: value}
        """
        self.elements.append(Spacer(1, 0.5*cm))
        stats_para = Paragraph("<b>STATISTIK</b>", self.styles['CustomTitle'])
        self.elements.append(stats_para)
        self.elements.append(Spacer(1, 0.3*cm))
        
        for label, value in stats_dict.items():
            stat_para = Paragraph(f"<b>{label}:</b> {value}", self.styles['InfoText'])
            self.elements.append(stat_para)
    
    def build(self):
        """Build the PDF document"""
        self.doc.build(self.elements)
        return self.buffer
