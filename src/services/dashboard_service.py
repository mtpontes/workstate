import json
from datetime import datetime
from src.utils import utils
from src.model.dto.state_dto import StateDTO

class DashboardService:
    @staticmethod
    def generate_dashboard_html(states: list[StateDTO], bucket_name: str) -> str:
        """Generates a standalone premium HTML dashboard."""
        
        # Group by project
        projects = {}
        total_size = 0
        for s in states:
            project_name = s.key.split("/")[0] if "/" in s.key else "root"
            if project_name not in projects:
                projects[project_name] = []
            projects[project_name].append(s)
            total_size += s.size
            
        project_details = []
        for name, p_states in projects.items():
            project_size = sum(s.size for s in p_states)
            last_mod = max(s.last_modified for s in p_states)
            project_details.append({
                "name": name,
                "count": len(p_states),
                "total_size": utils.format_file_size(project_size),
                "last_modified": last_mod.strftime("%Y-%m-%d %H:%M:%S"),
                "states": [
                    {
                        "key": s.key,
                        "size": utils.format_file_size(s.size),
                        "modified": s.last_modified.strftime("%Y-%m-%d %H:%M:%S"),
                        "protected": s.is_protected
                    } for s in p_states
                ]
            })

        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Workstate Dashboard - {bucket_name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --accent: #38bdf8;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --glass-border: rgba(255, 255, 255, 0.1);
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 40px 20px;
        }}
        
        .container {{ max-width: 1200px; margin: 0 auto; }}
        
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            padding: 20px;
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
        }}
        
        .logo-area h1 {{ font-size: 1.5rem; font-weight: 700; letter-spacing: -0.025em; }}
        .logo-area span {{ color: var(--accent); }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            padding: 24px;
            border-radius: 16px;
            transition: transform 0.2s ease;
        }}
        .stat-card:hover {{ transform: translateY(-4px); }}
        .stat-label {{ color: var(--text-secondary); font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }}
        .stat-value {{ font-size: 1.875rem; font-weight: 700; margin-top: 8px; color: var(--accent); }}
        
        .search-area {{ margin-bottom: 30px; }}
        #searchBar {{
            width: 100%;
            padding: 16px 24px;
            background: var(--card-bg);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            color: white;
            font-size: 1rem;
            outline: none;
        }}
        #searchBar:focus {{ border-color: var(--accent); }}
        
        .project-list {{ display: grid; gap: 24px; }}
        .project-card {{
            background: var(--card-bg);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            overflow: hidden;
        }}
        
        .project-header {{
            padding: 20px 24px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.03);
            transition: background 0.2s;
        }}
        .project-header:hover {{ background: rgba(255, 255, 255, 0.06); }}
        
        .project-info h2 {{ font-size: 1.25rem; font-weight: 600; }}
        .project-meta {{ font-size: 0.875rem; color: var(--text-secondary); }}
        
        .state-table-wrapper {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
            background: rgba(0,0,0,0.2);
        }}
        .project-card.active .state-table-wrapper {{ max-height: 1000px; }}
        
        table {{ width: 100%; border-collapse: collapse; text-align: left; }}
        th {{ padding: 12px 24px; font-size: 0.75rem; text-transform: uppercase; color: var(--text-secondary); border-bottom: 1px solid var(--glass-border); }}
        td {{ padding: 12px 24px; font-size: 0.875rem; border-bottom: 1px solid rgba(255,255,255,0.05); }}
        
        .badge {{
            padding: 2px 8px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .badge-protected {{ background: rgba(244, 63, 94, 0.2); color: #fb7185; }}
        .badge-standard {{ background: rgba(56, 189, 248, 0.2); color: #7dd3fc; }}
        
        footer {{ margin-top: 60px; text-align: center; color: var(--text-secondary); font-size: 0.875rem; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo-area">
                <h1>WORK<span>STATE</span> DASHBOARD</h1>
            </div>
            <div class="project-count">
                Bucket: <span style="color: var(--accent)">{bucket_name}</span>
            </div>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total states</div>
                <div class="stat-value">{len(states)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Use</div>
                <div class="stat-value">{utils.format_file_size(total_size)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Projects</div>
                <div class="stat-value">{len(projects)}</div>
            </div>
        </div>

        <div class="search-area">
            <input type="text" id="searchBar" placeholder="Search projects or files..." onkeyup="filterProjects()">
        </div>

        <div class="project-list" id="projectList">
            {DashboardService._generate_project_cards_html(project_details)}
        </div>

        <footer>
            Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} by Workstate CLI
        </footer>
    </div>

    <script>
        function toggleProject(el) {{
            el.closest('.project-card').classList.toggle('active');
        }}

        function filterProjects() {{
            const query = document.getElementById('searchBar').value.toLowerCase();
            const cards = document.querySelectorAll('.project-card');
            
            cards.forEach(card => {{
                const text = card.innerText.toLowerCase();
                card.style.display = text.includes(query) ? 'block' : 'none';
            }});
        }}
    </script>
</body>
</html>"""
        return html_template

    @staticmethod
    def _generate_project_cards_html(project_details: list[dict]) -> str:
        cards = []
        for p in project_details:
            rows = []
            for s in p["states"]:
                badge = '<span class="badge badge-protected">Protected</span>' if s["protected"] else '<span class="badge badge-standard">Standard</span>'
                rows.append(f"""
                <tr>
                    <td>{s["key"]}</td>
                    <td>{s["size"]}</td>
                    <td>{s["modified"]}</td>
                    <td>{badge}</td>
                </tr>
                """)
            
            card = f"""
            <div class="project-card">
                <div class="project-header" onclick="toggleProject(this)">
                    <div class="project-info">
                        <h2>{p["name"]}</h2>
                        <div class="project-meta">{p["count"]} states • Total: {p["total_size"]}</div>
                    </div>
                    <div class="project-date">
                        Last modified: {p["last_modified"]}
                    </div>
                </div>
                <div class="state-table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>File Name</th>
                                <th>Size</th>
                                <th>Modified</th>
                                <th>Type</th>
                            </tr>
                        </thead>
                        <tbody>
                            {"".join(rows)}
                        </tbody>
                    </table>
                </div>
            </div>
            """
            cards.append(card)
        return "".join(cards)
