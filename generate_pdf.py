"""
PDF Generator for Intergalactic Riksbanken Chip Authenticator Documentation
Authors: Group 8 - Suneela, Sara, and Abhishek
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from pathlib import Path
import re
import os


def parse_markdown_to_pdf_elements(md_content: str, styles, base_path: Path = None):
    """
    Parse markdown content and convert to ReportLab elements.
    
    Args:
        md_content: Markdown content string
        styles: ReportLab styles
        base_path: Base path for resolving relative image paths
        
    Returns:
        List of ReportLab flowables
    """
    elements = []
    lines = md_content.split('\n')
    
    code_block = []
    in_code_block = False
    table_rows = []
    in_table = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Handle code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # End code block
                code_text = '\n'.join(code_block)
                elements.append(Preformatted(code_text, styles['CustomCode']))
                elements.append(Spacer(1, 0.2*inch))
                code_block = []
                in_code_block = False
            else:
                # Start code block
                in_code_block = True
            i += 1
            continue
            
        if in_code_block:
            code_block.append(line)
            i += 1
            continue
        
        # Handle tables
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_rows = []
            
            # Parse table row
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            table_rows.append(cells)
            i += 1
            
            # Check if next line is separator or not a table row
            if i >= len(lines) or '|' not in lines[i] or not lines[i].strip().startswith('|'):
                # End of table
                if len(table_rows) > 0:
                    # Remove separator row if present
                    if len(table_rows) > 1 and all(c.strip().replace('-', '').replace(':', '') == '' for c in table_rows[1]):
                        table_rows.pop(1)
                    
                    table = Table(table_rows)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
                    ]))
                    elements.append(table)
                    elements.append(Spacer(1, 0.3*inch))
                in_table = False
            continue
        
        # Handle headers
        if line.startswith('# '):
            elements.append(PageBreak())
            elements.append(Paragraph(line[2:].strip(), styles['Heading1']))
            elements.append(Spacer(1, 0.3*inch))
        elif line.startswith('## '):
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph(line[3:].strip(), styles['Heading2']))
            elements.append(Spacer(1, 0.2*inch))
        elif line.startswith('### '):
            elements.append(Paragraph(line[4:].strip(), styles['Heading3']))
            elements.append(Spacer(1, 0.15*inch))
        elif line.startswith('#### '):
            elements.append(Paragraph(line[5:].strip(), styles['Heading4']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Handle images
        elif line.strip().startswith('!['):
            match = re.match(r'!\[(.*?)\]\((.*?)\)', line.strip())
            if match and base_path:
                alt_text, img_path = match.groups()
                # Resolve relative path
                full_img_path = base_path / img_path
                if full_img_path.exists():
                    try:
                        img = Image(str(full_img_path))
                        # Scale image to fit page width (max 5 inches)
                        img._restrictSize(5*inch, 4*inch)
                        elements.append(Spacer(1, 0.1*inch))
                        elements.append(img)
                        if alt_text:
                            elements.append(Paragraph(f"<i>{alt_text}</i>", styles['Normal']))
                        elements.append(Spacer(1, 0.2*inch))
                    except Exception as e:
                        # If image can't be loaded, show alt text
                        elements.append(Paragraph(f"[Image: {alt_text}]", styles['Normal']))
                else:
                    elements.append(Paragraph(f"[Image not found: {img_path}]", styles['Normal']))
        
        # Handle horizontal rules
        elif line.strip() == '---' or line.strip() == '***':
            elements.append(Spacer(1, 0.2*inch))
        
        # Handle bullet lists
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            text = line.strip()[2:]
            # Clean markdown formatting
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
            text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)
            elements.append(Paragraph(f"• {text}", styles['BodyText']))
        
        # Handle numbered lists
        elif re.match(r'^\d+\.\s', line.strip()):
            text = re.sub(r'^\d+\.\s', '', line.strip())
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
            text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)
            elements.append(Paragraph(text, styles['BodyText']))
        
        # Handle normal paragraphs
        elif line.strip():
            text = line.strip()
            # Clean markdown formatting
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
            text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)
            text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<link href="\2">\1</link>', text)
            elements.append(Paragraph(text, styles['BodyText']))
            elements.append(Spacer(1, 0.1*inch))
        else:
            # Empty line
            elements.append(Spacer(1, 0.1*inch))
        
        i += 1
    
    return elements


def create_pdf_from_markdown(md_file: str, output_pdf: str, title: str = None):
    """
    Convert a Markdown file to a professionally formatted PDF using ReportLab.
    
    Args:
        md_file: Path to the markdown file
        output_pdf: Path for the output PDF file
        title: Optional title for the document
    """
    print(f"📄 Reading markdown file: {md_file}")
    
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    print("📝 Generating PDF...")
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='CustomCode',
        parent=styles['Code'],
        fontSize=8,
        leftIndent=20,
        fontName='Courier',
        backColor=colors.HexColor('#f5f5f5'),
        borderColor=colors.HexColor('#dddddd'),
        borderWidth=1,
        borderPadding=5
    ))
    
    # Modify existing styles
    styles['Heading1'].textColor = colors.HexColor('#2c3e50')
    styles['Heading1'].fontSize = 18
    styles['Heading1'].spaceAfter = 12
    
    styles['Heading2'].textColor = colors.HexColor('#34495e')
    styles['Heading2'].fontSize = 14
    styles['Heading2'].spaceAfter = 10
    
    styles['Heading3'].textColor = colors.HexColor('#546e7a')
    styles['Heading3'].fontSize = 12
    
    styles['Heading4'].textColor = colors.HexColor('#607d8b')
    styles['Heading4'].fontSize = 11
    
    styles['BodyText'].fontSize = 10
    styles['BodyText'].leading = 14
    styles['BodyText'].alignment = TA_JUSTIFY
    
    # Build document
    story = []
    
    # Add title page if title provided
    if title:
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph(title, styles['CustomTitle']))
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph('Group 8', styles['Heading2']))
        story.append(Paragraph('Suneela, Sara, and Abhishek', styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph('December 14, 2025', styles['Normal']))
        story.append(PageBreak())
    
    # Parse and add markdown content
    base_path = Path(md_file).parent
    story.extend(parse_markdown_to_pdf_elements(md_content, styles, base_path))
    
    # Build PDF
    doc.build(story)
    
    print(f"✅ PDF created successfully: {output_pdf}")
    return output_pdf


def main():
    """Generate PDFs for all major documentation files."""
    
    base_dir = Path(__file__).parent
    
    # Documents to convert
    documents = [
        {
            'input': base_dir / 'DESIGN_DOCUMENT.md',
            'output': base_dir / 'Intergalactic_Riksbanken_Chip_Authenticator_Design_Document.pdf',
            'title': 'Intergalactic Riksbanken Chip Authenticator - Design Document'
        },
        {
            'input': base_dir / 'PROJECT_SUMMARY.md',
            'output': base_dir / 'Intergalactic_Riksbanken_Chip_Authenticator_Project_Summary.pdf',
            'title': 'Intergalactic Riksbanken Chip Authenticator - Project Summary'
        },
        {
            'input': base_dir / 'README.md',
            'output': base_dir / 'Intergalactic_Riksbanken_Chip_Authenticator_README.pdf',
            'title': 'Intergalactic Riksbanken Chip Authenticator - README'
        },
        {
            'input': base_dir / 'docs' / 'SCREENSHOTS.md',
            'output': base_dir / 'Intergalactic_Riksbanken_Chip_Authenticator_Screenshots.pdf',
            'title': 'Intergalactic Riksbanken Chip Authenticator - Screenshots'
        }
    ]
    
    print("🎨 Intergalactic Riksbanken Chip Authenticator - PDF Generator")
    print("=" * 70)
    print("Authors: Group 8 - Suneela, Sara, and Abhishek")
    print("=" * 70)
    print()
    
    generated = []
    
    for doc in documents:
        if doc['input'].exists():
            print(f"\n📚 Processing: {doc['input'].name}")
            print("-" * 70)
            try:
                create_pdf_from_markdown(
                    str(doc['input']),
                    str(doc['output']),
                    doc['title']
                )
                generated.append(doc['output'].name)
            except Exception as e:
                print(f"❌ Error generating {doc['output'].name}: {e}")
        else:
            print(f"⚠️  Skipping {doc['input'].name} - file not found")
    
    print("\n" + "=" * 70)
    print(f"✅ Successfully generated {len(generated)} PDF(s):")
    for pdf in generated:
        print(f"   📄 {pdf}")
    print("=" * 70)


if __name__ == '__main__':
    main()
