from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from qrcode.image.styledpil import StyledPilImage
from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.conf import settings
from django.urls import reverse
from django.views import View
from PIL import Image

import qrcode, webcolors, uuid, os

from qrcode.image.styles.moduledrawers.pil import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer,
)

from qrcode.image.styles.colormasks import (
    SolidFillColorMask,
    RadialGradiantColorMask,
    SquareGradiantColorMask,
    HorizontalGradiantColorMask,
    VerticalGradiantColorMask,
)

from accounts.models import QrCodeModel


class QrGenView(View):
    def get(self, request, *args, **kwargs):
        # Query Params
        # ( For showing download box useing query params )
        created = request.GET.get("created")
        image_url = request.GET.get("image_url")
        filename = request.GET.get("filename")
        saved = request.GET.get("saved")

        return render(
            request,
            "home_page.html",
            {
                "created": created,
                "image_url": image_url,
                "saved": saved,
                "filename": filename,
            },
        )

    def post(self, request, *args, **kwargs):
        data = request.POST

        # Getting Data From Html Form
        url = request.POST.get("url")
        size = request.POST.get("size")
        error_correction = request.POST.get("error_correction")
        style = request.POST.get("style")
        color_type = request.POST.get("color_type")
        color = request.POST.get("color")
        bg_color = request.POST.get("bg_color")
        gradient_start = request.POST.get("gradient_start")
        gradient_end = request.POST.get("gradient_end")
        gradient_direction = request.POST.get("gradient_direction")
        logo = request.FILES.get("logo")

        # Check Valua Error-Correction User Sent
        match error_correction:
            case "ERROR_CORRECT_L":
                error_correction = qrcode.constants.ERROR_CORRECT_L
            case "ERROR_CORRECT_M":
                error_correction = qrcode.constants.ERROR_CORRECT_M
            case "ERROR_CORRECT_Q":
                error_correction = qrcode.constants.ERROR_CORRECT_Q
            case "ERROR_CORRECT_H":
                error_correction = qrcode.constants.ERROR_CORRECT_H

        # Create QrCode And Add Url
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
            case "classic":
                style_data["module_drawer"] = SquareModuleDrawer()
            case "gapped":
                style_data["module_drawer"] = GappedSquareModuleDrawer()
            case "circle":
                style_data["module_drawer"] = CircleModuleDrawer()
            case "rounded":
                style_data["module_drawer"] = RoundedModuleDrawer()
            case "vertical":
                style_data["module_drawer"] = VerticalBarsDrawer()
            case "horizontal":
                style_data["module_drawer"] = HorizontalBarsDrawer()

        """
            Check color type : first check wich type of color select and set suitable value for eche one,
            If gradient selected it have a gradient_direction that needs to be checked
        """
        match color_type:
            case "solid":
                style_data["color_mask"] = SolidFillColorMask(
                    back_color=webcolors.hex_to_rgb(bg_color),
                    front_color=webcolors.hex_to_rgb(color),
                )
            case "gradient":
                match gradient_direction:
                    case "radial":
                        style_data["color_mask"] = RadialGradiantColorMask(
                            center_color=webcolors.hex_to_rgb(gradient_start),
                            edge_color=webcolors.hex_to_rgb(gradient_end),
                        )
                    case "square":
                        style_data["color_mask"] = SquareGradiantColorMask(
                            center_color=webcolors.hex_to_rgb(gradient_start),
                            edge_color=webcolors.hex_to_rgb(gradient_end),
                        )
                    case "horizontal":
                        style_data["color_mask"] = HorizontalGradiantColorMask(
                            left_color=webcolors.hex_to_rgb(gradient_start),
                            right_color=webcolors.hex_to_rgb(gradient_end),
                        )
                    case "vertical":
                        style_data["color_mask"] = VerticalGradiantColorMask(
                            top_color=webcolors.hex_to_rgb(gradient_start),
                            bottom_color=webcolors.hex_to_rgb(gradient_end),
                        )

        # Create QrCode
        qr_image = qr.make_image(image_factory=StyledPilImage, **style_data)

        # Media path for saving qrcode temporary
        media_path = os.path.join(settings.MEDIA_ROOT, "temporary")

        # Create directory if it doesn't exist
        if not os.path.exists(media_path):
            os.makedirs(media_path)

        # Generate unique filename and path
        filename = f"qr_{uuid.uuid4().hex}.png"
        file_path = os.path.join(media_path, filename)

        # Save the qrcode
        qr_image.save(file_path)

        # Qrcode url for showing on page and downloading
        image_url = f"{settings.MEDIA_URL}temporary/{filename}"

        # Set A Logo On Center of QrCode ( If logo sent )
        if logo is not None:
            # Open Qrcode & Logo with Pillow
            background = Image.open(file_path).convert("RGBA")
            overlay = Image.open(logo).convert("RGBA")

            # Resize Logo ( To avoid ruining the photo, Check QrCode Size And Set A Suitable Size For Logo )
            match size:
                case "10":
                    resized_overlay = overlay.resize((90, 90), Image.Resampling.LANCZOS)
                case "20":
                    resized_overlay = overlay.resize(
                        (160, 160), Image.Resampling.LANCZOS
                    )
                case "30":
                    resized_overlay = overlay.resize(
                        (240, 240), Image.Resampling.LANCZOS
                    )
                case _:
                    resized_overlay = overlay

            # Calculate position to center the logo
            bg_width, bg_height = background.size
            ol_width, ol_height = resized_overlay.size

            position = (
                (bg_width - ol_width) // 2,  # x coordinate
                (bg_height - ol_height) // 2,  # y coordinate
            )

            # Create a transparent layer for the overlay. to remove the of logo
            transparent_overlay = Image.new("RGBA", background.size, (0, 0, 0, 0))

            # Paste the logo onto the transparent layer using the overlay's alpha channel as mask
            transparent_overlay.paste(resized_overlay, position, resized_overlay)

            # Combine background with transparent logo
            qr_image = Image.alpha_composite(background, transparent_overlay)

            # Save the image
            qr_image.save(file_path, format="PNG", quality=95)

        # Return result with query params
        base_url = reverse("qr-gen")
        params = {"created": True, "image_url": image_url, "filename": filename}
        query_string = urlencode(params)

        return redirect(f"{base_url}?{query_string}")


@method_decorator(login_required, name="dispatch")
class SaveQRCodeView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        # Get Data From Query Params
        filename = request.GET.get("filename")
        image_url = request.GET.get("image_url")

        """
            Move the qrcode to qr_code dir to avoid deleting that
        """
        # New Path For Move
        new_path = os.path.join(settings.MEDIA_ROOT, "qr_codes")
        new_file = os.path.join(new_path, filename)

        # Orginal Path
        old_path = os.path.join(settings.MEDIA_ROOT, "temporary")
        old_file = os.path.join(old_path, filename)

        # Move Qrcode
        os.rename(old_file, new_file)

        # New Url For Saving
        new_url = f"{settings.MEDIA_URL}qr_codes/{filename}"

        # Saving Qrcode
        qr_code = QrCodeModel.objects.create(user=user, qrcode=new_url)

        # Return To Home Page
        base_url = reverse("qr-gen")
        params = {"saved": True, "created": True, "image_url": new_url}
        query_string = urlencode(params)

        return redirect(f"{base_url}?{query_string}")
