const { ClassicLevel } = require("classic-level");

const path = require("path");
const hydraDbPath = path.join(
    process.env.APPDATA,
    "hydralauncher",
    "hydra-db-repair-test"
);

const db = new ClassicLevel(hydraDbPath, {
    valueEncoding: "json",
});

const gameDB = db.sublevel("games", {
    valueEncoding: "json",
});

async function main() {
    for await (const key of gameDB.keys({
        gte: "steam:2000000",
    })) {
        console.log(key);
    }
}

main();