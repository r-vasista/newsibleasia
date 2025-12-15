"""
Django Management Command to fix Windows backslashes in image paths.

Place this file in: your_app/management/commands/fix_path_slashes.py

Usage: python manage.py fix_path_slashes
"""

from pathlib import Path
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from post_management.models import NewsPost


class Command(BaseCommand):
    help = 'Fixes Windows backslashes (\\) to forward slashes (/) in image paths'

    def __init__(self):
        super().__init__()
        self.log_file = None
        self.log_path = None

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without actually updating',
        )

    def log(self, message, style=None):
        """Write to both console and log file"""
        # Write to console
        if style:
            self.stdout.write(style(message))
        else:
            self.stdout.write(message)
        
        # Write to log file (without color codes)
        if self.log_file:
            import re
            # Remove ANSI color codes for log file
            clean_message = re.sub(r'\x1b\[[0-9;]*m', '', message)
            self.log_file.write(clean_message + '\n')
            self.log_file.flush()

    def setup_log_file(self):
        """Create log file for this run"""
        # Create logs directory if it doesn't exist
        logs_dir = Path(settings.BASE_DIR) / 'logs'
        logs_dir.mkdir(exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_path = logs_dir / f'fix_path_slashes_{timestamp}.log'
        
        self.log_file = open(self.log_path, 'w', encoding='utf-8')
        self.log(f'Fix Path Slashes Log - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        self.log('=' * 80)

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Setup log file
        self.setup_log_file()
        
        try:
            if dry_run:
                self.log('=' * 80, self.style.WARNING)
                self.log('DRY RUN MODE - No database updates will be made', self.style.WARNING)
                self.log('=' * 80, self.style.WARNING)
            
            # Get all NewsPost instances with images
            all_posts = NewsPost.objects.exclude(post_image='').exclude(post_image=None)
            
            self.log(f'\nFound {all_posts.count()} posts with images\n')
            
            updated_count = 0
            skipped_count = 0
            error_count = 0
            
            for post in all_posts:
                current_path = post.post_image.name
                
                # Check if path contains backslashes
                if '\\' in current_path:
                    # Convert backslashes to forward slashes
                    fixed_path = current_path.replace('\\', '/')
                    
                    self.log('-' * 80)
                    self.log(
                        f'🔧 NEEDS FIX: Post #{post.id} - {post.post_title[:60]}',
                        self.style.WARNING
                    )
                    self.log(f'  Current (WRONG): {current_path}')
                    self.log(f'  Fixed (CORRECT): {fixed_path}')
                    
                    if not dry_run:
                        try:
                            post.post_image.name = fixed_path
                            post.save(update_fields=['post_image'])
                            updated_count += 1
                            self.log('  ✅ UPDATED', self.style.SUCCESS)
                        except Exception as e:
                            error_count += 1
                            self.log(f'  ❌ ERROR: {str(e)}', self.style.ERROR)
                    else:
                        updated_count += 1
                        self.log('  ⏭️  WOULD UPDATE', self.style.WARNING)
                else:
                    # Path is already correct
                    skipped_count += 1
                    if skipped_count <= 5:  # Show first 5 correct paths
                        self.log(
                            f'✓ ALREADY CORRECT: Post #{post.id} - {post.post_title[:60]}',
                            self.style.SUCCESS
                        )
                        self.log(f'  Path: {current_path}')
            
            if skipped_count > 5:
                self.log(f'\n... and {skipped_count - 5} more posts already have correct paths')
            
            # Final Summary
            self.log('\n' + '=' * 80)
            if dry_run:
                self.log('DRY RUN SUMMARY:', self.style.WARNING)
            else:
                self.log('FIX COMPLETE:', self.style.SUCCESS)
            self.log('=' * 80)
            
            self.log(f'\n📊 Statistics:')
            self.log(f'  • Total posts checked: {all_posts.count()}')
            self.log(f'  • Already correct (skipped): {skipped_count}')
            self.log(f'  • {"Would be updated" if dry_run else "Successfully updated"}: {updated_count}')
            if error_count > 0:
                self.log(f'  • Errors: {error_count}', self.style.ERROR)
            
            self.log('\n' + '=' * 80)
            self.log(f'📄 Full log saved to: {self.log_path}', self.style.SUCCESS)
            
        finally:
            # Close log file
            if self.log_file:
                self.log_file.close()
                