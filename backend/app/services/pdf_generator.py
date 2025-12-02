"""
PDF Report Generator using ReportLab
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.feedback import Feedback, SentimentCategory
from app.models.report import WeeklyReport, ActionItem
import os
import io
import logging

logger = logging.getLogger(__name__)


class PDFGenerator:
    """Generate PDF reports for weekly sentiment analysis"""
    
    def __init__(self, db: Session):
        self.db = db
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1976d2'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#424242'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        # Subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubheading',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#616161'),
            spaceAfter=8
        ))
        
        # Quote style
        self.styles.add(ParagraphStyle(
            name='Quote',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#757575'),
            leftIndent=20,
            rightIndent=20,
            fontStyle='italic',
            spaceAfter=10
        ))
    
    def generate_pdf(self, report: WeeklyReport, output_path: str) -> str:
        """Generate complete PDF report"""
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build story (content)
            story = []
            
            # Cover page
            story.extend(self._create_cover_page(report))
            story.append(PageBreak())
            
            # Executive summary
            story.extend(self._create_executive_summary(report))
            story.append(PageBreak())
            
            # Category analysis
            story.extend(self._create_category_analysis(report))
            story.append(PageBreak())
            
            # Action items
            story.extend(self._create_action_items(report))
            story.append(PageBreak())
            
            # Appendix
            story.extend(self._create_appendix(report))
            
            # Build PDF
            doc.build(story)
            
            return output_path
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            raise
    
    def _create_cover_page(self, report: WeeklyReport) -> List:
        """Create cover page"""
        elements = []
        
        # Title
        title = Paragraph("L1 Feedback Sentiment Analysis", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        # Week range
        week_start_str = report.week_start_date.strftime('%B %d, %Y')
        week_end_str = report.week_end_date.strftime('%B %d, %Y')
        week_range = Paragraph(
            f"Week: {week_start_str} - {week_end_str}",
            self.styles['Heading2']
        )
        elements.append(week_range)
        elements.append(Spacer(1, 0.3*inch))
        
        # Key metrics table
        metrics_data = [
            ['Metric', 'Value'],
            ['Overall Sentiment Score', f"{report.overall_sentiment_score:.1f}%"],
            ['Sentiment Change', f"{report.sentiment_change:+.1f}%" if report.sentiment_change else "N/A"],
            ['Engagement Heat Index', f"{report.heat_index:.1f}/100"],
            ['Total Feedback Count', str(report.total_feedback_count)],
            ['Positive', str(report.positive_count)],
            ['Neutral', str(report.neutral_count)],
            ['Negative', str(report.negative_count)],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976d2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        elements.append(metrics_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Generated date
        generated_date = Paragraph(
            f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['Normal']
        )
        elements.append(generated_date)
        
        return elements
    
    def _create_executive_summary(self, report: WeeklyReport) -> List:
        """Create executive summary section"""
        elements = []
        
        # Section title
        title = Paragraph("Executive Summary", self.styles['CustomHeading'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Week overview
        week_start_str = report.week_start_date.strftime('%b %d')
        week_end_str = report.week_end_date.strftime('%b %d, %Y')
        overview_text = f"""
        <b>Week Overview:</b><br/>
        Date Range: {week_start_str} - {week_end_str}<br/>
        Overall Sentiment Score: {report.overall_sentiment_score:.0f}%
        """
        if report.sentiment_change:
            change_str = f"+{report.sentiment_change:.1f}%" if report.sentiment_change > 0 else f"{report.sentiment_change:.1f}%"
            overview_text += f" ({change_str} from last week)<br/>"
        overview_text += f"Engagement Heat Index: {report.heat_index:.1f}/100"
        
        overview = Paragraph(overview_text, self.styles['Normal'])
        elements.append(overview)
        elements.append(Spacer(1, 0.3*inch))
        
        # Executive summary text
        if report.executive_summary:
            summary_para = Paragraph(report.executive_summary, self.styles['Normal'])
            elements.append(summary_para)
            elements.append(Spacer(1, 0.3*inch))
        
        # Get top strengths and concerns with quotes
        strengths_concerns = self._get_strengths_and_concerns_with_quotes(report)
        
        # Top Strengths
        if strengths_concerns['strengths']:
            strengths_title = Paragraph("<b>Top Strengths:</b>", self.styles['CustomSubheading'])
            elements.append(strengths_title)
            for i, strength in enumerate(strengths_concerns['strengths'][:3], 1):
                strength_text = f"{i}. {strength['category']}: {strength['description']}"
                strength_para = Paragraph(strength_text, self.styles['Normal'])
                elements.append(strength_para)
                if strength.get('quote'):
                    quote_para = Paragraph(f'"{strength["quote"]}"', self.styles['Quote'])
                    elements.append(quote_para)
                elements.append(Spacer(1, 0.1*inch))
            elements.append(Spacer(1, 0.2*inch))
        
        # Top Concerns
        if strengths_concerns['concerns']:
            concerns_title = Paragraph("<b>Top Concerns:</b>", self.styles['CustomSubheading'])
            elements.append(concerns_title)
            for i, concern in enumerate(strengths_concerns['concerns'][:3], 1):
                concern_text = f"{i}. {concern['category']}: {concern['description']}"
                concern_para = Paragraph(concern_text, self.styles['Normal'])
                elements.append(concern_para)
                if concern.get('quote'):
                    quote_para = Paragraph(f'"{concern["quote"]}"', self.styles['Quote'])
                    elements.append(quote_para)
                elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_category_analysis(self, report: WeeklyReport) -> List:
        """Create category-wise analysis section"""
        elements = []
        
        title = Paragraph("Category Analysis", self.styles['CustomHeading'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Get feedback for the week
        feedback_list = self.db.query(Feedback).filter(
            Feedback.week_start_date >= report.week_start_date,
            Feedback.week_start_date <= report.week_end_date
        ).all()
        
        # Group by category
        category_data = {}
        for feedback in feedback_list:
            for mapping in feedback.category_mappings:
                category = mapping.category.value.replace('_', ' ').title()
                if category not in category_data:
                    category_data[category] = {
                        'positive': 0,
                        'neutral': 0,
                        'negative': 0,
                        'total': 0
                    }
                
                if feedback.sentiment_analysis:
                    sentiment = feedback.sentiment_analysis.sentiment_category.value
                    category_data[category][sentiment] += 1
                    category_data[category]['total'] += 1
        
        # Create table for each category
        for category, data in category_data.items():
            if data['total'] > 0:
                cat_title = Paragraph(f"<b>{category}</b>", self.styles['CustomSubheading'])
                elements.append(cat_title)
                
                cat_table_data = [
                    ['Sentiment', 'Count', 'Percentage'],
                    ['Positive', str(data['positive']), f"{(data['positive']/data['total']*100):.1f}%"],
                    ['Neutral', str(data['neutral']), f"{(data['neutral']/data['total']*100):.1f}%"],
                    ['Negative', str(data['negative']), f"{(data['negative']/data['total']*100):.1f}%"],
                    ['Total', str(data['total']), '100%'],
                ]
                
                cat_table = Table(cat_table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
                cat_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#616161')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(cat_table)
                elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_action_items(self, report: WeeklyReport) -> List:
        """Create action items section"""
        elements = []
        
        title = Paragraph("Action Items & Recommendations", self.styles['CustomHeading'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Get action items
        action_items = self.db.query(ActionItem).filter(
            ActionItem.report_id == report.id
        ).order_by(ActionItem.priority.desc()).all()
        
        if not action_items:
            no_items = Paragraph("No action items generated for this week.", self.styles['Normal'])
            elements.append(no_items)
            return elements
        
        # Group by priority
        priority_order = ['urgent', 'high', 'medium', 'low']
        for priority in priority_order:
            priority_items = [item for item in action_items if item.priority.value == priority]
            if priority_items:
                priority_title = Paragraph(
                    f"<b>{priority.upper()} Priority</b>",
                    self.styles['CustomSubheading']
                )
                elements.append(priority_title)
                
                for item in priority_items:
                    item_text = f"""
                    <b>{item.title}</b><br/>
                    Category: {item.category or 'General'}<br/>
                    {item.description}
                    """
                    if item.assigned_to:
                        item_text += f"<br/>Assigned to: {item.assigned_to}"
                    if item.confidence_score:
                        item_text += f"<br/>Confidence: {item.confidence_score*100:.0f}%"
                    
                    item_para = Paragraph(item_text, self.styles['Normal'])
                    elements.append(item_para)
                    elements.append(Spacer(1, 0.15*inch))
                
                elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_appendix(self, report: WeeklyReport) -> List:
        """Create appendix section"""
        elements = []
        
        title = Paragraph("Appendix", self.styles['CustomHeading'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Methodology
        methodology = Paragraph(
            """
            <b>Methodology:</b><br/>
            This report uses advanced NLP and machine learning models to analyze trainee feedback.
            Sentiment analysis is performed using RoBERTa-based transformer models, and category
            mapping uses keyword extraction and context relevance scoring.
            """,
            self.styles['Normal']
        )
        elements.append(methodology)
        elements.append(Spacer(1, 0.2*inch))
        
        # Data sources
        data_sources = Paragraph(
            f"""
            <b>Data Sources:</b><br/>
            Feedback collected from L1 trainees via weekly surveys.<br/>
            Report period: {report.week_start_date.strftime('%B %d, %Y')} - {report.week_end_date.strftime('%B %d, %Y')}<br/>
            Total feedback entries analyzed: {report.total_feedback_count}
            """,
            self.styles['Normal']
        )
        elements.append(data_sources)
        
        return elements
    
    def _get_strengths_and_concerns_with_quotes(self, report: WeeklyReport) -> Dict:
        """Get top strengths and concerns with supporting quotes"""
        feedback_list = self.db.query(Feedback).filter(
            Feedback.week_start_date >= report.week_start_date,
            Feedback.week_start_date <= report.week_end_date
        ).all()
        
        # Analyze positive feedback for strengths
        positive_feedback = [f for f in feedback_list 
                           if f.sentiment_analysis and 
                           f.sentiment_analysis.sentiment_category == SentimentCategory.POSITIVE]
        
        # Analyze negative feedback for concerns
        negative_feedback = [f for f in feedback_list 
                           if f.sentiment_analysis and 
                           f.sentiment_analysis.sentiment_category == SentimentCategory.NEGATIVE]
        
        # Count category mentions in positive feedback
        strength_categories = {}
        for feedback in positive_feedback:
            for mapping in feedback.category_mappings:
                category = mapping.category.value.replace('_', ' ').title()
                if category not in strength_categories:
                    strength_categories[category] = {
                        'count': 0,
                        'quotes': []
                    }
                strength_categories[category]['count'] += 1
                if len(strength_categories[category]['quotes']) < 2:
                    # Extract a meaningful quote (first 150 chars)
                    quote = feedback.open_text[:150] + "..." if len(feedback.open_text) > 150 else feedback.open_text
                    strength_categories[category]['quotes'].append(quote)
        
        # Count category mentions in negative feedback
        concern_categories = {}
        for feedback in negative_feedback:
            for mapping in feedback.category_mappings:
                category = mapping.category.value.replace('_', ' ').title()
                if category not in concern_categories:
                    concern_categories[category] = {
                        'count': 0,
                        'quotes': []
                    }
                concern_categories[category]['count'] += 1
                if len(concern_categories[category]['quotes']) < 2:
                    quote = feedback.open_text[:150] + "..." if len(feedback.open_text) > 150 else feedback.open_text
                    concern_categories[category]['quotes'].append(quote)
        
        # Get top 3 strengths
        top_strengths = sorted(
            strength_categories.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:3]
        strengths_list = [
            {
                'category': cat,
                'description': f"{cat} received {data['count']} positive mentions",
                'quote': data['quotes'][0] if data['quotes'] else None
            }
            for cat, data in top_strengths
        ]
        
        # Get top 3 concerns
        top_concerns = sorted(
            concern_categories.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:3]
        concerns_list = [
            {
                'category': cat,
                'description': f"{cat} received {data['count']} negative mentions",
                'quote': data['quotes'][0] if data['quotes'] else None
            }
            for cat, data in top_concerns
        ]
        
        return {
            'strengths': strengths_list,
            'concerns': concerns_list
        }



