#!/usr/bin/env python3
import subprocess
import os
import sys
import time

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{'=' * 50}")
    print(f"STEP: {description}")
    print(f"{'=' * 50}")
    print(f"Running command: {command}")
    
    try:
        # Run the command and capture output
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Stream output in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                sys.stdout.flush()
        
        # Get the return code
        return_code = process.poll()
        
        # Check if command was successful
        if return_code != 0:
            error_output = process.stderr.read()
            print(f"Error executing command. Return code: {return_code}")
            print(f"Error details: {error_output}")
            return False
            
        return True
        
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return False

def main():
    start_time = time.time()
    
    print("Starting data processing pipeline...")
    
    # Step 1: Run node command to fetch JSON data
    node_cmd = "node xshin.js all all"
    node_success = run_command(node_cmd, "Fetching validator data with Node.js")
    
    if not node_success:
        print("Failed to fetch data. Exiting pipeline.")
        return 1
    
    # Step 2: Run Python script to create Excel file
    python_cmd = "python3 rankings.py"
    python_success = run_command(python_cmd, "Creating Excel rankings file")
    
    if not python_success:
        print("Failed to create Excel rankings. Exiting pipeline.")
        return 1
    
    # Calculate total runtime
    total_time = time.time() - start_time
    minutes, seconds = divmod(total_time, 60)
    
    print(f"\n{'=' * 50}")
    print(f"Pipeline completed successfully in {int(minutes)}m {int(seconds)}s!")
    print(f"{'=' * 50}")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 