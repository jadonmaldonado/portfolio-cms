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

async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE}/api/projects`);

        if (!response.ok) {
            throw new Error(`API returned ${response.status}`);
        }

        const projects = await response.json();

        if (projects.length === 0) {
            return;
        }

        const container = document.getElementById("projects-list");
        container.innerHTML = "";

        projects.forEach((project) => {
            const article = document.createElement("article");

            const title = document.createElement("h3");
            title.textContent = project.title;
            article.appendChild(title);

            if (project.description) {
                const description = document.createElement("p");
                description.textContent = project.description;
                article.appendChild(description);
            }

            if (project.tech_stack) {
                const tech = document.createElement("p");
                tech.textContent = `Tech: ${project.tech_stack}`;
                article.appendChild(tech);
            }

            if (project.status) {
                const status = document.createElement("p");
                status.textContent = `Status: ${project.status}`;
                article.appendChild(status);
            }

            if (project.github) {
                const link = document.createElement("a");
                link.href = project.github;
                link.target = "_blank";
                link.rel = "noopener noreferrer";
                link.textContent = "View on GitHub";
                article.appendChild(link);
            }

            container.appendChild(article);
        });
    } catch (error) {
        console.error("Unable to load projects:", error);
    }
}

loadAbout();
loadCertifications();
loadProjects();