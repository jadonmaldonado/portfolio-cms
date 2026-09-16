const API_BASE = "https://api.jadonmaldonado.com";

async function loadAbout() {
    try {
        const response = await fetch(`${API_BASE}/api/about`);

        if (!response.ok) {
            throw new Error(`API returned ${response.status}`);
        }

        const data = await response.json();

        if (data.name) {
            document.getElementById("portfolio-name").textContent = data.name;
        }

        if (data.headline) {
            document.getElementById("portfolio-headline").textContent =
                data.headline;
        }

        if (data.about) {
            document.getElementById("portfolio-about").textContent = data.about;
        }
    } catch (error) {
        console.error("Unable to load portfolio content:", error);
    }
}

loadAbout();
loadCertifications();

async function loadCertifications() {
    try {
        const response = await fetch(`${API_BASE}/api/certifications`);

        if (!response.ok) {
            throw new Error(`API returned ${response.status}`);
        }

        const certifications = await response.json();

        if (certifications.length === 0) {
            return;
        }

        const list = document.getElementById("certifications-list");
        list.innerHTML = "";

        certifications.forEach((certification) => {
            const item = document.createElement("li");

            item.appendChild(
                document.createTextNode(
                    `${certification.name} — ${certification.issuer} `
                )
            );

            if (certification.credential_url) {
                const link = document.createElement("a");
                link.href = certification.credential_url;
                link.target = "_blank";
                link.rel = "noopener noreferrer";
                link.textContent = "View Credential";
                item.appendChild(link);
            }

            list.appendChild(item);
        });
    } catch (error) {
        console.error("Unable to load certifications:", error);
    }
}