document.addEventListener('DOMContentLoaded', function () {
    // Color picker synchronization
    const qrColor = document.getElementById('qrColor');
    const qrColorText = document.getElementById('qrColorText');
    const qrBgColor = document.getElementById('qrBgColor');
    const qrBgColorText = document.getElementById('qrBgColorText');
    const gradientStart = document.getElementById('gradientStart');
    const gradientStartText = document.getElementById('gradientStartText');
    const gradientEnd = document.getElementById('gradientEnd');
    const gradientEndText = document.getElementById('gradientEndText');

    // Sync color inputs with text inputs
    function syncColorInputs(colorInput, textInput) {
        colorInput.addEventListener('input', function () {
            textInput.value = this.value;
        });

        textInput.addEventListener('input', function () {
            if (/^#[0-9A-F]{6}$/i.test(this.value)) {
                colorInput.value = this.value;
            }
        });
    }

    syncColorInputs(qrColor, qrColorText);
    syncColorInputs(gradientStart, gradientStartText);
    syncColorInputs(gradientEnd, gradientEndText);

    // Toggle between solid and gradient color options
    const solidColorOption = document.getElementById('solidColor');
    const gradientColorOption = document.getElementById('gradientColor');
    const solidColorControls = document.getElementById('solidColorControls');
    const gradientColorControls = document.getElementById('gradientColorControls');

    solidColorOption.addEventListener('change', function () {
        if (this.checked) {
            solidColorControls.style.display = 'block';
            gradientColorControls.style.display = 'none';
        }
    });

    gradientColorOption.addEventListener('change', function () {
        if (this.checked) {
            solidColorControls.style.display = 'none';
            gradientColorControls.style.display = 'block';
        }
    });

    // File upload display
    const fileInput = document.getElementById('logoUpload');
    const fileName = document.getElementById('fileName');

    fileInput.addEventListener('change', function () {
        if (this.files.length > 0) {
            fileName.textContent = this.files[0].name;
        } else {
            fileName.textContent = 'No file chosen';
        }
    });

    // Style selection
    const stylesGrid = document.getElementById('stylesGrid');
    const styles = [
        {id: 'classic', name: 'Classic', icon: 'fas fa-qrcode'},
        {id: 'gapped', name: 'Gapped', icon: 'fas fa-paint-brush'},
        {id: 'circle', name: 'Circle', icon: 'fas fa-dot-circle'},
        {id: 'rounded', name: 'Rounded', icon: 'fas fa-image'},
        {id: 'vertical', name: 'Vertical Bars', icon: 'fas fa-shapes'},
        {id: 'horizontal', name: 'Horizontal Bars', icon: 'fas fa-gem'}
    ];
    let style_input = document.getElementById('style-input');

    // Populate style options
    styles.forEach(style => {
        const styleOption = document.createElement('div');
        styleOption.className = 'style-option';
        styleOption.dataset.style = style.id;
        styleOption.innerHTML = `
            <div class="style-preview">
                <i class="${style.icon}"></i>
            </div>
            <div class="style-label">${style.name}</div>
        `;

        styleOption.addEventListener('click', function () {
            // Remove selected class from all options
            document.querySelectorAll('.style-option').forEach(opt => {
                opt.classList.remove('selected');
            });

            // Add selected class to clicked option
            this.classList.add('selected');
            style_input.value = this.dataset.style
        });

        stylesGrid.appendChild(styleOption);
    });

    // Select first style by default
    if (stylesGrid.firstChild) {
        stylesGrid.firstChild.classList.add('selected');
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});