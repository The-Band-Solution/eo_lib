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
    md = "# Backlog - Enterprise Ontology Library\n\n"
    md += "This document is automatically synchronized with GitHub Issues. Last updated: " 
    md += subprocess.run(["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True).stdout.strip() + "\n\n"
    
    open_issues = [i for i in issues if i['state'] == 'OPEN']
    closed_issues = [i for i in issues if i['state'] == 'CLOSED']

    md += "## 📊 Summary\n"
    md += f"| Status | Count |\n| :--- | :--- |\n| 🟢 Open | {len(open_issues)} |\n| 🔴 Closed | {len(closed_issues)} |\n\n---\n\n"

    md += "## 🚀 Active Backlog\n\n"
    for i in open_issues:
        labels = format_labels(i.get('labels', []))
        desc = i.get('body', '').split('\n')[0][:150] # First line or first 150 chars
        md += f"### [OPEN] [#{i['number']}] {i['title']}\n"
        md += f"- **Labels**: {labels}\n"
        md += f"- **Preview**: {desc}...\n\n"

    md += "---\n\n## ✅ Completed\n\n"
    for i in closed_issues:
        md += f"### [CLOSED] [#{i['number']}] {i['title']}\n"
    
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
