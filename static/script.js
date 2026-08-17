const steamGames = document.getElementById("steam-games");

fetch("/apps")
    .then(response => response.json())
    .then(apps => {
        for (const app of apps) {
            const gameCard = document.createElement("button");
            gameCard.classList.add("game-card");
            const gameImage = document.createElement("img");
            const gameName = document.createElement("span");

            gameName.textContent = app.name;
            gameImage.src = app.image;

            gameCard.appendChild(gameImage);
            gameCard.appendChild(gameName);

            steamGames.appendChild(gameCard);

            gameCard.addEventListener("click", () => {
                fetch(`/launch/${app.id}`);
            })
        }
    });

