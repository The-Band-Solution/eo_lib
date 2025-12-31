import json
import subprocess
import os

def get_issues():
    try:
        cmd = ["gh", "issue", "list", "--json", "number,title,state,body,labels,milestone,assignees", "--limit", "100"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error fetching issues: {e}")
        return []

def format_labels(labels):
    if not labels:
        return ""
    return ", ".join([f"`{l['name']}`" for l in labels])

def format_assignees(assignees):
    if not assignees:
        return "-"
    return ", ".join([f"@{a['login']}" for a in assignees])

def generate_markdown(issues):
    md = "# Project Backlog - Enterprise Ontology Library\n\n"
    md += "This document is automatically synchronized with GitHub Issues. Last updated: " 
    md += subprocess.run(["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True).stdout.strip() + "\n\n"
    
    # --- 1. MASTER ISSUE LIST (OVERVIEW) ---
    md += "## 📋 Master Issue List\n"
    md += "Visão geral de todas as demandas, seus estados e executores.\n\n"
    md += "| # | Status | Title | Executor | Sprint | Milestone |\n"
    md += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
    for i in issues:
        status_icon = "🟢" if i['state'] == 'OPEN' else "✅"
        # Extract Sprint labels
        sprints = [l['name'].replace('Sprint: ', '') for l in i.get('labels', []) if l['name'].startswith('Sprint:')]
        sprint_str = ", ".join(sprints) if sprints else "-"
        # Milestone
        milestone = i.get('milestone', {}).get('title', '-') if i.get('milestone') else "-"
        # Assignees
        executors = format_assignees(i.get('assignees', []))
        
        # Hyperlinked issue number
        issue_link = f"[#{i['number']}](https://github.com/The-Band-Solution/eo_lib/issues/{i['number']})"
        
        md += f"| {issue_link} | {status_icon} | {i['title']} | {executors} | {sprint_str} | {milestone} |\n"
    md += "\n---\n\n"

    # --- 2. GROUPED BY WORKFLOW STATUS ---
    md += "## 📂 Workflow States\n\n"
    
    for state in ['OPEN', 'CLOSED']:
        title = "🟢 In Progress / Todo" if state == 'OPEN' else "✅ Done / Released"
        items = [i for i in issues if i['state'] == state]
        md += f"### {title}\n"
        if not items:
            md += "_Nenhuma issue neste estado._\n\n"
        for i in items:
            executors = format_assignees(i.get('assignees', []))
            issue_link = f"[#{i['number']}](https://github.com/The-Band-Solution/eo_lib/issues/{i['number']})"
            md += f"- {issue_link} **{i['title']}** (Executor: {executors})\n"
        md += "\n"
    md += "---\n\n"

    # --- 3. GROUPED BY SPRINT (INTERACTIONS) ---
    md += "## 🏃 Sprints (Interactions)\n"
    md += "Demandas organizadas por ciclos de execução. Uma issue pode aparecer em múltiplos sprints.\n\n"
    
    sprints_map = {}
    for i in issues:
        sprints = [l['name'] for l in i.get('labels', []) if l['name'].startswith('Sprint:')]
        if not sprints:
            if "No Sprint" not in sprints_map: sprints_map["No Sprint"] = []
            sprints_map["No Sprint"].append(i)
        for s in sprints:
            if s not in sprints_map: sprints_map[s] = []
            sprints_map[s].append(i)
            
    # Sort sprints by name
    for s_name in sorted(sprints_map.keys()):
        md += f"### 🗓️ {s_name}\n"
        for i in sprints_map[s_name]:
            status_icon = "🟢" if i['state'] == 'OPEN' else "✅"
            issue_link = f"[#{i['number']}](https://github.com/The-Band-Solution/eo_lib/issues/{i['number']})"
            md += f"- {status_icon} {issue_link} {i['title']}\n"
        md += "\n"
    md += "---\n\n"

    # --- 4. GROUPED BY MILESTONE (DELIVERY MARKS) ---
    md += "## 🎯 Delivery Marks (Milestones)\n"
    md += "Grandes entregas e objetivos estratégicos.\n\n"
    
    milestones_map = {}
    for i in issues:
        m = i.get('milestone', {}).get('title', 'Backlog / No Milestone') if i.get('milestone') else 'Backlog / No Milestone'
        if m not in milestones_map: milestones_map[m] = []
        milestones_map[m].append(i)
        
    for m_name in sorted(milestones_map.keys()):
        md += f"### 🏁 {m_name}\n"
        for i in milestones_map[m_name]:
            status_icon = "🟢" if i['state'] == 'OPEN' else "✅"
            issue_link = f"[#{i['number']}](https://github.com/The-Band-Solution/eo_lib/issues/{i['number']})"
            md += f"- {status_icon} {issue_link} {i['title']}\n"
        md += "\n"
    md += "---\n\n"

    # --- 5. DETAILED BACKLOG ---
    md += "## 📝 Detailed Backlog\n"
    md += "Detalhamento completo de cada issue.\n\n"
    for i in issues:
        state_label = "OPEN" if i['state'] == 'OPEN' else "CLOSED"
        issue_link = f"[#{i['number']}](https://github.com/The-Band-Solution/eo_lib/issues/{i['number']})"
        md += f"### [{state_label}] {issue_link} {i['title']}\n"
        
        executors = format_assignees(i.get('assignees', []))
        labels = format_labels(i.get('labels', []))
        milestone = i.get('milestone', {}).get('title', '-') if i.get('milestone') else "-"
        
        md += f"- **Executor**: {executors}\n"
        md += f"- **Labels**: {labels}\n"
        md += f"- **Milestone**: {milestone}\n"
        
        # Add body snippet if exists
        if i.get('body'):
            body_snippet = i['body'][:300] + "..." if len(i['body']) > 300 else i['body']
            md += f"\n**Description**:\n{body_snippet}\n"
        md += "\n---\n\n"
    
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
