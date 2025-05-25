function getCSRFToken() {
    let cookieValue = null;
    const name = "csrftoken";
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split("; ");
        for (let cookie of cookies) {
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.split("=")[1]);
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", () => {
    const steps = document.querySelectorAll(".form-step");
    const nextBtns = document.querySelectorAll(".next-btn");
    const form = document.getElementById("lead-form");
    const responseMsg = document.getElementById("response-message");

    let currentStep = 0;

    // Schrittwechsel
    nextBtns.forEach((btn, index) => {
        btn.addEventListener("click", () => {
            if (validateStep(steps[index])) {
                steps[index].classList.remove("active");
                steps[index + 1].classList.add("active");
                currentStep++;
            }
        });
    });

    // Laden der Unterkategorien bei Auswahl der Hauptkategorie
    const mainCategorySelect = document.getElementById("main_category");
    const subcategorySelect = document.getElementById("subcategory");

    mainCategorySelect.addEventListener("change", () => {
        const categoryId = mainCategorySelect.value;
        console.log("Ausgewählte Kategorie ID:", categoryId);
        if (!categoryId) return;

        fetch(`/get-subcategories/${categoryId}/`)
            .then(response => response.json())
            .then(data => {
                subcategorySelect.innerHTML = '<option value="">Unterkategorie auswählen</option>';
                data.subcategories.forEach(sub => {
                    const option = document.createElement("option");
                    option.value = sub.id;
                    option.textContent = sub.name;
                    subcategorySelect.appendChild(option);
                });
            })
            .catch(error => console.error("Fehler beim Laden der Unterkategorien:", error));
    });

    // Formular absenden
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const formData = {
            main_category: mainCategorySelect.value,
            subcategory: subcategorySelect.value,
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            phone: document.getElementById("phone").value
        };

        fetch("/submit-lead/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify(formData)
        })
        .then(res => res.json())
        .then(data => {
//            window.scrollTo({top: 0, behavior: "smooth"});
//            document.activeElement.blur();
            responseMsg.textContent = data.message || "Formular erfolgreich gesendet!";
            setTimeout(() => {
                location.reload();
            }, 1000);
            form.reset();
            steps.forEach(step => step.classList.remove("active"));
            steps[0].classList.add("active");

        })
        .catch(err => {
            responseMsg.textContent = "Fehler beim Absenden. Bitte versuchen Sie es später erneut.";
            console.error("Fehler:", err);
        });
    });

    // Überprüfung der Eingaben im aktuellen Schritt
    function validateStep(step) {
        const inputs = step.querySelectorAll("select, input");
        for (let input of inputs) {
            if (!input.checkValidity()) {
                input.reportValidity();
                return false;
            }
        }
        return true;
    }

    // CSRF-Token abrufen
    function getCSRFToken() {
        let cookieValue = null;
        const name = "csrftoken";
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split("; ");
            for (let cookie of cookies) {
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.split("=")[1]);
                    break;
                }
            }
        }
        return cookieValue;
    }
});
