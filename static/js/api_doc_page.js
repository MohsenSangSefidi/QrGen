document.addEventListener('DOMContentLoaded', function () {
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

    // Simple syntax highlighting
    document.querySelectorAll('.hljs.json').forEach(block => {
        const text = block.textContent;
        // This is a simplified syntax highlighter for JSON
        block.innerHTML = text
            .replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
                function (match) {
                    let cls = 'hljs-number';
                    if (/^"/.test(match)) {
                        if (/:$/.test(match)) {
                            cls = 'hljs-attr';
                        } else {
                            cls = 'hljs-string';
                        }
                    } else if (/true|false/.test(match)) {
                        cls = 'hljs-literal';
                    } else if (/null/.test(match)) {
                        cls = 'hljs-keyword';
                    }
                    return '<span class="' + cls + '">' + match + '</span>';
                });
    });
});
