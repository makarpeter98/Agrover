/* =========================================================
   MOBILE MENU
   ========================================================= */

const menuButton =
    document.getElementById("mobile-menu-button");

const mainNav =
    document.getElementById("main-nav");


if (menuButton && mainNav)
{
    menuButton.addEventListener(
        "click",
        () =>
        {
            mainNav.classList.toggle("open");
        }
    );
}


/* =========================================================
   THEME
   ========================================================= */

const themeToggle =
    document.getElementById("theme-toggle");

const themeIcon =
    document.getElementById("theme-toggle-icon");

const themeLabel =
    document.getElementById("theme-toggle-label");


function applyTheme(theme)
{
    if (theme === "light")
    {
        document.body.classList.add("light-mode");

        if (themeIcon)
        {
            themeIcon.textContent = "☀";
        }

        if (themeLabel)
        {
            themeLabel.textContent = "LIGHT";
        }
    }
    else
    {
        document.body.classList.remove("light-mode");

        if (themeIcon)
        {
            themeIcon.textContent = "☾";
        }

        if (themeLabel)
        {
            themeLabel.textContent = "DARK";
        }
    }
}


/*
 * Previously selected theme.
 *
 * If nothing was saved yet,
 * dark mode is used.
 */

const savedTheme =
    localStorage.getItem("rover-theme") || "dark";

applyTheme(savedTheme);


if (themeToggle)
{
    themeToggle.addEventListener(
        "click",
        () =>
        {
            const newTheme =
                document.body.classList.contains("light-mode")
                    ? "dark"
                    : "light";

            localStorage.setItem(
                "rover-theme",
                newTheme
            );

            applyTheme(newTheme);
        }
    );
}

