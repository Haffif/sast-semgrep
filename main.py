import os
import json
import subprocess
import argparse
from fpdf import FPDF

def logo():
    logo = r"""
  _________                                                         
 /   _____/ ____   _____    ___________   ____ ______   ___________ 
 \_____  \_/ __ \ /     \  / ___\_  __ \_/ __ \\____ \_/ __ \_  __ \
 /        \  ___/|  Y Y  \/ /_/  >  | \/\  ___/|  |_> >  ___/|  | \/
/_______  /\___  >__|_|  /\___  /|__|    \___  >   __/ \___  >__|   
        \/     \/      \//_____/             \/|__|        \/           
                                                   
    """
    print(logo)

def run_semgrep(directory):
    print(f"Target directory: {directory}...")
    
    try:
        result = subprocess.run(['semgrep', '--config', 'auto', directory, '--json'], check=True, capture_output=True, text=True)
        print("Scan Completed")
        return json.loads(result.stdout) 
    except Exception as e:
        print(f"Error running Semgrep: {e}")
        return None

def create_report(scan_results, report_file):
    print("Creating Report, Please wait...")
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "SAST Vulnerability Report", ln=True, align='C')

    pdf.set_font("Arial", 'B', 12)
    pdf.ln(10)
    pdf.cell(200, 10, "Detected Vulnerabilities", ln=True)

    pdf.set_font("Arial", size=10)

    if not scan_results.get('results'):
        pdf.ln(5)
        pdf.cell(200, 10, "No vulnerabilities found", ln=True)
    else:
        for result in scan_results['results']:
            pdf.ln(5)
            pdf.multi_cell(0, 10, f"Rule ID: {result.get('check_id', 'N/A')}")
            pdf.multi_cell(0, 10, f"Severity: {result.get('extra', {}).get('severity', 'Unknown')}")
            pdf.multi_cell(0, 10, f"Message: {result.get('extra', {}).get('message', 'No message available')}")
            pdf.multi_cell(0, 10, f"File: {result.get('path', 'Unknown file')} (Line {result.get('start', {}).get('line', 'Unknown')})")
            pdf.ln(5)

    pdf.output(report_file)
    print(f"Report Filename: {report_file}")

def main():
    logo()
    parser = argparse.ArgumentParser(description="Vulnerability Scanner with Semgrep (Report included)")
    parser.add_argument('directory', type=str, help='Target directory containing source codes')
    parser.add_argument('report_file', type=str, help='The output PDF report file name')

    if len(os.sys.argv) == 1:
        parser.print_help()
        exit(1)

    args = parser.parse_args()

    scan_results = run_semgrep(args.directory)
    if scan_results is not None:
        create_report(scan_results, args.report_file)
    
    print("Task Completed")

if __name__ == "__main__":
    main()
