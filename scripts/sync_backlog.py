import json
import subprocess
import os

def get_issues():
    try:
        cmd = ["gh", "issue list", "--json", "number,title,state,body,labels", "--limit", "100"]
        # gh CLI needs the separate arguments
        cmd = ["gh", "issue", "list", "--json", "number,title,state,body,labels", "--limit", "100"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error fetching issues: {e}")
        return []

def format_labels(labels):
    if not labels:
        return ""
    return ", ".join([f"`{l['name']}`" for l in labels])

def generate_markdown(issues):
    md = "# Project Backlog - Enterprise Ontology Library\n\n"
    md += "This document is automatically synchronized with GitHub Issues. Last updated: " 
    md += subprocess.run(["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True).stdout.strip() + "\n\n"
    
    # --- 1. OVERALL LIST (SUMMARY) ---
    md += "## 📋 Master Issue List\n\n"
    md += "| # | Status | Title | Description |\n"
    md += "| :--- | :--- | :--- | :--- |\n"
    for i in issues:
        status_icon = "🟢" if i['state'] == 'OPEN' else "🔴"
        # Clean description: first line or snippet
        desc = i.get('body', '').split('\n')[0].strip()[:100]
        if not desc: desc = "No description provided."
        md += f"| {i['number']} | {status_icon} {i['state']} | {i['title']} | {desc}... |\n"
    md += "\n---\n\n"

    # --- 2. GROUPED BY STATUS ---
    md += "## 📂 Workflow States\n\n"
    
    # Open Issues
    open_issues = [i for i in issues if i['state'] == 'OPEN']
    md += "### 🟢 Open / In Progress\n"
    if not open_issues:
        md += "_No open issues._\n\n"
    for i in open_issues:
        labels = format_labels(i.get('labels', []))
        md += f"#### [#{i['number']}] {i['title']}\n"
        md += f"- **Labels**: {labels}\n"
        md += f"- **Link**: [View Issue](https://github.com/The-Band-Solution/eo_lib/issues/{i['number']})\n\n"

    # Closed Issues
    closed_issues = [i for i in issues if i['state'] == 'CLOSED']
    md += "### 🔴 Closed / Done\n"
    if not closed_issues:
        md += "_No closed issues._\n\n"
    for i in closed_issues:
        md += f"- [#{i['number']}] {i['title']}\n"
    md += "\n---\n\n"

    # --- 3. GROUPED BY SPRINT (MILESTONE) ---
    md += "## 🏃 Sprints (Milestones)\n\n"
    
    milestones = {}
    no_milestone = []
    
    for i in issues:
        m = i.get('milestone')
        if m:
            m_title = m.get('title', 'Unknown Milestone')
            if m_title not in milestones:
                milestones[m_title] = []
            milestones[m_title].append(i)
        else:
            no_milestone.append(i)
            
    if not milestones and not no_milestone:
        md += "_No sprint data available._\n"
    else:
        for m_title, m_issues in milestones.items():
            md += f"### 🗓️ {m_title}\n"
            for i in m_issues:
                status_icon = "🟢" if i['state'] == 'OPEN' else "✅"
                md += f"- {status_icon} [#{i['number']}] {i['title']}\n"
            md += "\n"
        
        if no_milestone:
            md += "### 📥 No Sprint Assigned\n"
            for i in no_milestone:
                status_icon = "🟢" if i['state'] == 'OPEN' else "✅"
                md += f"- {status_icon} [#{i['number']}] {i['title']}\n"
    
    return md

def main():
    issues = get_issues()
    if not issues:
        print("No issues found or error occurred.")
        return

    content = generate_markdown(issues)
    
    file_path = "docs/backlog.md"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w") as f:
        f.write(content)
    
    print(f"Successfully updated {file_path}")

if __name__ == "__main__":
    main()
