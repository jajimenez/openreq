(() => {
    // Get all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll(".needs-validation");

    // Loop over the forms and prevent submission
    Array.from(forms).forEach((f) => {
        f.addEventListener("submit", (e) => {
            if (!f.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }

            f.classList.add("was-validated");
        }, false);
    });
})();
