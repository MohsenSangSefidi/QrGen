# QRGen - Custom QR Code Generator

![QRGen](https://img.shields.io/badge/QRGen-Django%20QR%20Generator-blue)
![Python](https://img.shields.io/badge/Python-3.11%2B-green)
![Django](https://img.shields.io/badge/Django-5.5%2B-brightgreen)

A powerful Django-based web application for generating customized QR codes with advanced styling options and a comprehensive REST API.

## ✨ Features

- **Custom QR Code Generation**: Create QR codes with various styles and colors
- **Multiple Style Options**: Classic, gradient, and solid color styles
- **Error Correction**: Support for different error correction levels
- **Logo Integration**: Add custom logos to your QR codes
- **RESTful API**: Complete API for programmatic access
- **User Management**: Save and manage your generated QR codes
- **High Customization**: Control size, colors, and appearance

## 🚀 Quick Start

### Online Demo

- Visit At : https://qrgenpro.pythonanywhere.com/

### Prerequisites

- Python 3.11+
- Django 5.2+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/qrgen.git
   cd qrgen
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file**
    ```env
    EMAIL_HOST_USER=your-gmail@gamil.com
    EMAIL_HOST_PASSWORD=your-gemail-app-password
    DEFAULT_FROM_EMAIL=your-gmail@gamil.com
    DEFAULT_DOMAIN=http://localhost:8000 # For Run It Local don't change it
    ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Visit the application**
   ```
   http://localhost:8000
   ```

## 📖 API Documentation

### Authentication

All API endpoints require an `x-api-key` header for authentication. you can pick your api-key from dashboard.

```http
x-api-key: your_api_key_here
```

### Endpoints

#### See Full Documentation

- ApiDog : https://share.apidog.com/f461c568-8b5d-4f4b-b74b-13b15b27374a

#### 1. Create QR Code

**POST** `/api/create-qrcode/`

Creates a new customized QR code.

**Request Body:**
```json
{
  "url": "https://example.com",
  "size": 10, // choices [10, 20, 30]
  "error_correction": "ERROR_CORRECT_L", // choices ["ERROR_CORRECT_L", "ERROR_CORRECT_M", "ERROR_CORRECT_Q", "ERROR_CORRECT_H"]
  "style": "classic", // choices ["classic", "gapped", "circle", "rounded", "vertical", "horizontal"]
  "color_type": "solid", // choices ["solid", "gradient"]
  "solid_color": "#000000",
  "gradient_start_color": "#FF0000",
  "gradient_end_color": "#0000FF",
  "gradient_bg_color": "#FFFFFF",
  "gradient_direction": "radial", // choices ["radial", "square", "horizontal", "vertical",]
  "saved": true,
  "logo": "base64_encoded_image"
}
```

**Response:**
```json
{
  "result": true,
  "message": "QrCode Created",
  "data": [
    {
      "download_url": "http://localhost:8000/media/qr_codes/qr_1db6ceccfb1048a689d5b43a8a05ef4c.png",
      "qr_code_id": 21
    }
  ]
}
```

#### 2. Get QR Code

**GET** `/api/get-qrcode/{qrcode_id}`

Retrieves a specific QR code by ID.

**Response:**
```json
{
  "result": true,
  "message": "Successfully retrieved QrCode",
  "data": {
    "download_url": "http://localhost:8000/media/qr_codes/qr_ab272525bd5d4bc9a4cc6e746888f6fe.png",
    "qr_code_id": 20
  }
}
```

#### 3. User QR Codes

**GET** `/api/user-qrcodes/`

Retrieves all QR codes for the authenticated user.

**Response:**
```json
{
  "result": true,
  "message": "Successfully retrieved QrCodes",
  "data": [
    {
      "download_url": "http://localhost:8000/media/qr_codes/qr_1353d5243e4947e6b642836adf6ae5fd.png",
      "qr_code_id": 11
    }
  ]
}
```

### Error Responses

**Invalid API Key:**
```json
{
  "result": false,
  "message": "Invalid API_Key"
}
```

**Missing API Key:**
```json
{
  "result": false,
  "message": "Missing API_Key"
}
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django Framework
- QRCode library
- Pillow for image processing

---

**QRGen** - Generate beautiful, customized QR codes with ease! 🎯