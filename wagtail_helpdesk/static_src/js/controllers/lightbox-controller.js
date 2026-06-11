import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
    static targets = ["overlay", "image", "caption"];

    open(event) {
        // log if loaded
        console.log("Lightbox script opened");
        const trigger = event.currentTarget;
        const imageUrl = trigger.dataset.lightboxImageUrl;
        const caption = trigger.dataset.lightboxCaption || "";

        this.imageTarget.src = imageUrl;
        this.imageTarget.alt = caption || "Vergrote afbeelding";
        this.captionTarget.textContent = caption;

        this.overlayTarget.hidden = false;
        document.body.classList.add("is-lightbox-open");
    }

    close(event) {
        if (event) {
            event.preventDefault();
            event.stopPropagation();
        }

        this.overlayTarget.hidden = true;

        setTimeout(() => {
            this.imageTarget.src = "";
            this.captionTarget.textContent = "";
            document.body.classList.remove("is-lightbox-open");
        }, 0);
    }

    stop(event) {
        event.stopPropagation();
    }

    closeOnBackdrop(event) {
        if (event.target === this.overlayTarget) {
            this.close();
        }
    }

    closeOnEscape(event) {
        if (event.key === "Escape" && !this.overlayTarget.hidden) {
            this.close();
        }
    }

    connect() {
        this.closeOnEscape = this.closeOnEscape.bind(this);
        document.addEventListener("keydown", this.closeOnEscape);
    }

    disconnect() {
        document.removeEventListener("keydown", this.closeOnEscape);
    }
}
