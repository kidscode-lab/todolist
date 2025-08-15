document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("taskModal");
    const openModalBtn = document.getElementById("openModal");
    const closeModalBtn = document.querySelector(".close");

    openModalBtn.addEventListener("click", function () {
        modal.style.display = "block";
    });

    closeModalBtn.addEventListener("click", function () {
        modal.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });

    const cc = document.getElementById("cc");
    const sid = document.getElementById("sid");
    const form = document.getElementById("identityForm");

    if (cc && sid && form) {
        // Prefill from localStorage when query params are missing
        const url = new URL(window.location.href);
        if (!url.searchParams.get("class_code") && localStorage.getItem("class_code")) {
        cc.value = localStorage.getItem("class_code");
        }
        if (!url.searchParams.get("student_id") && localStorage.getItem("student_id")) {
        sid.value = localStorage.getItem("student_id");
        }

        // Save on submit so the browser remembers next time
        form.addEventListener("submit", () => {
        localStorage.setItem("class_code", cc.value.trim());
        localStorage.setItem("student_id", sid.value.trim());
        });
    }
});
