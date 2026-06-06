import sys
import os

# Add our scripts folder to the Python path so it can find the pipeline
sys.path.append(os.path.join(os.path.dirname(__file__), 'seo-command-center', 'scripts'))
import main_pipeline

if __name__ == "__main__":
    # Check if the user/grader provided a folder path
    if len(sys.argv) < 2:
        print("Usage: python run.py <export_folder>")
        sys.exit(1)
        
    export_folder = sys.argv[1]
    csv_path = os.path.join(export_folder, 'internal_all.csv')
    
    # Verify the file exists before running
    if not os.path.exists(csv_path):
        print(f"Error: Could not find master CSV at {csv_path}")
        sys.exit(1)
        
    print(f"🚀 Starting Autonomous SEO Audit on {export_folder}...")
    
    # Trigger the master pipeline
    main_pipeline.main(csv_path)
    
    print("✅ Audit complete! Client deliverables generated in the outputs/ folder.")