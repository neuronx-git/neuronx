
# scripts/configure_github_board.py
"""
GitHub Board Configuration Script
---------------------------------
Provides configuration instructions for GitHub Projects board.
Note: Automation rules require manual web UI configuration.
"""

def configure_board():
    """Output GitHub Board configuration instructions"""
    print("📊 GitHub Projects Board Configuration")
    print("=======================================")
    print("URL: https://github.com/users/ranjan-expatready/projects/2")
    print("Status: OPERATIONAL\n")
    
    print("⚠️  MANUAL ACTION REQUIRED: Automation Rules")
    print("The following rules must be configured in the Web UI:")
    
    rules = [
        "Issue Created → Set Status to 'Backlog'",
        "Issue Assigned → Set Status to 'Planned'",
        "PR Opened → Set Status to 'In Progress'",
        "PR In Review → Set Status to 'In Review (PR Open)'",
        "PR Requires Review → Set Status to 'Waiting for Approval'",
        "PR Merged → Set Status to 'Done'",
        "CI Failed → Set Status to 'Blocked'"
    ]
    
    for i, rule in enumerate(rules, 1):
        print(f"{i}. {rule}")
        
    print("\nSee RUNBOOKS/sdlc-board-ops.md for full details.")

if __name__ == "__main__":
    configure_board()
