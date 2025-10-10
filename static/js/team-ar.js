document.addEventListener("DOMContentLoaded", () => {
    const arButton = document.getElementById("activate-ar");
    const overlay = document.getElementById("ar-overlay");
    const closeButton = document.getElementById("close-ar");
    const markers = document.querySelectorAll("a-marker[data-member]");
    const cards = document.querySelectorAll(".member-card");
    const scene = document.getElementById("team-ar-scene");

    const showOverlay = async () => {
        if (!overlay) return;
        overlay.classList.add("visible");
        try {
            if (overlay.requestFullscreen) {
                await overlay.requestFullscreen();
            }
        } catch (error) {
            console.warn("Fullscreen request was blocked:", error);
        }
    };

    const hideOverlay = () => {
        if (!overlay) return;
        overlay.classList.remove("visible");
        cards.forEach((card) => card.classList.remove("visible"));
        if (document.fullscreenElement && document.exitFullscreen) {
            document.exitFullscreen().catch(() => {});
        }
    };

    const showCard = (memberId) => {
        cards.forEach((card) => {
            if (card.dataset.member === memberId) {
                card.classList.add("visible");
            } else {
                card.classList.remove("visible");
            }
        });
    };

    const hideCard = (memberId) => {
        cards.forEach((card) => {
            if (card.dataset.member === memberId) {
                card.classList.remove("visible");
            }
        });
    };

    markers.forEach((marker) => {
        const memberId = marker.dataset.member;
        marker.addEventListener("markerFound", () => showCard(memberId));
        marker.addEventListener("markerLost", () => hideCard(memberId));
    });

    if (arButton) {
        arButton.addEventListener("click", showOverlay);
    }

    if (closeButton) {
        closeButton.addEventListener("click", hideOverlay);
    }

    if (scene) {
        scene.addEventListener("exit-vr", hideOverlay);
    }

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            hideOverlay();
        }
    });

    window.addEventListener("orientationchange", () => {
        if (!overlay?.classList.contains("visible")) {
            return;
        }
        // delay to allow layout settle
        setTimeout(() => {
            scene?.components?.arjs?.arController?.canvas?.style?.setProperty("width", "100%", "important");
        }, 250);
    });
});
