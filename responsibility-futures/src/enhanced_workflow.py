#!/usr/bin/env python3
"""
Enhanced Responsibility Futures Workflow
Integrates Cortext.io processing with HTML report and PNG generation

This script provides a complete workflow from Cortext.io JSON input
to enriched HTML reports and visualizations.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class ResponsibilityWorkflow:
    """
    Complete workflow manager for Responsibility Futures analysis
    """
    
    def __init__(self, cortext_reports_dir: str = None):
        self.src_dir = Path(__file__).parent
        self.project_dir = self.src_dir.parent
        
        # Default to cortext.io reports directory if not specified
        if cortext_reports_dir:
            self.reports_dir = Path(cortext_reports_dir)
        else:
            self.reports_dir = Path("../../../cortext.io/reports").resolve()
        
        self.output_dir = self.project_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"📁 Source directory: {self.src_dir}")
        print(f"📁 Reports directory: {self.reports_dir}")
        print(f"📁 Output directory: {self.output_dir}")
    
    def find_latest_cortext_report(self) -> Optional[Path]:
        """Find the most recent Cortext.io extraction JSON file"""
        if not self.reports_dir.exists():
            print(f"❌ Reports directory not found: {self.reports_dir}")
            return None
        
        # Look for extraction JSON files
        extraction_files = list(self.reports_dir.glob("extraction_*.json"))
        
        # Filter out responsibility analysis files (we want the original extraction)
        extraction_files = [f for f in extraction_files if "responsibility_analysis" not in f.name]
        
        if not extraction_files:
            print(f"❌ No extraction JSON files found in {self.reports_dir}")
            return None
        
        # Sort by modification time and get the latest
        latest_file = max(extraction_files, key=lambda f: f.stat().st_mtime)
        print(f"📄 Found latest Cortext.io report: {latest_file.name}")
        
        return latest_file
    
    def run_responsibility_analysis(self, input_file: Path) -> Optional[Path]:
        """
        Run the responsibility analysis on the Cortext.io JSON file
        Returns the path to the generated responsibility analysis JSON
        """
        print("🔬 Running responsibility analysis...")
        
        cortext_integration_script = self.src_dir / "cortext_integration.py"
        
        try:
            # Run the cortext integration script
            result = subprocess.run([
                sys.executable, str(cortext_integration_script), str(input_file)
            ], capture_output=True, text=True, cwd=self.src_dir)
            
            if result.returncode != 0:
                print(f"❌ Error running responsibility analysis:")
                print(result.stderr)
                return None
            
            print("✅ Responsibility analysis completed")
            print(result.stdout)
            
            # Find the generated responsibility analysis file
            analysis_file = input_file.with_name(
                input_file.stem + "_responsibility_analysis.json"
            )
            
            if analysis_file.exists():
                return analysis_file
            else:
                print(f"❌ Expected analysis file not found: {analysis_file}")
                return None
                
        except Exception as e:
            print(f"❌ Error running responsibility analysis: {e}")
            return None
    
    def generate_reports(self, analysis_file: Path) -> Optional[Dict[str, str]]:
        """
        Generate HTML report and PNG visualizations
        Returns dictionary of generated file paths
        """
        print("🎨 Generating enhanced reports and visualizations...")
        
        report_generator_script = self.src_dir / "report_generator.py"
        
        try:
            # Run the report generator script
            result = subprocess.run([
                sys.executable, str(report_generator_script), str(analysis_file)
            ], capture_output=True, text=True, cwd=self.src_dir)
            
            if result.returncode != 0:
                print(f"❌ Error generating reports:")
                print(result.stderr)
                return None
            
            print("✅ Report generation completed")
            print(result.stdout)
            
            # Parse the output to find generated files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_dir = analysis_file.parent
            
            generated_files = {
                'html_report': report_dir / f"responsibility_report_{timestamp}.html",
                'matrix_plot': report_dir / f"responsibility_matrix_{timestamp}.png",
                'vector_plot': report_dir / f"vector_analysis_{timestamp}.png",
                'stats_plot': report_dir / f"statistical_summary_{timestamp}.png"
            }
            
            # Find the actual generated files (timestamps might be slightly different)
            actual_files = {}
            for file_type, expected_path in generated_files.items():
                # Look for files with similar patterns
                pattern = expected_path.name.split('_')[:-1]  # Remove timestamp part
                pattern = '_'.join(pattern) + '_*.html' if 'html' in expected_path.suffix else '_'.join(pattern) + '_*.png'
                
                matching_files = list(report_dir.glob(pattern))
                if matching_files:
                    # Get the most recent one
                    actual_files[file_type] = max(matching_files, key=lambda f: f.stat().st_mtime)
            
            return actual_files
            
        except Exception as e:
            print(f"❌ Error generating reports: {e}")
            return None
    
    def copy_to_output(self, generated_files: Dict[str, Path]) -> Dict[str, Path]:
        """
        Copy generated files to the output directory with organized naming
        """
        print("📋 Organizing output files...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_files = {}
        
        for file_type, source_path in generated_files.items():
            if source_path and source_path.exists():
                # Create organized filename
                if file_type == 'html_report':
                    output_name = f"responsibility_futures_report_{timestamp}.html"
                else:
                    output_name = f"responsibility_futures_{file_type}_{timestamp}.png"
                
                output_path = self.output_dir / output_name
                
                # Copy file
                import shutil
                shutil.copy2(source_path, output_path)
                output_files[file_type] = output_path
                
                print(f"   📄 {file_type}: {output_name}")
        
        return output_files
    
    def run_complete_workflow(self, input_file: Path = None) -> Dict[str, Path]:
        """
        Run the complete workflow from Cortext.io JSON to final reports
        """
        print("🚀 Starting Enhanced Responsibility Futures Workflow")
        print("=" * 60)
        
        # Step 1: Find input file if not provided
        if input_file is None:
            input_file = self.find_latest_cortext_report()
            if input_file is None:
                return {}
        
        print(f"📥 Input file: {input_file}")
        
        # Step 2: Run responsibility analysis
        analysis_file = self.run_responsibility_analysis(input_file)
        if analysis_file is None:
            return {}
        
        print(f"📊 Analysis file: {analysis_file}")
        
        # Step 3: Generate reports and visualizations
        generated_files = self.generate_reports(analysis_file)
        if generated_files is None:
            return {}
        
        # Step 4: Copy to organized output directory
        output_files = self.copy_to_output(generated_files)
        
        print("\n🎉 Workflow completed successfully!")
        print("📋 Generated files:")
        for file_type, file_path in output_files.items():
            print(f"   • {file_type}: {file_path}")
        
        # Print quick access info
        if 'html_report' in output_files:
            html_path = output_files['html_report']
            print(f"\n🌐 View the complete report:")
            print(f"   file://{html_path.absolute()}")
        
        return output_files
    
    def list_available_reports(self) -> List[Path]:
        """List all available Cortext.io reports"""
        if not self.reports_dir.exists():
            return []
        
        extraction_files = list(self.reports_dir.glob("extraction_*.json"))
        extraction_files = [f for f in extraction_files if "responsibility_analysis" not in f.name]
        
        return sorted(extraction_files, key=lambda f: f.stat().st_mtime, reverse=True)

def main():
    """Main execution function with command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Enhanced Responsibility Futures Workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process the latest Cortext.io report
  python enhanced_workflow.py
  
  # Process a specific report file
  python enhanced_workflow.py --input /path/to/extraction_file.json
  
  # Use a different reports directory
  python enhanced_workflow.py --reports-dir /path/to/reports
  
  # List available reports
  python enhanced_workflow.py --list
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        help='Specific Cortext.io JSON file to process'
    )
    
    parser.add_argument(
        '--reports-dir', '-r',
        type=str,
        help='Directory containing Cortext.io reports (default: ../../../cortext.io/reports)'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List available Cortext.io reports and exit'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize workflow
        workflow = ResponsibilityWorkflow(args.reports_dir)
        
        # List reports if requested
        if args.list:
            reports = workflow.list_available_reports()
            if reports:
                print("📋 Available Cortext.io reports:")
                for i, report in enumerate(reports, 1):
                    mtime = datetime.fromtimestamp(report.stat().st_mtime)
                    print(f"   {i:2d}. {report.name} ({mtime.strftime('%Y-%m-%d %H:%M')})")
            else:
                print("❌ No Cortext.io reports found")
            return
        
        # Determine input file
        input_file = None
        if args.input:
            input_file = Path(args.input)
            if not input_file.exists():
                print(f"❌ Input file not found: {input_file}")
                sys.exit(1)
        
        # Run the complete workflow
        output_files = workflow.run_complete_workflow(input_file)
        
        if output_files:
            print("\n✅ Workflow completed successfully!")
        else:
            print("\n❌ Workflow failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Workflow interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()