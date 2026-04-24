import typer
from rich.console import Console
from pathlib import Path
from src.services import state_service, dashboard_service
from src.utils.utils import handle_error
from src.services.config_service import ConfigService

def register(app: typer, console: Console):
    @app.command("dashboard", help="Generates and uploads an S3 dashboard HTML")
    def dashboard(
        open_browser: bool = typer.Option(True, "--open", help="Open the dashboard in browser after upload"),
    ) -> None:
        """Generates a standalone HTML dashboard of your S3 bucket states and uploads it.
        
        The dashboard includes:
        - Visualization of all project states
        - Total disk usage statistics
        - Search and filtering capabilities
        """
        try:
            with console.status("[bold green]Fetching bucket data...", spinner="dots"):
                states = state_service.list_states(global_scan=True, use_cache=False)
                credentials = ConfigService.get_aws_credentials()
                bucket_name = credentials.bucket_name
            
            if not states:
                console.print("[yellow]No states found in bucket to generate dashboard.[/yellow]")
                return

            with console.status("[bold blue]Generating HTML Dashboard...", spinner="dots"):
                html_content = dashboard_service.DashboardService.generate_dashboard_html(states, bucket_name)
                
                # Write to temp file
                from tempfile import NamedTemporaryFile
                with NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as tmp:
                    tmp.write(html_content)
                    tmp_path = Path(tmp.name)
            
            with console.status("[bold magenta]Uploading to S3...", spinner="dots"):
                from src.clients import s3_client
                s3 = s3_client.create_s3_resource()
                # Upload to index.html at root (or a dedicated reports/ folder)
                target_key = "dashboard.html"
                s3.upload_file(str(tmp_path), target_key, ExtraArgs={'ContentType': 'text/html'})
                
                # Generate a pre-signed URL for temporary access
                s3_client_raw = s3_client.create_s3_client()
                url = s3_client_raw.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': bucket_name, 'Key': target_key},
                    ExpiresIn=3600 # 1 hour
                )

            console.print(f"\n[green][OK] Dashboard generated and uploaded to {bucket_name}/{target_key}[/green]")
            console.print(f"[bold cyan]Access URL (Valid for 1 hour):[/bold cyan]\n{url}\n")
            
            if open_browser:
                import webbrowser
                webbrowser.open(url)
                
            # Cleanup
            tmp_path.unlink()

        except Exception as e:
            handle_error(console, e)
