/* ================================
   CONTACT PAGE JS
================================ */

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".contact-form");
    if (!form) return;

    form.addEventListener("submit", (e) => {
        const fields = form.querySelectorAll("input, textarea");
        let valid = true;

        fields.forEach(f => {
            if (!f.value.trim()) {
                f.style.borderColor = "#ef4444";
                valid = false;
            } else {
                f.style.borderColor = "";
            }
        });

        if (!valid) {
            e.preventDefault();
            showToast("Please fill in all fields.");
            return;
        }

        // Valid - let the form submit natively to POST /contact
    });
});

function showToast(message) {
    const toast = document.createElement("div");
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%);
        background: #8b6914;
        color: #fff;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        z-index: 9999;
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}
