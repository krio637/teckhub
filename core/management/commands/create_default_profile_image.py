from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates a default profile image'

    def handle(self, *args, **kwargs):
        # Create the profile_pics directory if it doesn't exist
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pics')
        os.makedirs(profile_pics_dir, exist_ok=True)

        # Set the size for the profile image
        size = (400, 400)
        
        # Create a new image with a purple background
        image = Image.new('RGB', size, color='#6f42c1')
        draw = ImageDraw.Draw(image)
        
        # Draw a circle for the avatar
        margin = 10
        circle_bbox = [margin, margin, size[0] - margin, size[1] - margin]
        draw.ellipse(circle_bbox, fill='#ffffff')
        
        # Draw a smaller circle for the person icon
        icon_margin = size[0] // 4
        icon_bbox = [icon_margin, icon_margin, size[0] - icon_margin, size[1] - icon_margin]
        draw.ellipse(icon_bbox, fill='#6f42c1')

        # Save the image
        output_path = os.path.join(profile_pics_dir, 'default.png')
        image.save(output_path, 'PNG')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created default profile image at {output_path}')) 