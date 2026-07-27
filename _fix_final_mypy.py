"""
Fix all 6 remaining mypy errors.
"""
import ast
import os


def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def check(path, content):
    try:
        ast.parse(content)
        return True
    except SyntaxError as e:
        print(f"SYNTAX ERROR in {path}: {e}")
        return False


# FIX 1: mikrotik.py - UniversalNATRule assigned to UniversalFirewallRule variable
# The issue is at line 317 in the NAT section. Let me check the exact code.
path = 'apps/network_engineer/vendor/mikrotik.py'
content = read(path)

# Look for: nat_action = ... then ast.nat_rules.append(UniversalNATRule(...))
# The error says "Incompatible types in assignment (expression has type "UniversalNATRule", variable has type "UniversalFirewallRule")"
# This means somewhere UniversalNATRule is being appended to firewall_rules or assigned to a firewall variable
# Let me check if there's a shared variable being reused

if 'UniversalNATRule' in content:
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'UniversalNATRule' in line:
            print(f"  [{i+1}] {line.strip()}")
    
    # Check if we need to fix imports or variable reuse
    # The error at line 317 might be a variable being reused after firewall_rules loop
    # Look for for nat_rule loops
    for i, line in enumerate(lines):
        if 'for nat_rule in config.nat_rules' in line:
            print(f"\n  NAT loop starts at line {i+1}")
            # Check the next lines
            for j in range(i, min(i+15, len(lines))):
                if 'ast.nat_rules.append' in lines[j]:
                    print(f"    -> line {j+1}: {lines[j].strip()}")
                    break

print("\nNeed to examine actual line 317...")

# FIX 2: execution.py - Artifact vs ExecutionArtifact
path2 = 'backend/app/api/execution.py'
content2 = read(path2)
# The issue: art from artifact_service.get_artifact returns Artifact, not ExecutionArtifact
# Need to convert properly
print(f"\nexecution.py: Looking for ExecutionArtifact usage...")
if 'ExecutionArtifact' in content2:
    for line in content2.split('\n'):
        if 'ExecutionArtifact' in line and 'from' not in line and 'import' not in line:
            print(f"  Usage: {line.strip()}")
    # Check getAllArtifact
    for line in content2.split('\n'):
        if 'get_artifact' in line:
            print(f"  get_artifact call: {line.strip()}")

# FIX 3: ai_studio.py - return type
path3 = 'backend/app/studio/ai_studio.py'
content3 = read(path3)
# The observability.get_trace might return list or dict
print(f"\nai_studio.py: Checking get_trace...")
for line in content3.split('\n'):
    if 'get_trace' in line:
        print(f"  {line.strip()}")

# FIX 4: task_queue.py 
path4 = 'backend/app/core/task_queue.py'
content4 = read(path4)
# Check for _serialize 
print(f"\ntask_queue.py: Checking _serialize...")
for i, line in enumerate(content4.split('\n')):
    if '_serialize' in line:
        print(f"  [{i+1}] {line.strip()}")
    if 'def enqueue' in line:
        print(f"  [{i+1}] {line.strip()}")
        for j in range(i, min(i+5, len(content4.split('\n')))):
            if '_serialize' in content4.split('\n')[j]:
                print(f"    -> [{j+1}] {content4.split('\n')[j].strip()}")

# FIX 5: society.py
path5 = 'apps/society/society.py'
content5 = read(path5)
print(f"\nsociety.py: Checking SubtaskResult...")
if 'SubtaskResult' in content5:
    print("  SubtaskResult is imported")
    for line in content5.split('\n'):
        if 'SubtaskResult' in line:
            print(f"  {line.strip()}")
else:
    print("  SubtaskResult NOT found - good (import removed if not needed)")

# Check results.append at line 449
lines5 = content5.split('\n')
print(f"\n  Line 449: {lines5[448].strip() if len(lines5) > 448 else 'N/A'}")
print(f"  Line 450: {lines5[449].strip() if len(lines5) > 449 else 'N/A'}")

print("\n=== Analysis complete ===")
