"""
UtopiaHire CLI - Command Line Interface
User-friendly interface for resume analysis and enhancement

WHY CLI FIRST:
- Test functionality quickly without building web UI
- Perfect for demos and initial testing
- Easy for technical users to use
- Can be automated with scripts
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
from rich.prompt import Prompt, Confirm
import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.resume_parser import ResumeParser
from utils.resume_analyzer import ResumeAnalyzer
from utils.resume_enhancer import ResumeEnhancer
from utils.job_matcher import JobMatcher
from utils.interview_simulator import InterviewSimulator
from config.database import (
    test_connection,
    insert_one,
    get_one,
    execute_query
)

# Rich console for beautiful output
console = Console()


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    🚀 UtopiaHire - AI Career Architect
    
    Empower job seekers in MENA and Sub-Saharan Africa with AI-powered resume optimization.
    
    \b
    Quick Start:
      utopiahire analyze resume.pdf        # Analyze a resume
      utopiahire enhance resume.pdf        # Get improvement suggestions
      utopiahire full resume.pdf           # Complete analysis + enhancement
    """
    # Check database connection
    if not test_connection():
        console.print("[yellow]⚠ Warning: Database connection failed. Some features may not work.[/yellow]")


@cli.command()
@click.argument('resume_file', type=click.Path(exists=True))
@click.option('--output', '-o', default=None, help='Output file for analysis report')
@click.option('--format', '-f', type=click.Choice(['text', 'json']), default='text', help='Output format')
def analyze(resume_file, output, format):
    """
    Analyze a resume and get detailed scores and suggestions.
    
    Example: utopiahire analyze resume.pdf
    """
    console.print("\n[bold cyan]📊 UtopiaHire Resume Analyzer[/bold cyan]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Parse resume
        task = progress.add_task("Parsing resume...", total=None)
        try:
            parser = ResumeParser()
            parsed = parser.parse_file(resume_file)
            progress.update(task, completed=True)
            console.print(f"✓ Parsed: {parsed['metadata']['word_count']} words\n")
        except Exception as e:
            console.print(f"[red]✗ Error parsing resume: {e}[/red]")
            return
        
        # Analyze resume
        task = progress.add_task("Analyzing resume...", total=None)
        try:
            analyzer = ResumeAnalyzer(use_ai_models=False)
            analysis = analyzer.analyze(parsed)
            progress.update(task, completed=True)
        except Exception as e:
            console.print(f"[red]✗ Error analyzing resume: {e}[/red]")
            return
    
    # Display results
    if format == 'json':
        _output_json(analysis, output)
    else:
        _display_analysis(analysis, parsed['metadata'])
        
        if output:
            _save_text_report(analysis, parsed['metadata'], output)


@cli.command()
@click.argument('resume_file', type=click.Path(exists=True))
@click.option('--output', '-o', default=None, help='Output file for enhanced resume')
def enhance(resume_file, output):
    """
    Enhance a resume with AI-powered improvements.
    
    Example: utopiahire enhance resume.pdf -o improved_resume.txt
    """
    console.print("\n[bold cyan]✨ UtopiaHire Resume Enhancer[/bold cyan]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Parse
        task = progress.add_task("Parsing resume...", total=None)
        parser = ResumeParser()
        parsed = parser.parse_file(resume_file)
        progress.update(task, completed=True)
        
        # Analyze
        task = progress.add_task("Analyzing resume...", total=None)
        analyzer = ResumeAnalyzer(use_ai_models=False)
        analysis = analyzer.analyze(parsed)
        progress.update(task, completed=True)
        
        # Enhance
        task = progress.add_task("Enhancing resume...", total=None)
        enhancer = ResumeEnhancer(use_ai_models=False)
        enhanced = enhancer.enhance_resume(parsed, analysis)
        progress.update(task, completed=True)
    
    # Display enhancements
    _display_enhancements(enhanced)
    
    # Save if requested
    if output:
        enhanced_text = enhancer.generate_improved_resume_text(enhanced)
        with open(output, 'w', encoding='utf-8') as f:
            f.write(enhanced_text)
        console.print(f"\n✓ Enhanced resume saved to: [green]{output}[/green]")


@cli.command()
@click.argument('resume_file', type=click.Path(exists=True))
@click.option('--output-dir', '-o', default='data/outputs', help='Output directory')
@click.option('--save-db', is_flag=True, help='Save results to database')
def full(resume_file, output_dir, save_db):
    """
    Complete analysis and enhancement pipeline.
    
    Example: utopiahire full resume.pdf --save-db
    """
    console.print("\n[bold cyan]🚀 UtopiaHire Full Analysis[/bold cyan]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Parse
        task = progress.add_task("[1/3] Parsing resume...", total=None)
        parser = ResumeParser()
        parsed = parser.parse_file(resume_file)
        progress.update(task, completed=True)
        console.print(f"✓ Parsed: {parsed['metadata']['word_count']} words")
        
        # Analyze
        task = progress.add_task("[2/3] Analyzing resume...", total=None)
        analyzer = ResumeAnalyzer(use_ai_models=False)
        analysis = analyzer.analyze(parsed)
        progress.update(task, completed=True)
        console.print(f"✓ Score: {analysis['scores']['overall_score']}/100")
        
        # Enhance
        task = progress.add_task("[3/3] Enhancing resume...", total=None)
        enhancer = ResumeEnhancer(use_ai_models=False)
        enhanced = enhancer.enhance_resume(parsed, analysis)
        progress.update(task, completed=True)
        console.print(f"✓ {len(enhanced['changes_made'])} improvements made\n")
    
    # Display everything
    console.print("\n[bold]📊 ANALYSIS RESULTS[/bold]")
    _display_analysis(analysis, parsed['metadata'], compact=True)
    
    console.print("\n[bold]✨ ENHANCEMENT RESULTS[/bold]")
    _display_enhancements(enhanced, compact=True)
    
    # Save to files
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = os.path.splitext(os.path.basename(resume_file))[0]
    
    # Save analysis
    analysis_file = os.path.join(output_dir, f"{base_name}_analysis_{timestamp}.json")
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, default=str)
    console.print(f"\n✓ Analysis saved: [green]{analysis_file}[/green]")
    
    # Save enhancement
    enhanced_file = os.path.join(output_dir, f"{base_name}_enhanced_{timestamp}.txt")
    enhanced_text = enhancer.generate_improved_resume_text(enhanced)
    with open(enhanced_file, 'w', encoding='utf-8') as f:
        f.write(enhanced_text)
    console.print(f"✓ Enhancement saved: [green]{enhanced_file}[/green]")
    
    # Save to database if requested
    if save_db:
        try:
            _save_to_database(parsed, analysis, enhanced)
            console.print("✓ Results saved to database")
        except Exception as e:
            console.print(f"[yellow]⚠ Could not save to database: {e}[/yellow]")


@cli.command()
def stats():
    """Show statistics from database."""
    console.print("\n[bold cyan]📈 UtopiaHire Statistics[/bold cyan]\n")
    
    try:
        # Total resumes
        result = execute_query("SELECT COUNT(*) as count FROM resumes")
        total_resumes = result[0]['count'] if result else 0
        
        # Total analyses
        result = execute_query("SELECT COUNT(*) as count FROM analyses")
        total_analyses = result[0]['count'] if result else 0
        
        # Average score
        result = execute_query("SELECT AVG(overall_score) as avg_score FROM analyses")
        avg_score = round(result[0]['avg_score'], 1) if result and result[0]['avg_score'] else 0
        
        # Create stats table
        table = Table(title="Database Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green", justify="right")
        
        table.add_row("Total Resumes Analyzed", str(total_resumes))
        table.add_row("Total Analyses", str(total_analyses))
        table.add_row("Average Score", f"{avg_score}/100")
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error fetching statistics: {e}[/red]")


def _display_analysis(analysis: dict, metadata: dict, compact: bool = False):
    """Display analysis results in a beautiful format"""
    scores = analysis['scores']
    
    # Scores table
    table = Table(title="📊 Resume Scores", show_header=True, header_style="bold magenta")
    table.add_column("Category", style="cyan", width=20)
    table.add_column("Score", justify="right", style="green", width=10)
    table.add_column("Grade", justify="center", width=15)
    
    table.add_row("Overall", f"{scores['overall_score']}/100", analysis['grade'])
    table.add_row("ATS Compatibility", f"{scores['ats_score']}/100", _score_to_emoji(scores['ats_score']))
    table.add_row("Formatting", f"{scores['formatting_score']}/100", _score_to_emoji(scores['formatting_score']))
    table.add_row("Keywords", f"{scores['keyword_score']}/100", _score_to_emoji(scores['keyword_score']))
    table.add_row("Content Quality", f"{scores['content_score']}/100", _score_to_emoji(scores['content_score']))
    
    console.print(table)
    
    if not compact:
        # Strengths
        if analysis['strengths']:
            console.print("\n[bold green]✅ Strengths:[/bold green]")
            for strength in analysis['strengths']:
                console.print(f"  {strength}")
        
        # Weaknesses
        if analysis['weaknesses']:
            console.print("\n[bold yellow]⚠️  Areas for Improvement:[/bold yellow]")
            for weakness in analysis['weaknesses']:
                console.print(f"  {weakness}")
        
        # Top suggestions
        console.print("\n[bold blue]💡 Top Suggestions:[/bold blue]")
        for i, suggestion in enumerate(analysis['suggestions'][:5], 1):
            priority_color = {"high": "red", "medium": "yellow", "low": "green"}[suggestion['priority']]
            console.print(f"  {i}. [{priority_color}][{suggestion['priority'].upper()}][/{priority_color}] {suggestion['message']}")


def _display_enhancements(enhanced: dict, compact: bool = False):
    """Display enhancement results"""
    summary = enhanced['improvement_summary']
    
    # Improvement summary
    panel = Panel(
        f"[green]Original Score:[/green] {summary['original_score']}/100\n"
        f"[green]Projected Score:[/green] {summary['estimated_new_score']}/100\n"
        f"[bold green]Improvement:[/bold green] +{summary['improvement_points']} points ({summary['improvement_percentage']}%)",
        title="📈 Score Projection",
        border_style="green"
    )
    console.print(panel)
    
    # Changes made
    if enhanced['changes_made']:
        console.print("\n[bold]✨ Changes Made:[/bold]")
        for change in enhanced['changes_made']:
            console.print(f"  • {change['section']}: {change['description']}")
    
    if not compact and enhanced.get('experience'):
        # Show sample enhanced bullets
        console.print("\n[bold]📝 Sample Enhanced Bullet Points:[/bold]")
        for exp in enhanced['experience'][:1]:
            original = exp.get('original_bullets', [])
            enhanced_bullets = exp.get('enhanced_bullets', [])
            
            for i, (orig, enh) in enumerate(zip(original[:2], enhanced_bullets[:2]), 1):
                console.print(f"\n  [dim]Before:[/dim] {orig}")
                console.print(f"  [green]After:[/green]  {enh}")


def _score_to_emoji(score: int) -> str:
    """Convert score to emoji grade"""
    if score >= 90:
        return "🌟 Excellent"
    elif score >= 80:
        return "✅ Good"
    elif score >= 70:
        return "👍 Fair"
    elif score >= 60:
        return "⚠️  Needs Work"
    else:
        return "❌ Poor"


def _output_json(data: dict, output_file: str = None):
    """Output data as JSON"""
    json_str = json.dumps(data, indent=2, default=str)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_str)
        console.print(f"✓ JSON saved to: [green]{output_file}[/green]")
    else:
        console.print(json_str)


def _save_text_report(analysis: dict, metadata: dict, output_file: str):
    """Save analysis as text report"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("UTOPIAHIRE RESUME ANALYSIS REPORT\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"File: {metadata['filename']}\n")
        f.write(f"Analyzed: {analysis['analyzed_at']}\n")
        f.write(f"Word Count: {metadata['word_count']}\n\n")
        
        f.write("SCORES:\n")
        f.write("-" * 70 + "\n")
        scores = analysis['scores']
        f.write(f"Overall Score: {scores['overall_score']}/100 - {analysis['grade']}\n")
        f.write(f"ATS Score: {scores['ats_score']}/100\n")
        f.write(f"Formatting: {scores['formatting_score']}/100\n")
        f.write(f"Keywords: {scores['keyword_score']}/100\n")
        f.write(f"Content: {scores['content_score']}/100\n\n")
        
        if analysis['strengths']:
            f.write("STRENGTHS:\n")
            f.write("-" * 70 + "\n")
            for strength in analysis['strengths']:
                f.write(f"✓ {strength}\n")
            f.write("\n")
        
        if analysis['weaknesses']:
            f.write("AREAS FOR IMPROVEMENT:\n")
            f.write("-" * 70 + "\n")
            for weakness in analysis['weaknesses']:
                f.write(f"⚠ {weakness}\n")
            f.write("\n")
        
        f.write("SUGGESTIONS:\n")
        f.write("-" * 70 + "\n")
        for i, suggestion in enumerate(analysis['suggestions'], 1):
            f.write(f"{i}. [{suggestion['priority'].upper()}] {suggestion['message']}\n")
            f.write(f"   Impact: {suggestion['impact']}\n\n")
    
    console.print(f"✓ Report saved to: [green]{output_file}[/green]")


def _save_to_database(parsed: dict, analysis: dict, enhanced: dict):
    """Save results to database"""
    # Save resume
    resume_id = insert_one('resumes', {
        'user_id': None,  # Anonymous for now
        'filename': parsed['metadata']['filename'],
        'file_path': parsed['metadata'].get('file_path', ''),
        'file_type': parsed['metadata']['file_type'],
        'raw_text': parsed['raw_text'],
        'parsed_data': json.dumps(parsed['structured_data']),
        'file_size': parsed['metadata']['file_size']
    })
    
    # Save analysis
    analysis_id = insert_one('analyses', {
        'resume_id': resume_id,
        'ats_score': analysis['scores']['ats_score'],
        'formatting_score': analysis['scores']['formatting_score'],
        'keyword_score': analysis['scores']['keyword_score'],
        'overall_score': analysis['scores']['overall_score'],
        'suggestions': json.dumps(analysis['suggestions']),
        'strengths': json.dumps(analysis['strengths']),
        'weaknesses': json.dumps(analysis['weaknesses']),
        'missing_sections': json.dumps(analysis['missing_sections']),
        'model_used': 'rule-based'
    })
    
    # Save enhanced version
    insert_one('improved_resumes', {
        'resume_id': resume_id,
        'analysis_id': analysis_id,
        'enhanced_text': json.dumps(enhanced),
        'enhanced_data': json.dumps(enhanced),
        'changes_made': json.dumps(enhanced['changes_made']),
        'improvement_percentage': enhanced['improvement_summary']['improvement_percentage']
    })


@cli.command()
@click.option('--queries', default='Software Engineer,Data Analyst,Frontend Developer', help='Job titles to search (comma-separated)')
@click.option('--locations', default='Tunisia,Egypt,Nigeria,Kenya', help='Locations to search (comma-separated)')
@click.option('--num', default=10, help='Number of jobs per query')
def scrape(queries, locations, num):
    """
    🔍 Scrape real jobs from APIs
    
    Example: utopiahire scrape --queries "Software Engineer" --locations "Tunisia"
    """
    console.print("\n[bold blue]🔍 UtopiaHire Job Scraper[/bold blue]\n")
    
    try:
        from utils.job_scraper import RealJobScraper
        
        query_list = [q.strip() for q in queries.split(',')]
        location_list = [l.strip() for l in locations.split(',')]
        
        console.print(f"Scraping jobs:")
        console.print(f"  Queries: {', '.join(query_list)}")
        console.print(f"  Locations: {', '.join(location_list)}")
        console.print(f"  Results per query: {num}\n")
        
        scraper = RealJobScraper()
        
        total_jobs = 0
        all_jobs = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            for query in query_list:
                for location in location_list:
                    task = progress.add_task(f"Fetching {query} in {location}...", total=None)
                    
                    jobs = scraper.search_jobs(query, location, num_results=num)
                    total_jobs += len(jobs)
                    all_jobs.extend(jobs)
                    
                    progress.update(task, completed=True)
                    console.print(f"✓ Found {len(jobs)} jobs for {query} in {location}")
        
        console.print(f"\n[green]✓ Total jobs scraped: {total_jobs}[/green]\n")
        
        # Show sample
        if all_jobs:
            console.print("[bold]Sample Jobs:[/bold]\n")
            for i, job in enumerate(all_jobs[:5], 1):
                console.print(f"{i}. [cyan]{job['title']}[/cyan] at [green]{job['company']}[/green]")
                console.print(f"   📍 {job['location']} | Source: {job['source']}")
                console.print(f"   🔗 {job['url']}\n")
        
        # Save to file
        output_dir = 'data/scraped_jobs'
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"{output_dir}/jobs_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(all_jobs, f, indent=2)
        
        console.print(f"✓ Jobs saved to: [green]{output_file}[/green]")
        
    except ImportError:
        console.print("[red]✗ Job scraper not available. Check installation.[/red]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise


@cli.command()
@click.argument('resume_file', type=click.Path(exists=True))
@click.option('--limit', default=10, help='Maximum number of job matches to show')
@click.option('--save', is_flag=True, help='Save matches to JSON file')
@click.option('--cached', is_flag=True, help='Use cached jobs only (faster, no API calls)')
def match(resume_file, limit, save, cached):
    """
    🎯 Find matching REAL job opportunities with apply links
    
    Examples:
      utopiahire match resume.pdf              # Fetch fresh real jobs (default)
      utopiahire match resume.pdf --cached     # Use cached jobs (faster)
      utopiahire match resume.pdf --limit 5    # Show top 5 matches
    
    NOTE: All matches include apply URLs for frontend "Apply Now" buttons!
    """
    console.print("\n[bold blue]🎯 UtopiaHire Job Matcher[/bold blue]\n")
    console.print("[dim]Matching with REAL jobs from live APIs...[/dim]\n")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            # Parse resume
            task1 = progress.add_task("Parsing resume...", total=None)
            parser = ResumeParser()
            parsed = parser.parse_file(resume_file)
            progress.update(task1, completed=True)
            console.print("✓ Resume parsed successfully\n")
            
            # Find matches
            task2 = progress.add_task("Searching for matching jobs...", total=None)
            matcher = JobMatcher(use_real_jobs=True)  # Always use real jobs
            matches = matcher.find_matches(parsed, limit=limit, fetch_real=not cached)  # Fetch unless cached
            progress.update(task2, completed=True)
        
        if not matches:
            console.print("[yellow]No job matches found. Try updating your skills![/yellow]")
            return
        
        console.print(f"[green]✓ Found {len(matches)} job matches![/green]\n")
        
        # Display matches
        for i, match in enumerate(matches, 1):
            job = match['job']
            score = match['match_score']
            
            # Job title panel
            console.print(Panel(
                f"[bold]{job['title']}[/bold] at [cyan]{job['company']}[/cyan]\n"
                f"📍 {job['location']} | {'🏠 Remote' if job['remote'] else '🏢 On-site'} | {job['type']}\n"
                f"💼 Experience: {job['experience_level']} | 💰 {job['salary_range']['min']}-{job['salary_range']['max']} {job['salary_range']['currency']}/month",
                title=f"Match #{i} - Score: {score['overall_score']}/100",
                border_style="green" if score['overall_score'] >= 80 else "yellow"
            ))
            
            # Score breakdown table
            score_table = Table(show_header=True, header_style="bold magenta", box=None)
            score_table.add_column("Metric", style="dim")
            score_table.add_column("Score", justify="right")
            
            score_table.add_row("Skills Match", f"{score['skill_score']}/100")
            score_table.add_row("Location Match", f"{score['location_score']}/100")
            score_table.add_row("Experience Match", f"{score['experience_score']}/100")
            
            console.print(score_table)
            
            # Matched skills
            if score['breakdown']['matched_skills']:
                console.print(f"\n✓ Matched Skills: [green]{', '.join(score['breakdown']['matched_skills'][:8])}[/green]")
            
            # Missing skills
            if score['breakdown']['missing_skills']:
                console.print(f"⚠️  Missing Skills: [yellow]{', '.join(score['breakdown']['missing_skills'][:5])}[/yellow]")
            
            console.print(f"\n🔗 Apply: {job['url']}\n")
            console.print("-" * 80 + "\n")
        
        # Save to file if requested
        if save:
            output_dir = 'data/outputs/job_matches'
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"{output_dir}/matches_{timestamp}.json"
            
            with open(output_file, 'w') as f:
                json.dump({
                    'resume': os.path.basename(resume_file),
                    'matches': matches,
                    'generated_at': datetime.now().isoformat()
                }, f, indent=2)
            
            console.print(f"✓ Matches saved to: [green]{output_file}[/green]")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise


@cli.command()
@click.option('--region', default='MENA', help='Region for market insights (MENA, Sub-Saharan Africa)')
def market(region):
    """
    📊 Get job market insights
    
    Example: utopiahire market --region MENA
    """
    console.print(f"\n[bold blue]📊 Job Market Insights: {region}[/bold blue]\n")
    
    try:
        matcher = JobMatcher()
        insights = matcher.get_market_insights(region)
        
        if insights['total_jobs'] == 0:
            console.print(f"[yellow]No data available for {region}[/yellow]")
            return
        
        # Summary panel
        console.print(Panel(
            f"Total Jobs: [cyan]{insights['total_jobs']}[/cyan]\n"
            f"Remote Jobs: [green]{insights['remote_jobs_percentage']}%[/green]",
            title=f"{region} Market Overview",
            border_style="blue"
        ))
        
        # Top skills table
        console.print("\n[bold]Top In-Demand Skills:[/bold]\n")
        skills_table = Table(show_header=True, header_style="bold magenta")
        skills_table.add_column("Rank", justify="center", style="cyan")
        skills_table.add_column("Skill", style="green")
        skills_table.add_column("Demand", justify="right")
        
        for i, skill_data in enumerate(insights['top_skills'][:10], 1):
            skills_table.add_row(
                str(i),
                skill_data['skill'],
                str(skill_data['demand'])
            )
        
        console.print(skills_table)
        
        # Average salaries
        console.print("\n[bold]Average Salaries by Experience Level:[/bold]\n")
        salary_table = Table(show_header=True, header_style="bold magenta")
        salary_table.add_column("Experience Level", style="cyan")
        salary_table.add_column("Average Salary", justify="right", style="green")
        
        for level, salary_data in insights['average_salaries'].items():
            salary_table.add_row(
                level,
                f"{salary_data['average']} {salary_data['currency']}/month"
            )
        
        console.print(salary_table)
        console.print()
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise


@cli.command()
@click.option('--type', '-t', 'session_type', 
              type=click.Choice(['technical', 'behavioral', 'mixed']), 
              default='mixed', 
              help='Interview type')
@click.option('--role', '-r', default='Software Engineer', help='Target job role')
@click.option('--level', '-l', 'difficulty',
              type=click.Choice(['junior', 'mid', 'senior']),
              default='mid',
              help='Difficulty level')
@click.option('--questions', '-q', default=5, help='Number of questions')
def interview(session_type, role, difficulty, questions):
    """
    🎤 Practice job interviews with AI feedback
    
    Example: utopiahire interview --type mixed --role "Software Engineer" --level mid
    """
    console.print("\n[bold magenta]🎤 UtopiaHire AI Interview Simulator[/bold magenta]\n")
    
    try:
        # Start session
        console.print(Panel(
            f"Session Type: [cyan]{session_type}[/cyan]\n"
            f"Job Role: [cyan]{role}[/cyan]\n"
            f"Difficulty: [cyan]{difficulty}[/cyan]\n"
            f"Questions: [cyan]{questions}[/cyan]",
            title="Interview Setup",
            border_style="magenta"
        ))
        
        simulator = InterviewSimulator()
        session_info = simulator.start_session(
            session_type=session_type,
            job_role=role,
            difficulty_level=difficulty,
            num_questions=questions
        )
        
        console.print(f"\n[green]✓ Session started (ID: {session_info['session_id']})[/green]\n")
        
        # Interview loop
        question_num = 1
        while True:
            question = simulator.get_next_question()
            
            if not question:
                break
            
            # Display question
            console.print(Panel(
                f"[bold]{question['question_text']}[/bold]\n\n"
                f"Type: [cyan]{question['question_type']}[/cyan] | "
                f"Category: [cyan]{question.get('category', 'N/A')}[/cyan]",
                title=f"Question {question['question_number']}/{question['total_questions']}",
                border_style="blue"
            ))
            
            # Get answer
            console.print("\n[yellow]Your answer (type 'skip' to skip, 'quit' to end session):[/yellow]")
            console.print("[dim]Press Enter after typing your answer:[/dim]\n")
            
            # Multiline input
            answer_lines = []
            while True:
                line = input()
                if line == "" and answer_lines:  # Empty line after content ends input
                    break
                answer_lines.append(line)
            
            answer = '\n'.join(answer_lines).strip()
            
            if answer.lower() == 'quit':
                console.print("\n[yellow]Ending session early...[/yellow]")
                break
            
            if answer.lower() == 'skip':
                console.print("[yellow]Question skipped[/yellow]\n")
                continue
            
            if len(answer) < 20:
                console.print("[red]Answer too short! Please provide a more detailed response.[/red]\n")
                continue
            
            # Analyze answer
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Analyzing your answer...", total=None)
                result = simulator.submit_answer(answer)
                progress.update(task, completed=True)
            
            # Display feedback
            scores = result['scores']
            feedback = result['feedback']
            
            console.print(f"\n[bold green]✓ Answer Submitted![/bold green]\n")
            
            # Scores table
            scores_table = Table(title="Your Scores", show_header=True, header_style="bold cyan")
            scores_table.add_column("Dimension", style="white")
            scores_table.add_column("Score", justify="center", style="green")
            
            for dimension, score in scores.items():
                if dimension != 'overall':
                    color = 'green' if score >= 70 else 'yellow' if score >= 50 else 'red'
                    scores_table.add_row(
                        dimension.replace('_', ' ').title(),
                        f"[{color}]{score}/100[/{color}]"
                    )
            
            console.print(scores_table)
            
            # Overall score
            overall_color = 'green' if scores['overall'] >= 70 else 'yellow' if scores['overall'] >= 50 else 'red'
            console.print(f"\n[bold]Overall Score: [{overall_color}]{scores['overall']}/100[/{overall_color}][/bold]\n")
            
            # Narrative feedback
            console.print(Panel(feedback['narrative'], title="AI Feedback", border_style="cyan"))
            
            # Ask if they want to continue
            if result['has_more_questions']:
                console.print()
                if not Confirm.ask("[bold]Continue to next question?[/bold]", default=True):
                    break
                console.print()
            
            question_num += 1
        
        # Complete session
        console.print("\n[bold blue]📊 Generating Session Report...[/bold blue]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Analyzing session performance...", total=None)
            summary = simulator.complete_session()
            progress.update(task, completed=True)
        
        # Display session summary
        console.print(Panel(
            f"Performance: [cyan]{summary['performance'].upper()}[/cyan]\n"
            f"Questions Answered: [cyan]{summary['questions_answered']}[/cyan]\n"
            f"Average Score: [cyan]{summary['average_scores']['overall']}/100[/cyan]\n"
            f"Total Time: [cyan]{summary['total_time_seconds']//60} minutes[/cyan]",
            title="Session Summary",
            border_style="green"
        ))
        
        # Ratings
        console.print("\n[bold]Your Ratings:[/bold]\n")
        ratings_table = Table(show_header=False)
        ratings_table.add_column("Category", style="cyan")
        ratings_table.add_column("Rating", style="yellow")
        
        ratings = summary['ratings']
        ratings_table.add_row("Technical", "⭐" * ratings['technical'])
        ratings_table.add_row("Communication", "⭐" * ratings['communication'])
        ratings_table.add_row("Confidence", "⭐" * ratings['confidence'])
        
        console.print(ratings_table)
        
        # Key strengths
        if summary['feedback']['key_strengths']:
            console.print("\n[bold green]✓ Key Strengths:[/bold green]")
            for strength in summary['feedback']['key_strengths']:
                console.print(f"  • {strength}")
        
        # Areas to improve
        if summary['feedback']['areas_to_improve']:
            console.print("\n[bold yellow]⚠ Areas to Improve:[/bold yellow]")
            for area in summary['feedback']['areas_to_improve']:
                console.print(f"  • {area}")
        
        # Preparation tips
        console.print(f"\n[bold blue]💡 Preparation Tips:[/bold blue]\n")
        console.print(summary['feedback']['preparation_tips'])
        
        console.print(f"\n[green]✓ Session complete! (ID: {summary['session_id']})[/green]\n")
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interview cancelled[/yellow]")
    except Exception as e:
        console.print(f"\n[red]✗ Error: {e}[/red]")
        import traceback
        traceback.print_exc()


@cli.command()
@click.option('--limit', '-l', default=10, help='Number of sessions to show')
def history(limit):
    """
    📜 View your interview practice history
    
    Example: utopiahire history --limit 10
    """
    console.print("\n[bold cyan]📜 Interview History[/bold cyan]\n")
    
    try:
        # For now, show all sessions (no user auth yet)
        sessions = execute_query(
            """
            SELECT 
                s.id,
                s.session_type,
                s.job_role,
                s.difficulty_level,
                s.questions_answered,
                s.average_score,
                s.status,
                s.started_at,
                f.overall_performance
            FROM interview_sessions s
            LEFT JOIN interview_feedback f ON s.id = f.session_id
            ORDER BY s.started_at DESC
            LIMIT %s
            """,
            (limit,)
        )
        
        if not sessions:
            console.print("[yellow]No interview sessions found. Start your first interview![/yellow]\n")
            return
        
        # Display sessions table
        table = Table(title=f"Recent Interview Sessions", show_header=True, header_style="bold magenta")
        table.add_column("ID", justify="center", style="cyan")
        table.add_column("Type", style="blue")
        table.add_column("Role", style="white")
        table.add_column("Level", style="yellow")
        table.add_column("Q's", justify="center", style="cyan")
        table.add_column("Avg Score", justify="center", style="green")
        table.add_column("Performance", style="magenta")
        table.add_column("Date", style="white")
        
        for session in sessions:
            score = session.get('average_score', 0)
            score_color = 'green' if score >= 70 else 'yellow' if score >= 50 else 'red'
            
            performance = session.get('overall_performance', 'N/A')
            perf_color = {
                'excellent': 'green',
                'good': 'blue',
                'average': 'yellow',
                'needs_improvement': 'red'
            }.get(performance, 'white')
            
            date_str = session['started_at'].strftime('%Y-%m-%d')
            
            table.add_row(
                str(session['id']),
                session['session_type'],
                session['job_role'],
                session['difficulty_level'],
                str(session.get('questions_answered', 0)),
                f"[{score_color}]{score:.1f}[/{score_color}]" if score else "N/A",
                f"[{perf_color}]{performance}[/{perf_color}]",
                date_str
            )
        
        console.print(table)
        console.print()
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        import traceback
        traceback.print_exc()


@cli.command()
@click.option('--github', '-g', help='GitHub username')
@click.option('--stackoverflow', '-s', type=int, help='Stack Overflow user ID')
@click.option('--user-id', '-u', default=1, help='User ID (default: 1)')
def scan(github, stackoverflow, user_id):
    """
    🔍 Scan your professional footprint across GitHub and Stack Overflow
    
    Example: utopiahire scan --github octocat --stackoverflow 22656
    """
    console.print("\n[bold cyan]🔍 Professional Footprint Scanner[/bold cyan]\n")
    
    if not github and not stackoverflow:
        console.print("[yellow]Please provide at least one platform to scan:[/yellow]")
        console.print("  --github <username>")
        console.print("  --stackoverflow <user_id>")
        console.print("\nExample: utopiahire scan --github octocat --stackoverflow 22656\n")
        return
    
    try:
        from utils.footprint_calculator import FootprintCalculator
        
        calculator = FootprintCalculator(user_id=user_id)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            # Scan GitHub
            if github:
                task = progress.add_task(f"Scanning GitHub: @{github}...", total=None)
                try:
                    calculator.scan_github(github)
                    progress.update(task, completed=True)
                    console.print(f"[green]✓ GitHub scan complete[/green]\n")
                except Exception as e:
                    console.print(f"[red]✗ GitHub scan failed: {e}[/red]\n")
            
            # Scan Stack Overflow
            if stackoverflow:
                task = progress.add_task(f"Scanning Stack Overflow: {stackoverflow}...", total=None)
                try:
                    calculator.scan_stackoverflow(stackoverflow)
                    progress.update(task, completed=True)
                    console.print(f"[green]✓ Stack Overflow scan complete[/green]\n")
                except Exception as e:
                    console.print(f"[red]✗ Stack Overflow scan failed: {e}[/red]\n")
            
            # Calculate footprint
            task = progress.add_task("Calculating footprint...", total=None)
            result = calculator.calculate_footprint()
            progress.update(task, completed=True)
        
        # Display results
        console.print(Panel.fit(
            f"[bold green]{result['overall_score']}/100[/bold green]\n"
            f"[dim]{result['performance_level'].upper()}[/dim]",
            title="[bold]Overall Footprint Score[/bold]",
            border_style="green"
        ))
        
        # Platform scores
        console.print("\n[bold]Platform Scores:[/bold]\n")
        table = Table(show_header=False, box=None)
        table.add_column("Platform", style="cyan")
        table.add_column("Score", justify="right")
        
        if result['github_score'] > 0:
            score_color = 'green' if result['github_score'] >= 70 else 'yellow' if result['github_score'] >= 50 else 'red'
            table.add_row("GitHub", f"[{score_color}]{result['github_score']}/100[/{score_color}]")
        
        if result['stackoverflow_score'] > 0:
            score_color = 'green' if result['stackoverflow_score'] >= 70 else 'yellow' if result['stackoverflow_score'] >= 50 else 'red'
            table.add_row("Stack Overflow", f"[{score_color}]{result['stackoverflow_score']}/100[/{score_color}]")
        
        console.print(table)
        
        # Dimension scores
        console.print("\n[bold]Dimension Scores:[/bold]\n")
        dims = Table(show_header=False, box=None)
        dims.add_column("Dimension", style="blue")
        dims.add_column("Score", justify="right")
        
        for dim, score in [
            ('Visibility', result['visibility_score']),
            ('Activity', result['activity_score']),
            ('Impact', result['impact_score']),
            ('Expertise', result['expertise_score'])
        ]:
            score_color = 'green' if score >= 70 else 'yellow' if score >= 50 else 'red'
            dims.add_row(dim, f"[{score_color}]{score}/100[/{score_color}]")
        
        console.print(dims)
        
        # Strengths
        if result['strengths']:
            console.print("\n[bold green]✅ Strengths:[/bold green]\n")
            for strength in result['strengths']:
                console.print(f"  • {strength}")
        
        # Weaknesses
        if result['weaknesses']:
            console.print("\n[bold yellow]⚠️  Areas to Improve:[/bold yellow]\n")
            for weakness in result['weaknesses']:
                console.print(f"  • {weakness}")
        
        # Recommendations
        if result['recommendations']:
            console.print("\n[bold blue]💡 Recommendations:[/bold blue]\n")
            for rec in result['recommendations']:
                console.print(f"  • {rec}")
        
        console.print(f"\n[dim]Percentile: Top {100 - result['percentile']}% | Peer Comparison: {result['peer_comparison']}[/dim]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        import traceback
        traceback.print_exc()


@cli.command()
@click.option('--user-id', '-u', default=1, help='User ID (default: 1)')
def footprint(user_id):
    """
    📊 View your current professional footprint score
    
    Example: utopiahire footprint
    """
    console.print("\n[bold cyan]📊 Professional Footprint Report[/bold cyan]\n")
    
    try:
        # Get profile data
        from config.database import get_one, execute_query
        
        profile = get_one('user_profiles', {'user_id': user_id})
        
        if not profile:
            console.print("[yellow]No footprint data found. Run 'utopiahire scan' first![/yellow]\n")
            return
        
        # Get latest scores
        scores = get_one('footprint_scores', {'profile_id': profile['id']})
        
        if not scores:
            console.print("[yellow]No scores calculated yet. Run 'utopiahire scan' first![/yellow]\n")
            return
        
        # Display main score
        console.print(Panel.fit(
            f"[bold green]{scores['overall_score']}/100[/bold green]\n"
            f"[dim]{scores['performance_level'].upper()}[/dim]",
            title="[bold]Overall Footprint Score[/bold]",
            border_style="green"
        ))
        
        # Platform scores
        console.print("\n[bold]Platform Scores:[/bold]\n")
        table = Table(show_header=False, box=None)
        table.add_column("Platform", style="cyan")
        table.add_column("Score", justify="right")
        
        for platform, score in [
            ('GitHub', scores['github_score']),
            ('Stack Overflow', scores['stackoverflow_score']),
            ('LinkedIn', scores['linkedin_score'])
        ]:
            if score > 0:
                score_color = 'green' if score >= 70 else 'yellow' if score >= 50 else 'red'
                table.add_row(platform, f"[{score_color}]{score}/100[/{score_color}]")
        
        console.print(table)
        
        # Dimension scores
        console.print("\n[bold]Dimension Scores:[/bold]\n")
        dims = Table(show_header=False, box=None)
        dims.add_column("Dimension", style="blue")
        dims.add_column("Score", justify="right")
        
        for dim, score in [
            ('Visibility', scores['visibility_score']),
            ('Activity', scores['activity_score']),
            ('Impact', scores['impact_score']),
            ('Expertise', scores['expertise_score'])
        ]:
            score_color = 'green' if score >= 70 else 'yellow' if score >= 50 else 'red'
            dims.add_row(dim, f"[{score_color}]{score}/100[/{score_color}]")
        
        console.print(dims)
        
        # Parse JSON fields (they may already be parsed by psycopg2)
        import json
        strengths = scores['strengths'] if isinstance(scores['strengths'], list) else (json.loads(scores['strengths']) if scores['strengths'] else [])
        weaknesses = scores['weaknesses'] if isinstance(scores['weaknesses'], list) else (json.loads(scores['weaknesses']) if scores['weaknesses'] else [])
        recommendations = scores['recommendations'] if isinstance(scores['recommendations'], list) else (json.loads(scores['recommendations']) if scores['recommendations'] else [])
        
        # Strengths
        if strengths:
            console.print("\n[bold green]✅ Strengths:[/bold green]\n")
            for strength in strengths:
                console.print(f"  • {strength}")
        
        # Weaknesses
        if weaknesses:
            console.print("\n[bold yellow]⚠️  Areas to Improve:[/bold yellow]\n")
            for weakness in weaknesses:
                console.print(f"  • {weakness}")
        
        # Recommendations
        if recommendations:
            console.print("\n[bold blue]💡 Recommendations:[/bold blue]\n")
            for rec in recommendations:
                console.print(f"  • {rec}")
        
        # Get history count
        history = execute_query(
            "SELECT COUNT(*) as count FROM footprint_history WHERE profile_id = %s",
            (profile['id'],)
        )
        scan_count = history[0]['count'] if history else 0
        
        console.print(f"\n[dim]Last scanned: {scores['calculated_at'].strftime('%Y-%m-%d %H:%M')} | Total scans: {scan_count}[/dim]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        import traceback
        traceback.print_exc()


@cli.command()
@click.option('--user-id', '-u', default=1, help='User ID (default: 1)')
@click.option('--limit', '-l', default=10, help='Number of historical records to show')
def trends(user_id, limit):
    """
    📈 View your footprint score trends over time
    
    Example: utopiahire trends --limit 10
    """
    console.print("\n[bold cyan]📈 Footprint Trends[/bold cyan]\n")
    
    try:
        from config.database import get_one, execute_query
        
        # Get profile
        profile = get_one('user_profiles', {'user_id': user_id})
        
        if not profile:
            console.print("[yellow]No footprint data found. Run 'utopiahire scan' first![/yellow]\n")
            return
        
        # Get history
        history = execute_query(
            """
            SELECT 
                overall_score,
                github_score,
                stackoverflow_score,
                score_change,
                improvement_percentage,
                recorded_at
            FROM footprint_history
            WHERE profile_id = %s
            ORDER BY recorded_at DESC
            LIMIT %s
            """,
            (profile['id'], limit)
        )
        
        if not history:
            console.print("[yellow]No historical data yet. Scan multiple times to see trends![/yellow]\n")
            return
        
        # Display history table
        table = Table(title=f"Score History (Last {len(history)} Scans)", show_header=True, header_style="bold magenta")
        table.add_column("Date", style="white")
        table.add_column("Overall", justify="center", style="cyan")
        table.add_column("GitHub", justify="center", style="blue")
        table.add_column("Stack Overflow", justify="center", style="yellow")
        table.add_column("Change", justify="center", style="green")
        
        for record in history:
            date_str = record['recorded_at'].strftime('%Y-%m-%d %H:%M')
            overall = record['overall_score']
            github = record.get('github_score', 0)
            stackoverflow = record.get('stackoverflow_score', 0)
            change = record.get('score_change', 0)
            
            # Color code change
            if change > 0:
                change_str = f"[green]+{change}[/green]"
            elif change < 0:
                change_str = f"[red]{change}[/red]"
            else:
                change_str = "0"
            
            table.add_row(
                date_str,
                str(overall),
                str(github) if github > 0 else "-",
                str(stackoverflow) if stackoverflow > 0 else "-",
                change_str
            )
        
        console.print(table)
        console.print()
        
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    cli()
