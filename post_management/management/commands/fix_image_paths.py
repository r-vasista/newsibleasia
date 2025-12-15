"""
Django Management Command to fix incorrect image paths based on post_date.

Place this file in: your_app/management/commands/fix_image_paths.py

Usage: python manage.py fix_image_paths
"""

import os
import re
from pathlib import Path
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from post_management.models import NewsPost  # Replace 'your_app' with your actual app name


class Command(BaseCommand):
    help = 'Fixes NewsPost image paths to match their actual post_date location'

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
        self.log_path = logs_dir / f'fix_image_paths_{timestamp}.log'
        
        self.log_file = open(self.log_path, 'w', encoding='utf-8')
        self.log(f'Fix Image Paths Log - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        self.log('=' * 80)

    def extract_base_filename(self, filename):
        """
        Extract base filename without _c_c_c suffixes, random hashes, and extension.
        Examples:
            news1_image_c_c_c.jpg -> news1_image
            test_photo_c.webp -> test_photo
            Egypt_c_eLIBQpH_c_c_c.jpg -> Egypt
            Donald_Trump_c_Q6XQyFn_c_c.jpg -> Donald_Trump
            simple.png -> simple
        """
        # Remove extension
        name_without_ext = Path(filename).stem
        
        # Remove everything from the first _c onwards (including random hashes)
        # This handles cases like: Egypt_c_eLIBQpH_c_c_c -> Egypt
        if '_c' in name_without_ext:
            base_name = name_without_ext.split('_c')[0]
        else:
            base_name = name_without_ext
        
        return base_name

    def find_actual_image(self, base_filename, post_date):
        """
        Find the actual image file based on post_date and base filename.
        Searches in blog/YYYY/MM/DD/ folder for matching files.
        """
        # Construct the expected folder path based on post_date
        year = post_date.strftime('%Y')
        month = post_date.strftime('%m')
        day = post_date.strftime('%d')
        
        expected_folder = Path(settings.MEDIA_ROOT) / 'blog' / year / month / day
        
        if not expected_folder.exists():
            return None
        
        # Look for files that match the base filename with any extension
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
        
        for ext in image_extensions:
            # Try exact match first
            exact_file = expected_folder / f'{base_filename}{ext}'
            if exact_file.exists():
                return exact_file
            
            # Try with _c suffix (in case the correct file has _c)
            c_file = expected_folder / f'{base_filename}_c{ext}'
            if c_file.exists():
                return c_file
        
        # If exact match not found, try to find any file starting with base_filename
        for file in expected_folder.iterdir():
            if file.is_file() and file.stem.startswith(base_filename):
                # Make sure it's an image
                if file.suffix.lower() in image_extensions:
                    return file
        
        return None

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
            not_found_count = 0
            
            for post in all_posts:
                current_path = post.post_image.name  # Relative path like 'blog/2025/12/13/news1_c_c.jpg'
                current_filename = Path(current_path).name
                
                # Extract base filename without _c suffixes and extension
                base_filename = self.extract_base_filename(current_filename)
                
                # Get the date folder where image SHOULD be based on post_date
                expected_year = post.post_date.strftime('%Y')
                expected_month = post.post_date.strftime('%m')
                expected_day = post.post_date.strftime('%d')
                
                # Check if current path already matches the expected date
                current_date_in_path = f'{expected_year}/{expected_month}/{expected_day}'
                
                if current_date_in_path in current_path:
                    # Path is already correct date-wise
                    # But might have _c_c_c suffix, so still check
                    actual_file = self.find_actual_image(base_filename, post.post_date)
                    
                    if actual_file and str(actual_file) == post.post_image.path:
                        # Everything is correct, skip
                        skipped_count += 1
                        self.log(
                            f'✓ ALREADY CORRECT: Post #{post.id} - {post.post_title[:50]}',
                            self.style.SUCCESS
                        )
                        self.log(f'  Current: {current_path}')
                        continue
                
                # Find the actual image file
                actual_file = self.find_actual_image(base_filename, post.post_date)
                
                if actual_file:
                    # Calculate relative path from MEDIA_ROOT
                    media_root = Path(settings.MEDIA_ROOT)
                    relative_path = actual_file.relative_to(media_root)
                    new_path = str(relative_path)
                    
                    # Check if path needs updating
                    if new_path == current_path:
                        skipped_count += 1
                        self.log(
                            f'✓ ALREADY CORRECT: Post #{post.id} - {post.post_title[:50]}',
                            self.style.SUCCESS
                        )
                        self.log(f'  Current: {current_path}')
                    else:
                        self.log('\n' + '-' * 80)
                        self.log(
                            f'🔧 NEEDS UPDATE: Post #{post.id} - {post.post_title[:50]}',
                            self.style.WARNING
                        )
                        self.log(f'  Posted on: {post.post_date.strftime("%Y-%m-%d")}')
                        self.log(f'  Current (WRONG):  {current_path}')
                        self.log(f'  Correct (FOUND):  {new_path}')
                        
                        if not dry_run:
                            try:
                                post.post_image.name = new_path
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
                    not_found_count += 1
                    self.log('\n' + '-' * 80)
                    self.log(
                        f'❌ NOT FOUND: Post #{post.id} - {post.post_title[:50]}',
                        self.style.ERROR
                    )
                    self.log(f'  Posted on: {post.post_date.strftime("%Y-%m-%d")}')
                    self.log(f'  Current path: {current_path}')
                    self.log(f'  Base filename: {base_filename}')
                    self.log(f'  Expected location: blog/{expected_year}/{expected_month}/{expected_day}/')
                    self.log('  ⚠️  Could not find actual image file', self.style.ERROR)
            
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
            self.log(f'  • Not found (needs manual check): {not_found_count}')
            if error_count > 0:
                self.log(f'  • Errors: {error_count}', self.style.ERROR)
            
            self.log('\n' + '=' * 80)
            
            if not_found_count > 0:
                self.log(
                    f'\n⚠️  {not_found_count} posts have images that could not be found.',
                    self.style.WARNING
                )
                self.log(
                    'These may need manual investigation or the images may be truly missing.',
                    self.style.WARNING
                )
            
            # Log file location
            self.log(f'\n📄 Full log saved to: {self.log_path}', self.style.SUCCESS)
            
        finally:
            # Close log file
            if self.log_file:
                self.log_file.close()
