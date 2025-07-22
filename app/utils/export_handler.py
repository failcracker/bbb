import csv
import io
from datetime import date, datetime
from typing import Optional, List
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from app.services.absensi_service import AbsensiService
from app.config.firebase import firestore_client

def export_absensi_pdf(tanggal: Optional[date] = None) -> bytes:
    """
    Export attendance data to PDF format
    """
    # Get attendance data
    absensi_list = AbsensiService.list_absensi(tanggal)
    
    # Create PDF buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Add title
    title_text = f"Laporan Absensi Karyawan"
    if tanggal:
        title_text += f" - {tanggal.strftime('%d/%m/%Y')}"
    else:
        title_text += " - Semua Tanggal"
    
    title = Paragraph(title_text, title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))
    
    # Prepare table data
    table_data = []
    
    # Header
    headers = [
        'No', 'Nama Karyawan', 'Kode', 'Tanggal', 'Jam Datang', 
        'Jam Pulang', 'Status', 'Lokasi', 'Terlambat', 'Face Valid'
    ]
    table_data.append(headers)
    
    # Get user data for names
    user_cache = {}
    
    # Add attendance data
    for i, absensi in enumerate(absensi_list, 1):
        # Get user data if not cached
        if absensi.karyawan_id not in user_cache:
            user_doc = firestore_client.collection("users").document(absensi.karyawan_id).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                user_cache[absensi.karyawan_id] = user_data
            else:
                user_cache[absensi.karyawan_id] = {"nama": "Unknown", "kode_karyawan": "Unknown"}
        
        user_data = user_cache[absensi.karyawan_id]
        
        # Format data
        tanggal_str = absensi.tanggal if isinstance(absensi.tanggal, str) else absensi.tanggal.strftime('%d/%m/%Y')
        jam_datang = absensi.jam_datang or "-"
        jam_pulang = absensi.jam_pulang or "-"
        terlambat = "Ya" if absensi.terlambat else "Tidak"
        face_valid = "Ya" if absensi.face_valid else "Tidak"
        
        row = [
            str(i),
            user_data.get("nama", "Unknown"),
            user_data.get("kode_karyawan", "Unknown"),
            tanggal_str,
            jam_datang,
            jam_pulang,
            absensi.status_kehadiran,
            absensi.status_lokasi,
            terlambat,
            face_valid
        ]
        table_data.append(row)
    
    # Create table
    if len(table_data) > 1:  # If there's data besides header
        table = Table(table_data, colWidths=[0.3*inch, 1.2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 
                                            0.8*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch])
        
        # Style the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Nama Karyawan left aligned
        ])
        table.setStyle(style)
        elements.append(table)
    else:
        # No data message
        no_data = Paragraph("Tidak ada data absensi untuk tanggal yang dipilih", styles['Normal'])
        elements.append(no_data)
    
    # Add footer
    elements.append(Spacer(1, 20))
    footer_text = f"Laporan dibuat pada: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    footer = Paragraph(footer_text, styles['Normal'])
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def export_absensi_csv(tanggal: Optional[date] = None) -> bytes:
    """
    Export attendance data to CSV format
    """
    # Get attendance data
    absensi_list = AbsensiService.list_absensi(tanggal)
    
    # Create CSV buffer
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    
    # Write header
    headers = [
        'No', 'Nama Karyawan', 'Kode Karyawan', 'Tanggal', 'Jam Datang', 
        'Jam Pulang', 'Status Kehadiran', 'Status Lokasi', 'Terlambat', 'Face Valid'
    ]
    writer.writerow(headers)
    
    # Get user data for names
    user_cache = {}
    
    # Write attendance data
    for i, absensi in enumerate(absensi_list, 1):
        # Get user data if not cached
        if absensi.karyawan_id not in user_cache:
            user_doc = firestore_client.collection("users").document(absensi.karyawan_id).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                user_cache[absensi.karyawan_id] = user_data
            else:
                user_cache[absensi.karyawan_id] = {"nama": "Unknown", "kode_karyawan": "Unknown"}
        
        user_data = user_cache[absensi.karyawan_id]
        
        # Format data
        tanggal_str = absensi.tanggal if isinstance(absensi.tanggal, str) else absensi.tanggal.strftime('%d/%m/%Y')
        jam_datang = absensi.jam_datang or ""
        jam_pulang = absensi.jam_pulang or ""
        terlambat = "Ya" if absensi.terlambat else "Tidak"
        face_valid = "Ya" if absensi.face_valid else "Tidak"
        
        row = [
            i,
            user_data.get("nama", "Unknown"),
            user_data.get("kode_karyawan", "Unknown"),
            tanggal_str,
            jam_datang,
            jam_pulang,
            absensi.status_kehadiran,
            absensi.status_lokasi,
            terlambat,
            face_valid
        ]
        writer.writerow(row)
    
    # Convert to bytes
    csv_content = buffer.getvalue()
    buffer.close()
    return csv_content.encode('utf-8-sig')  # UTF-8 with BOM for Excel compatibility