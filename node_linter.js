// node_linter.js
// Reads JS code from stdin, lints/fixes using ESLint, outputs fixed code

const { ESLint } = require("eslint");

async function main() {
    let input = "";

    process.stdin.on("data", chunk => {
        input += chunk;
    });

    process.stdin.on("end", async () => {
        try {
            const eslint = new ESLint({ fix: true });
            const results = await eslint.lintText(input);
            await ESLint.outputFixes(results);
            const fixed = results[0].output || input;
            process.stdout.write(fixed);
        } catch (err) {
            console.error(err);
            process.stdout.write(input); // fallback
        }
    });

    process.stdin.resume();
}

main();
