from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.conf import settings
from urllib.parse import urlencode
import qrcode
import webcolors
import uuid
import os
from qrcode.image.styledpil import StyledPilImage
from PIL import Image

from qrcode.image.styles.moduledrawers.pil import (
    SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer, RoundedModuleDrawer, VerticalBarsDrawer,
    HorizontalBarsDrawer
)

from qrcode.image.styles.colormasks import (
    SolidFillColorMask, RadialGradiantColorMask, SquareGradiantColorMask, HorizontalGradiantColorMask,
    VerticalGradiantColorMask
)


class QrGenView(View):
    def get(self, request, *args, **kwargs):
        # Page Status
        created = request.GET.get('created')
        image_url = request.GET.get('image_url')

        return render(request, 'home_page.html', {'created': created, 'image_url': image_url})

    def post(self, request: HttpRequest, *args, **kwargs):
        data = request.POST

        # Data
        url = request.POST.get('url')
        size = request.POST.get('size')
        error_correction = request.POST.get('error_correction')
        style = request.POST.get('style')
        color_type = request.POST.get('color_type')
        color = request.POST.get('color')
        bg_color = request.POST.get('bg_color')
        gradient_start = request.POST.get('gradient_start')
        gradient_end = request.POST.get('gradient_end')
        gradient_direction = request.POST.get('gradient_direction')
        logo = request.FILES.get('logo')

        # Check Error-Correction
        match error_correction:
            case 'ERROR_CORRECT_L':
                error_correction = qrcode.constants.ERROR_CORRECT_L
            case 'ERROR_CORRECT_M':
                error_correction = qrcode.constants.ERROR_CORRECT_M
            case 'ERROR_CORRECT_Q':
                error_correction = qrcode.constants.ERROR_CORRECT_Q
            case 'ERROR_CORRECT_H':
                error_correction = qrcode.constants.ERROR_CORRECT_H

        # Create QrCode
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_correction,
            box_size=size,
            border=1,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Check Qrcode Style
        style_data = {}
        match style:
            case 'classic':
                style_data['module_drawer'] = SquareModuleDrawer()
            case 'gapped':
                style_data['module_drawer'] = GappedSquareModuleDrawer()
            case 'circle':
                style_data['module_drawer'] = CircleModuleDrawer()
            case 'rounded':
                style_data['module_drawer'] = RoundedModuleDrawer()
            case 'vertical':
                style_data['module_drawer'] = VerticalBarsDrawer()
            case 'horizontal':
                style_data['module_drawer'] = HorizontalBarsDrawer()

        # Check Color Type
        match color_type:
            case 'solid':
                style_data['color_mask'] = SolidFillColorMask(
                    back_color=webcolors.hex_to_rgb(bg_color),
                    front_color=webcolors.hex_to_rgb(color)
                )
            case 'gradient':
                match gradient_direction:
                    case 'radial':
                        style_data['color_mask'] = RadialGradiantColorMask(
                            center_color=webcolors.hex_to_rgb(gradient_start), edge_color=webcolors.hex_to_rgb(gradient_end)
                        )
                    case 'square':
                        style_data['color_mask'] = SquareGradiantColorMask(
                            center_color=webcolors.hex_to_rgb(gradient_start), edge_color=webcolors.hex_to_rgb(gradient_end)
                        )
                    case 'horizontal':
                        style_data['color_mask'] = HorizontalGradiantColorMask(
                            left_color=webcolors.hex_to_rgb(gradient_start), right_color=webcolors.hex_to_rgb(gradient_end)
                        )
                    case 'vertical':
                        style_data['color_mask'] = VerticalGradiantColorMask(
                            top_color=webcolors.hex_to_rgb(gradient_start), bottom_color=webcolors.hex_to_rgb(gradient_end)
                        )

        # Create QrCode
        qr_image = qr.make_image(image_factory=StyledPilImage, **style_data)

        # Save the image to media directory
        media_path = os.path.join(settings.MEDIA_ROOT, 'qrcodes')

        # Create directory if it doesn't exist
        if not os.path.exists(media_path):
            os.makedirs(media_path)

        # Generate unique filename
        filename = f"qr_{uuid.uuid4().hex}.png"
        file_path = os.path.join(media_path, filename)

        # Save the image
        qr_image.save(file_path)

        # Get the URL for the saved image
        image_url = f"{settings.MEDIA_URL}qrcodes/{filename}"

        if logo is not None:
            # Open images with Pillow
            background = Image.open(file_path).convert('RGBA')
            overlay = Image.open(logo).convert('RGBA')

            match size:
                case '10':
                    resized_overlay = overlay.resize((90, 90), Image.Resampling.LANCZOS)
                case '20':
                    resized_overlay = overlay.resize((160, 160), Image.Resampling.LANCZOS)
                case '30':
                    resized_overlay = overlay.resize((240, 240), Image.Resampling.LANCZOS)
                case _:
                    resized_overlay = overlay

            # Calculate position to center the overlay image
            bg_width, bg_height = background.size
            ol_width, ol_height = resized_overlay.size

            position = (
                (bg_width - ol_width) // 2,  # x coordinate
                (bg_height - ol_height) // 2  # y coordinate
            )

            # Create a transparent layer for the overlay
            transparent_overlay = Image.new('RGBA', background.size, (0, 0, 0, 0))

            # Paste the overlay onto the transparent layer using the overlay's alpha channel as mask
            transparent_overlay.paste(resized_overlay, position, resized_overlay)

            # Combine background with transparent overlay
            result = Image.alpha_composite(background, transparent_overlay)

            # Save the image
            result.save(file_path, format='PNG', quality=95)

        # Return result with query params
        base_url = reverse('qr-gen')
        params = {'created': True, 'image_url': image_url}
        query_string = urlencode(params)

        return redirect(f"{base_url}?{query_string}")


class Header(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'header.html')

    def post(self, request: HttpRequest, *args, **kwargs):
        return render(request, 'header.html')


class Footer(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'footer.html')

    def post(self, request: HttpRequest, *args, **kwargs):
        return render(request, 'footer.html')
