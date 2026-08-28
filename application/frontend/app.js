const API_BASE =
    "http://portfolio-cms-alb-1990170921.us-west-1.elb.amazonaws.com";

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
