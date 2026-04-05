import os
from django.core.management.base import BaseCommand
from django.conf import settings
from item.models import Item
from django.core.files import File
import cloudinary.uploader

class Command(BaseCommand):
    help = 'Migrates local media files to Cloudinary'

    def handle(self, *args, **options):
        items = Item.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Found {items.count()} items to check.'))

        for item in items:
            if not item.image:
                self.stdout.write(self.style.WARNING(f'Item "{item.name}" has no image. Skipping.'))
                continue

            # Check if image is already a Cloudinary URL
            if item.image.url.startswith('http'):
                self.stdout.write(self.style.SUCCESS(f'Item "{item.name}" already has a remote URL. Skipping.'))
                continue

            local_path = item.image.path
            if os.path.exists(local_path):
                self.stdout.write(self.style.NOTICE(f'Uploading "{item.name}" image: {local_path}'))
                try:
                    # Upload to Cloudinary
                    with open(local_path, 'rb') as f:
                        # Use the original filename but let Cloudinary handle folders
                        result = cloudinary.uploader.upload(
                            f,
                            folder='item_images/'
                        )
                    
                    # Update item image field with the public_id or the URL
                    # django-cloudinary-storage handles the mapping if we just 
                    # use the relative path that it expects, or if we assign it directly.
                    # The easiest way is to let the result['secure_url'] or similar be used.
                    
                    # However, since we use DEFAULT_FILE_STORAGE, just saving the file 
                    # through the field will trigger the storage backend.
                    
                    with open(local_path, 'rb') as f:
                        file_name = os.path.basename(local_path)
                        item.image.save(file_name, File(f), save=True)

                    self.stdout.write(self.style.SUCCESS(f'Successfully migrated "{item.name}" to Cloudinary.'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to upload "{item.name}": {str(e)}'))
            else:
                self.stdout.write(self.style.ERROR(f'Local file not found for "{item.name}": {local_path}'))

        self.stdout.write(self.style.SUCCESS('Migration complete! Please check your Cloudinary dashboard.'))
