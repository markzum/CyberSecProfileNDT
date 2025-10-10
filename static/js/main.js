document.addEventListener("DOMContentLoaded", () => {
    const nav = document.querySelector(".main-nav");
    const toggle = document.querySelector(".nav-toggle");

    if (toggle && nav) {
        toggle.addEventListener("click", () => {
            nav.classList.toggle("open");
            toggle.classList.toggle("open");
        });
    }

    // Subtle parallax effect on hero visual
    const orbital = document.querySelector(".orbital-grid");
    const codeRain = document.querySelector(".code-rain");

    if (orbital && codeRain) {
        window.addEventListener("mousemove", (event) => {
            const { innerWidth, innerHeight } = window;
            const offsetX = (event.clientX / innerWidth - 0.5) * 16;
            const offsetY = (event.clientY / innerHeight - 0.5) * 16;
            orbital.style.transform = `translate3d(${offsetX}px, ${offsetY}px, 0)`;
            codeRain.style.transform = `translate3d(${offsetX * 0.6}px, ${offsetY * 0.6}px, 0)`;
        });
    }
});
