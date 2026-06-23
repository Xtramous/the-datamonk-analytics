"""CLI for Airflow Optimization Agent"""
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from src.agents.orchestrator import AgentOrchestrator
import json

app = typer.Typer()
console = Console()
orchestrator = AgentOrchestrator()


@app.command()
def analyze_all():
    """Run comprehensive analysis on all DAGs"""
    console.print(Panel("🤖 Airflow Optimization Agent - Full Analysis", style="bold blue"))

    with console.status("[bold cyan]Analyzing DAGs...", spinner="dots"):
        report = orchestrator.run_full_analysis()

    if "error" in report:
        console.print(f"[red]Error: {report['error']}[/red]")
        return

    # Display summary
    summary = report.get("summary", {})
    console.print("\n[bold green]📊 Optimization Summary[/bold green]")
    summary_table = Table(title="Cost Analysis")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="magenta")

    summary_table.add_row("Total DAGs", str(summary.get("total_dags")))
    summary_table.add_row("Current Monthly Cost", f"${summary.get('current_monthly_cost', 0):.2f}")
    summary_table.add_row("Potential Monthly Savings", f"${summary.get('potential_monthly_savings', 0):.2f}")
    summary_table.add_row("Potential Annual Savings", f"${summary.get('potential_annual_savings', 0):.2f}")
    summary_table.add_row("Optimization Rate", summary.get("optimization_rate"))

    console.print(summary_table)

    # Display priority order
    console.print("\n[bold green]🎯 DAG Optimization Priority[/bold green]")
    priority_table = Table(title="Recommended Order")
    priority_table.add_column("Priority", style="cyan")
    priority_table.add_column("DAG ID", style="magenta")

    for idx, dag_id in enumerate(report.get("priority_order", [])[:5], 1):
        priority_table.add_row(str(idx), dag_id)

    console.print(priority_table)

    # Display next actions
    console.print("\n[bold green]✅ Next Actions[/bold green]")
    for action in report.get("next_actions", []):
        console.print(f"  {action}")

    # Save report
    with open("optimization_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    console.print("\n[green]✓ Report saved to optimization_report.json[/green]")


@app.command()
def analyze_dag(dag_id: str):
    """Analyze a specific DAG"""
    console.print(Panel(f"🔍 Analyzing DAG: {dag_id}", style="bold blue"))

    with console.status(f"[bold cyan]Analyzing {dag_id}...", spinner="dots"):
        result = orchestrator.analyze_single_dag(dag_id)

    if "error" in result:
        console.print(f"[red]{result['error']}[/red]")
        return

    # Display analysis
    analysis = result.get("analysis", {})
    console.print("\n[bold green]📈 Performance Analysis[/bold green]")
    analysis_table = Table(title="Metrics")
    analysis_table.add_column("Metric", style="cyan")
    analysis_table.add_column("Value", style="magenta")

    assessment = analysis.get("assessment", "unknown")
    color = "green" if assessment == "good" else "yellow" if assessment == "okay" else "red"
    analysis_table.add_row("Assessment", f"[{color}]{assessment}[/{color}]")
    analysis_table.add_row("Estimated Cost Impact", f"${analysis.get('estimated_cost_impact', 0)}")
    analysis_table.add_row("Expected Savings", analysis.get("expected_savings"))

    console.print(analysis_table)

    # Display issues
    issues = analysis.get("issues", [])
    if issues:
        console.print("\n[bold red]⚠️  Performance Issues[/bold red]")
        for issue in issues:
            console.print(f"  • {issue}")

    # Display recommendations
    recommendations = result.get("recommendations", {})
    if recommendations and "error" not in recommendations:
        console.print("\n[bold green]💡 Recommendations[/bold green]")
        console.print(f"Primary Technique: {recommendations.get('primary_technique')}")
        console.print(f"Expected Monthly Savings: ${recommendations.get('expected_monthly_savings', 0)}")
        console.print(f"Implementation Time: {recommendations.get('estimated_implementation_hours', 0)} hours")
        console.print(f"Confidence Level: {recommendations.get('confidence_level')}")

        console.print("\n[bold]Implementation Steps:[/bold]")
        for step in recommendations.get('implementation_steps', []):
            console.print(f"  • {step}")

    # Display ROI
    roi = result.get("roi", {})
    if roi and "error" not in roi:
        console.print("\n[bold green]💰 ROI Analysis[/bold green]")
        roi_table = Table(title="Financial Impact")
        roi_table.add_column("Metric", style="cyan")
        roi_table.add_column("Value", style="magenta")

        roi_table.add_row("Monthly Savings", f"${roi.get('monthly_savings', 0):.2f}")
        roi_table.add_row("Annual Savings", f"${roi.get('annual_savings', 0):.2f}")
        roi_table.add_row("Payback Period", f"{roi.get('payback_period_days', 0)} days")
        roi_table.add_row("ROI", f"{roi.get('roi_percent', 0):.1f}%")
        roi_table.add_row("Recommendation", roi.get("recommendation", "defer"))

        console.print(roi_table)

    # Save detailed report
    with open(f"{dag_id}_analysis.json", "w") as f:
        json.dump(result, f, indent=2, default=str)
    console.print(f"\n[green]✓ Detailed report saved to {dag_id}_analysis.json[/green]")


@app.command()
def show_patterns():
    """Show learned optimization patterns"""
    console.print(Panel("📚 Learned Optimization Patterns", style="bold blue"))

    stats = orchestrator.pattern_store.get_statistics()

    console.print(f"\nTotal Patterns Stored: {stats.get('total_patterns')}")
    console.print(f"Average Savings: {stats.get('avg_savings_percent', 0):.1f}%")

    techniques = stats.get("techniques", {})
    if techniques:
        console.print("\n[bold]Techniques & Results:[/bold]")
        tech_table = Table(title="Optimization Techniques")
        tech_table.add_column("Technique", style="cyan")
        tech_table.add_column("Uses", style="magenta")
        tech_table.add_column("Avg Savings %", style="green")

        for technique, data in techniques.items():
            count = data.get("count", 0)
            total = data.get("total_savings", 0)
            avg = (total / count) if count > 0 else 0
            tech_table.add_row(technique, str(count), f"{avg:.1f}%")

        console.print(tech_table)


@app.command()
def demo():
    """Run demonstration with mock data"""
    console.print(Panel("🚀 Airflow Optimization Agent - Demo", style="bold blue"))

    console.print("\n[cyan]This demo shows how the agent works with mock data.[/cyan]")
    console.print("\nAgent Capabilities:")
    console.print("  1. ✓ Connects to Airflow REST API (collect metrics)")
    console.print("  2. ✓ Fetches Prometheus metrics (performance data)")
    console.print("  3. ✓ Uses Claude AI (intelligent analysis & recommendations)")
    console.print("  4. ✓ Stores patterns in Chroma (learning & retrieval)")
    console.print("  5. ✓ Calculates costs & ROI (financial impact)")

    console.print("\n[bold green]Setup Instructions:[/bold green]")
    console.print("  1. Create .env file with:")
    console.print("     - ANTHROPIC_API_KEY=your_key")
    console.print("     - AIRFLOW_BASE_URL=http://localhost:8080")
    console.print("     - PROMETHEUS_URL=http://localhost:9090")
    console.print("  2. Install dependencies: pip install -r requirements.txt")
    console.print("  3. Run: python -m src.cli analyze-all")

    console.print("\n[bold green]Next: Available Commands[/bold green]")
    console.print("  • python -m src.cli analyze-all       → Full analysis")
    console.print("  • python -m src.cli analyze-dag <id>  → Single DAG")
    console.print("  • python -m src.cli show-patterns      → Learned patterns")


@app.command()
def health():
    """Check agent health and connectivity"""
    console.print(Panel("🏥 Agent Health Check", style="bold blue"))

    checks = {
        "Anthropic API": False,
        "Airflow Connection": False,
        "Prometheus Connection": False,
        "Chroma Database": False,
    }

    try:
        orchestrator.analysis_agent.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=10,
            messages=[{"role": "user", "content": "ping"}]
        )
        checks["Anthropic API"] = True
    except Exception as e:
        console.print(f"[red]Anthropic API Error: {e}[/red]")

    try:
        dags = orchestrator.airflow_client.get_dags()
        checks["Airflow Connection"] = len(dags) >= 0
    except Exception as e:
        console.print(f"[yellow]Airflow Connection: {e}[/yellow]")

    try:
        orchestrator.prometheus_client.query("up")
        checks["Prometheus Connection"] = True
    except Exception as e:
        console.print(f"[yellow]Prometheus Connection: {e}[/yellow]")

    try:
        orchestrator.pattern_store.get_statistics()
        checks["Chroma Database"] = True
    except Exception as e:
        console.print(f"[red]Chroma Database Error: {e}[/red]")

    # Display results
    health_table = Table(title="System Health")
    health_table.add_column("Component", style="cyan")
    health_table.add_column("Status", style="magenta")

    for component, status in checks.items():
        status_str = "[green]✓[/green]" if status else "[red]✗[/red]"
        health_table.add_row(component, status_str)

    console.print(health_table)


if __name__ == "__main__":
    app()
