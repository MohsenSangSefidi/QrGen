from django.core.validators import RegexValidator
from rest_framework import serializers


hex_color_validator = RegexValidator(
    regex=r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3}|[A-Fa-f0-9]{8}|[A-Fa-f0-9]{4})$",
    message="Enter a valid hex color code (e.g., #RRGGBB, #RGB, #RRGGBBAA, #RGBA)",
    code="invalid_hex_color",
)


class CreateQrCodeSerializer(serializers.Serializer):
    size_choices = ((10, 10), (20, 20), (30, 30))
    error_correction_choices = (
        ("ERROR_CORRECT_L", "ERROR_CORRECT_L"),
        ("ERROR_CORRECT_M", "ERROR_CORRECT_M"),
        ("ERROR_CORRECT_Q", "ERROR_CORRECT_Q"),
        ("ERROR_CORRECT_H", "ERROR_CORRECT_H"),
    )
    style_choices = (
        ("classic", "classic"),
        ("gapped", "gapped"),
        ("circle", "circle"),
        ("rounded", "rounded"),
        ("vertical", "vertical"),
        ("horizontal", "horizontal"),
    )
    color_type_choices = (("solid", "solid"), ("gradient", "gradient"))
    gradient_direction_choices = (
        ("radial", "radial"),
        ("square", "square"),
        ("horizontal", "horizontal"),
        ("vertical", "vertical"),
    )

    url = serializers.URLField()
    size = serializers.ChoiceField(choices=size_choices)
    error_correction = serializers.ChoiceField(choices=error_correction_choices)
    style = serializers.ChoiceField(choices=style_choices)
    color_type = serializers.ChoiceField(choices=color_type_choices)
    solid_color = serializers.CharField(
        required=False, validators=[hex_color_validator]
    )
    gradient_start_color = serializers.CharField(
        required=False, validators=[hex_color_validator]
    )
    gradient_end_color = serializers.CharField(
        required=False, validators=[hex_color_validator]
    )
    gradient_direction = serializers.ChoiceField(
        choices=gradient_direction_choices, required=False
    )
    saved = serializers.BooleanField(default=False)
    logo = serializers.ImageField(required=False)

    def validate(self, data):
        color_type = data.get("color_type")
        solid_color = data.get("solid_color")
        gradient_start_color = data.get("gradient_start_color")
        gradient_end_color = data.get("gradient_end_color")
        gradient_direction = data.get("gradient_direction")

        if color_type == "solid":
            if solid_color is None:
                raise serializers.ValidationError(
                    "When color_type Is solid, solid_color Must Be Send"
                )

        if color_type == "gradient":
            if gradient_start_color is None:
                raise serializers.ValidationError(
                    "When color_type Is gradient, gradient_start_color Must Be Send"
                )
            elif gradient_end_color is None:
                raise serializers.ValidationError(
                    "When color_type Is gradient, gradient_end_color Must Be Send"
                )
            elif gradient_direction is None:
                raise serializers.ValidationError(
                    "When color_type Is gradient, gradient_direction Must Be Send"
                )

        return data
