import os
from django.core.management.base import BaseCommand
from django.conf import settings
from item.models import Item
from core.models import Profile, SiteConfiguration
from django.core.files import File
import cloudinary.uploader

class Command(BaseCommand):
    help = 'Migrates local media files (Items, Profiles, and Logo) to Cloudinary'

    def handle(self, *args, **options):
        # 1. Migrate Items
        items = Item.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Found {items.count()} items to check.'))
        self.migrate_instances(items, 'image', 'item_images/')

        # 2. Migrate Profiles
        profiles = Profile.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Found {profiles.count()} profiles to check.'))
        self.migrate_instances(profiles, 'image', 'profile_images/')

        # 3. Initialize Site Configuration with Logo
        self.initialize_site_config()

        self.stdout.write(self.style.SUCCESS('Migration complete! Please check your Cloudinary dashboard.'))

    def migrate_instances(self, queryset, field_name, folder):
        for instance in queryset:
            field = getattr(instance, field_name)
            if not field:
                continue

            # Check if image is already a Cloudinary URL
            try:
                if field.url.startswith('http'):
                    self.stdout.write(self.style.SUCCESS(f'"{instance}" already has a remote URL. Skipping.'))
                    continue
            except ValueError:
                # This can happen if the field is empty or misconfigured
                continue

            local_path = field.path
            if os.path.exists(local_path):
                self.stdout.write(self.style.NOTICE(f'Uploading "{instance}" {field_name}: {local_path}'))
                try:
                    with open(local_path, 'rb') as f:
                        file_name = os.path.basename(local_path)
                        field.save(file_name, File(f), save=True)
                    self.stdout.write(self.style.SUCCESS(f'Successfully migrated "{instance}" to Cloudinary.'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to upload "{instance}": {str(e)}'))
            else:
                self.stdout.write(self.style.ERROR(f'Local file not found for "{instance}": {local_path}'))

    def initialize_site_config(self):
        config, created = SiteConfiguration.objects.get_or_create(id=1)
        if created:
            self.stdout.write(self.style.NOTICE('Created initial SiteConfiguration.'))
        
        # Try to upload the static logo as the initial dynamic logo
        static_logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
        
        if not config.logo and os.path.exists(static_logo_path):
            self.stdout.write(self.style.NOTICE(f'Initializing site logo from {static_logo_path}'))
            with open(static_logo_path, 'rb') as f:
                config.logo.save('logo.png', File(f), save=True)
            self.stdout.write(self.style.SUCCESS('Site logo initialized on Cloudinary.'))

        if not config.favicon and os.path.exists(static_logo_path):
            self.stdout.write(self.style.NOTICE(f'Initializing site favicon from {static_logo_path}'))
            with open(static_logo_path, 'rb') as f:
                config.favicon.save('favicon.png', File(f), save=True)
            self.stdout.write(self.style.SUCCESS('Site favicon initialized on Cloudinary.'))
