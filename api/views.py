from qrcode.image.styledpil import StyledPilImage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from PIL import Image
import webcolors
import qrcode
import uuid
import os

from accounts.models import UserModel, QrCodeModel

from .serializers import CreateQrCodeSerializer

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


def validate_api_key(rq):
    api_key = rq.META.get("HTTP_X_API_KEY")
    response = Response()

    if api_key is None:
        response.data = {"result": False, "message": "Missing API_Key"}
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response, False, None

    # Check API_Key
    try:
        user = UserModel.objects.get(api_key=api_key)
    except UserModel.DoesNotExist:
        response.data = {"result": False, "message": "Invalid API_Key"}
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response, False, None

    return response, True, user


class QrGenAPIView(APIView):
    def post(self, request):
        response, result, user = validate_api_key(request)

        if not result:
            return response

        serializer = CreateQrCodeSerializer(data=request.data)

        # Validate Data
        if not serializer.is_valid():
            return Response(
                {"result": False, "massage": "Invalid Data", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Serializer Data
        url = serializer.validated_data.get("url")
        size = serializer.validated_data.get("size")
        error_correction = serializer.validated_data.get("error_correction")
        style = serializer.validated_data.get("style")
        color_type = serializer.validated_data.get("color_type")
        solid_color = serializer.validated_data.get("solid_color")
        gradient_start_color = serializer.validated_data.get("gradient_start_color")
        gradient_end_color = serializer.validated_data.get("gradient_end_color")
        gradient_direction = serializer.validated_data.get("gradient_direction")
        logo = serializer.validated_data.get("logo")
        saved = serializer.validated_data.get("saved")

        # Check Value Error-Correction User Sent
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
            Check color type : first check which type of color select and set suitable value for eche one,
            If gradient selected it have a gradient_direction that needs to be checked
        """
        match color_type:
            case "solid":
                style_data["color_mask"] = SolidFillColorMask(
                    front_color=webcolors.hex_to_rgb(solid_color),
                )
            case "gradient":
                match gradient_direction:
                    case "radial":
                        style_data["color_mask"] = RadialGradiantColorMask(
                            center_color=webcolors.hex_to_rgb(gradient_start_color),
                            edge_color=webcolors.hex_to_rgb(gradient_end_color),
                        )
                    case "square":
                        style_data["color_mask"] = SquareGradiantColorMask(
                            center_color=webcolors.hex_to_rgb(gradient_start_color),
                            edge_color=webcolors.hex_to_rgb(gradient_end_color),
                        )
                    case "horizontal":
                        style_data["color_mask"] = HorizontalGradiantColorMask(
                            left_color=webcolors.hex_to_rgb(gradient_start_color),
                            right_color=webcolors.hex_to_rgb(gradient_end_color),
                        )
                    case "vertical":
                        style_data["color_mask"] = VerticalGradiantColorMask(
                            top_color=webcolors.hex_to_rgb(gradient_start_color),
                            bottom_color=webcolors.hex_to_rgb(gradient_end_color),
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
        download_url = f"{settings.DEFAULT_DOMAIN}{image_url}"

        data = {"download_url": download_url}

        # Set A Logo On Center of QrCode ( If logo sent )
        if logo is not None:
            # Open Qrcode & Logo with Pillow
            background = Image.open(file_path).convert("RGBA")
            overlay = Image.open(logo).convert("RGBA")

            # Resize Logo ( To avoid ruining the photo, Check QrCode Size And Set A Suitable Size For Logo )
            match size:
                case 10:
                    resized_overlay = overlay.resize((90, 90), Image.Resampling.LANCZOS)
                case 20:
                    resized_overlay = overlay.resize(
                        (160, 160), Image.Resampling.LANCZOS
                    )
                case 30:
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

        if saved:
            # New Path For Move
            new_path = os.path.join(settings.MEDIA_ROOT, "qr_codes")
            new_file = os.path.join(new_path, filename)

            # Original Path
            old_path = os.path.join(settings.MEDIA_ROOT, "temporary")
            old_file = os.path.join(old_path, filename)

            # Move Qrcode
            os.rename(old_file, new_file)

            # New Url For Saving
            new_url = f"{settings.MEDIA_URL}qr_codes/{filename}"

            # Saving Qrcode
            qr_code = QrCodeModel.objects.create(user=user, qrcode=new_url)
            download_url = f"{settings.DEFAULT_DOMAIN}{new_url}"
            data["download_url"] = download_url
            data["qr_code_id"] = qr_code.id

        return Response(
            {"result": True, "massage": "QrCode Created", "data": [data]},
            status=status.HTTP_201_CREATED,
        )


class GetQrcodeAPIView(APIView):
    def get(self, request, qrcode_id):
        response, result, user = validate_api_key(request)

        if not result:
            return response

        try:
            qr_code = QrCodeModel.objects.get(id=qrcode_id)
        except QrCodeModel.DoesNotExist:
            return Response(
                {
                    "result": False,
                    "message": "QrCode does not exist",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        download_url = f"{settings.DEFAULT_DOMAIN}{qr_code.qrcode}"

        return Response(
            {
                "result": True,
                "message": "Successfully retrieved QrCode",
                "data": [{"download_url": download_url, "qr_code_id": qr_code.id}],
            }
        )


class UserQrCodeAPIView(APIView):
    def get(self, request):
        response, result, user = validate_api_key(request)

        if not result:
            return response

        qrcodes = QrCodeModel.objects.filter(user=user)

        data = []

        for item in qrcodes:
            data.append(
                {
                    "download_url": f"{settings.DEFAULT_DOMAIN}{item.qrcode}",
                    "qr_code_id": item.id,
                }
            )

        return Response(
            {"result": True, "message": "Successfully retrieved QrCodes", "data": data}
        )
