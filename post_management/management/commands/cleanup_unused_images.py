"""
Django Management Command to clean up unused images from all of December 2025.

Place this file in: your_app/management/commands/cleanup_unused_images.py

Usage: python manage.py cleanup_unused_images
"""

import os
from pathlib import Path
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from post_management.models import NewsPost


class Command(BaseCommand):
    help = 'Removes unused images from blog/2025/12/ (entire December 2025 folder)'

    def __init__(self):
        super().__init__()
        self.log_file = None
        self.log_path = None

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
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
        self.log_path = logs_dir / f'cleanup_unused_images_{timestamp}.log'
        
        self.log_file = open(self.log_path, 'w', encoding='utf-8')
        self.log(f'Cleanup Unused Images Log - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        self.log('=' * 80)

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Setup log file
        self.setup_log_file()
        
        try:
            if dry_run:
                self.log('=' * 70, self.style.WARNING)
                self.log('DRY RUN MODE - No files will be deleted', self.style.WARNING)
                self.log('=' * 70, self.style.WARNING)
            
            # Get ALL NewsPost instances with images (not just from December)
            all_posts = NewsPost.objects.exclude(post_image='').exclude(post_image=None)
            
            # Collect all image paths that ARE being used
            used_image_paths = set()
            used_images_list = []
            
            for post in all_posts:
                if post.post_image:
                    try:
                        full_path = Path(post.post_image.path)
                        # Normalize path for Windows
                        normalized_path = str(full_path).replace('\\', '/')
                        used_image_paths.add(normalized_path)
                        used_images_list.append({
                            'path': normalized_path,
                            'name': full_path.name,
                            'post_title': post.post_title,
                            'post_id': post.id
                        })
                    except Exception as e:
                        self.log(f'Warning: Could not process image for post #{post.id}: {str(e)}', self.style.WARNING)
            
            self.log('\n' + '=' * 70)
            self.log(f'IMAGES BEING USED ({len(used_images_list)}):', self.style.SUCCESS)
            self.log('=' * 70)
            for img in used_images_list:
                self.log(f'✓ {img["name"]}')
                self.log(f'  Post: {img["post_title"]} (ID: {img["post_id"]})')
            
            # Define the target directory for entire December 2025
            december_folder = Path(settings.MEDIA_ROOT) / 'blog' / '2025' / '12'
            
            if not december_folder.exists():
                self.log(f'\nFolder does not exist: {december_folder}', self.style.ERROR)
                return
            
            deleted_files = []
            kept_count = 0
            total_size_freed = 0
            error_count = 0
            
            self.log(f'\n' + '=' * 70)
            self.log(f'Scanning folder: {december_folder}')
            self.log('=' * 70)
            
            # Get all image files recursively from the December folder
            image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
            all_files = []
            
            try:
                for ext in image_extensions:
                    # Use rglob to search recursively through all subdirectories
                    all_files.extend(december_folder.rglob(f'*{ext}'))
            except Exception as e:
                self.log(f'Error scanning folder: {str(e)}', self.style.ERROR)
                return
            
            self.log(f'Found {len(all_files)} total image files in December 2025 folder\n')
            
            # Group files by day for better logging
            files_by_day = {}
            for image_file in all_files:
                # Get the day folder (e.g., "01", "12", "31")
                day = image_file.parent.name
                if day not in files_by_day:
                    files_by_day[day] = []
                files_by_day[day].append(image_file)
            
            # Process files day by day
            for day in sorted(files_by_day.keys()):
                day_files = files_by_day[day]
                
                self.log(f'\n--- Processing December {day}, 2025 ({len(day_files)} files) ---')
                
                for image_file in day_files:
                    try:
                        # Normalize path for comparison
                        full_path = str(image_file).replace('\\', '/')
                        
                        # Check if file exists (it might have been deleted)
                        if not image_file.exists():
                            self.log(f'⚠️  File no longer exists: {image_file.name}', self.style.WARNING)
                            continue
                        
                        # Get file size
                        try:
                            file_size = image_file.stat().st_size
                        except (FileNotFoundError, OSError) as e:
                            self.log(f'⚠️  Cannot access file: {image_file.name} - {str(e)}', self.style.WARNING)
                            error_count += 1
                            continue
                        
                        if full_path not in used_image_paths:
                            # This image is NOT being used - DELETE IT
                            deleted_files.append({
                                'name': image_file.name,
                                'path': full_path,
                                'day': day,
                                'size': file_size
                            })
                            
                            if dry_run:
                                self.log(
                                    f'✗ WOULD DELETE: {image_file.name} ({file_size / 1024:.2f} KB)',
                                    self.style.WARNING
                                )
                            else:
                                try:
                                    os.remove(image_file)
                                    self.log(
                                        f'✗ DELETED: {image_file.name} ({file_size / 1024:.2f} KB)',
                                        self.style.ERROR
                                    )
                                    total_size_freed += file_size
                                except FileNotFoundError:
                                    self.log(
                                        f'⚠️  File already deleted: {image_file.name}',
                                        self.style.WARNING
                                    )
                                except Exception as e:
                                    self.log(
                                        f'✗ ERROR deleting {image_file.name}: {str(e)}',
                                        self.style.ERROR
                                    )
                                    error_count += 1
                        else:
                            kept_count += 1
                            self.log(
                                f'✓ KEEPING: {image_file.name} ({file_size / 1024:.2f} KB) - IN USE',
                                self.style.SUCCESS
                            )
                    except Exception as e:
                        self.log(
                            f'✗ ERROR processing {image_file.name}: {str(e)}',
                            self.style.ERROR
                        )
                        error_count += 1
                        continue
            
            # Final Summary
            self.log('\n' + '=' * 70)
            if dry_run:
                self.log('DRY RUN SUMMARY:', self.style.WARNING)
            else:
                self.log('CLEANUP COMPLETE:', self.style.SUCCESS)
            self.log('=' * 70)
            
            self.log(f'\n📊 Statistics:')
            self.log(f'  • Images in use (kept): {kept_count}')
            self.log(f'  • Images {"that would be " if dry_run else ""}deleted: {len(deleted_files)}')
            if error_count > 0:
                self.log(f'  • Errors/Warnings: {error_count}')
            if not dry_run:
                self.log(f'  • Space freed: {total_size_freed / (1024*1024):.2f} MB')
            else:
                total_would_free = sum(f["size"] for f in deleted_files)
                self.log(f'  • Space would be freed: {total_would_free / (1024*1024):.2f} MB')
            
            if deleted_files:
                self.log(f'\n🗑️  Files {"that would be " if dry_run else ""}deleted by day:')
                # Group by day for summary
                deleted_by_day = {}
                for f in deleted_files:
                    day = f['day']
                    if day not in deleted_by_day:
                        deleted_by_day[day] = []
                    deleted_by_day[day].append(f)
                
                for day in sorted(deleted_by_day.keys()):
                    self.log(f'\n  December {day}:')
                    for f in deleted_by_day[day]:
                        self.log(f'    • {f["name"]} ({f["size"] / 1024:.2f} KB)')
            
            self.log('\n' + '=' * 70)
            self.log(f'📄 Full log saved to: {self.log_path}', self.style.SUCCESS)
            
        finally:
            # Close log file
            if self.log_file:
                self.log_file.close()