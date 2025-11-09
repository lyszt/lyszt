#!/usr/bin/env python3
"""
Generate a visual HTML table from the project descriptions in README.md.
This script parses the markdown tables and creates a styled HTML table.
"""

import re
from datetime import datetime
from typing import List, Dict


def parse_readme_tables(readme_path: str) -> Dict[str, List[Dict[str, str]]]:
    """Parse the markdown tables from README.md."""
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tables = {}
    
    # Find each section with tables
    sections = [
        ("Ongoing personal projects", "ongoing"),
        ("Finished projects", "finished"),
        ("Abandoned projects", "abandoned"),
        ("College projects", "college"),
        ("Experiments", "experiments")
    ]
    
    for section_title, section_key in sections:
        # Find the section
        section_match = re.search(rf'\*\*{re.escape(section_title)}\*\*.*?\n(.*?)(?=\n\*\*|\n<br>|\Z)', content, re.DOTALL)
        
        if not section_match:
            continue
        
        section_content = section_match.group(1)
        
        # Parse the table rows (skip header and separator)
        rows = section_content.strip().split('\n')[2:]  # Skip header and separator line
        
        projects = []
        for row in rows:
            if not row.strip() or row.startswith('|---|'):
                continue
            
            # Split by pipe and clean up
            parts = [p.strip() for p in row.split('|')]
            if len(parts) >= 4:  # Should have empty, name, language, description
                projects.append({
                    'name': parts[1],
                    'language': parts[2],
                    'description': parts[3]
                })
        
        if projects:
            tables[section_key] = projects
    
    return tables


def generate_html_table(tables: Dict[str, List[Dict[str, str]]], output_path: str) -> None:
    """Generate a styled HTML table from the parsed data."""
    
    section_titles = {
        "ongoing": "🚀 Ongoing Personal Projects",
        "finished": "✅ Finished Projects",
        "abandoned": "⏸️ Abandoned Projects",
        "college": "🎓 College Projects",
        "experiments": "🧪 Experiments"
    }
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Projects Overview</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #24292f;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 2.5rem;
        }}
        
        h1 {{
            color: #24292f;
            font-size: 2.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            text-align: center;
        }}
        
        .subtitle {{
            color: #57606a;
            font-size: 1rem;
            text-align: center;
            margin-bottom: 2rem;
        }}
        
        .section {{
            margin-bottom: 3rem;
        }}
        
        .section-title {{
            color: #24292f;
            font-size: 1.75rem;
            font-weight: 600;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #667eea;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}
        
        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        th {{
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 1rem;
            border-bottom: 1px solid #d0d7de;
        }}
        
        tbody tr {{
            transition: background-color 0.2s ease;
        }}
        
        tbody tr:hover {{
            background-color: #f6f8fa;
        }}
        
        tbody tr:last-child td {{
            border-bottom: none;
        }}
        
        .project-name {{
            font-weight: 600;
            color: #0969da;
            font-size: 1.05rem;
        }}
        
        .language {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: #ddf4ff;
            color: #0969da;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        .description {{
            color: #57606a;
            line-height: 1.5;
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 1rem;
            }}
            
            .container {{
                padding: 1.5rem;
            }}
            
            h1 {{
                font-size: 1.75rem;
            }}
            
            table {{
                font-size: 0.875rem;
            }}
            
            th, td {{
                padding: 0.75rem 0.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>GitHub Projects Overview</h1>
        <p class="subtitle">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</p>
"""
    
    # Generate tables for each section
    for section_key, section_title in section_titles.items():
        if section_key not in tables or not tables[section_key]:
            continue
        
        html += f"""
        <div class="section">
            <h2 class="section-title">{section_title}</h2>
            <table>
                <thead>
                    <tr>
                        <th style="width: 20%;">Project</th>
                        <th style="width: 15%;">Language</th>
                        <th style="width: 65%;">Description</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        for project in tables[section_key]:
            html += f"""
                    <tr>
                        <td class="project-name">{project['name']}</td>
                        <td><span class="language">{project['language']}</span></td>
                        <td class="description">{project['description']}</td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
        </div>
"""
    
    html += """
    </div>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Table saved to {output_path}")


def main():
    """Main function to generate the projects table."""
    readme_path = "README.md"
    output_path = "github_projects_table.html"
    
    print(f"Parsing {readme_path}...")
    tables = parse_readme_tables(readme_path)
    
    total_projects = sum(len(projects) for projects in tables.values())
    print(f"Found {total_projects} projects across {len(tables)} sections")
    
    print("Generating HTML table...")
    generate_html_table(tables, output_path)
    
    print("Done!")


if __name__ == "__main__":
    main()
