import subprocess
import re

'''
import subprocess

def get_squeue_output():
    """Execute the squeue command and return its output."""
    try:
        result = subprocess.run(['squeue'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error executing squeue: {result.stderr}")
            return None
        return result.stdout
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def parse_squeue_output(output):
    """Parse the squeue output to determine which nodes are taken."""
    taken_nodes = set()
    lines = output.strip().split('\n')
    
    # Skip the header line
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 8:
            node = parts[-1]
            taken_nodes.add(node)
    
    return taken_nodes

def main():
    output = get_squeue_output()
    if output is None:
        return
    
    taken_nodes = parse_squeue_output(output)
    
    print("Taken nodes:")
    for node in sorted(taken_nodes):
        print(node)

if __name__ == "__main__":
    main()

'''


def get_squeue_output():
    """Execute the squeue command and return its output."""
    try:
        result = subprocess.run(['squeue'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error executing squeue: {result.stderr}")
            return None
        return result.stdout
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def parse_squeue_output(output):
    """Parse the squeue output to determine which nodes are taken."""
    taken_nodes = set()
    lines = output.strip().split('\n')
    
    # Skip the header line
    for line in lines[1:]:
        parts = re.split(r'\s+', line)
        if len(parts) >= 8:
            node = parts[-1]
            taken_nodes.add(node)
    
    return taken_nodes

def get_all_nodes():
    """Get a list of all available nodes."""
    try:
        result = subprocess.run(['scontrol', 'show', 'nodes'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error executing scontrol: {result.stderr}")
            return None
        nodes = re.findall(r'NodeName=(\S+)', result.stdout)
        return set(nodes)
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def main():
    squeue_output = get_squeue_output()
    if squeue_output is None:
        return
    
    taken_nodes = parse_squeue_output(squeue_output)
    
    all_nodes = get_all_nodes()
    if all_nodes is None:
        return
    
    free_nodes = all_nodes - taken_nodes
    
    print("Taken nodes:")
    for node in sorted(taken_nodes):
        print(node)
    
    print("\nFree nodes:")
    for node in sorted(free_nodes):
        print(node)

if __name__ == "__main__":
    main()



'''

Explanation
get_squeue_output Function:

Executes the squeue command using subprocess.run.
Captures the standard output and error.
Returns the output if the command is successful, otherwise prints an error message.
parse_squeue_output Function:

Takes the output of squeue as input.
Splits the output into lines and skips the header line.
Extracts the node information from each line and adds it to a set of taken nodes.
main Function:

Calls get_squeue_output to get the squeue output.
Calls parse_squeue_output to parse the output and determine the taken nodes.
Prints the list of taken nodes.
Running the Script
Save the script to a file, for example, check_nodes.py, and run it using Python:

This script will print the list of nodes that are currently taken based on the output of the squeue command.







To refine the script for checking which nodes are taken based on the output of the squeue command, we can use additional commands and techniques to ensure robustness and clarity. Here is an improved version of the script:

Refined Python Script
Explanation
get_squeue_output Function:

Executes the squeue command using subprocess.run.
Captures the standard output and error.
Returns the output if the command is successful, otherwise prints an error message.
parse_squeue_output Function:

Takes the output of squeue as input.
Splits the output into lines and skips the header line.
Uses regular expressions to split the line into parts and extracts the node information.
Adds the node information to a set of taken nodes.
get_all_nodes Function:

Executes the scontrol show nodes command to get a list of all available nodes.
Uses regular expressions to extract node names from the output.
Returns a set of all node names.
main Function:

Calls get_squeue_output to get the squeue output.
Calls parse_squeue_output to parse the output and determine the taken nodes.
Calls get_all_nodes to get a list of all available nodes.
Calculates the free nodes by subtracting the taken nodes from all nodes.
Prints the list of taken and free nodes.
Running the Script
Save the script to a file, for example, check_nodes.py, and run it using Python:

This refined script will print the list of nodes that are currently taken and the list of nodes that are free based on the output of the squeue and scontrol show nodes commands.

'''