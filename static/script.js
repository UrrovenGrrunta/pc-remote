const buttons = document.querySelectorAll('[id$="-button"]');

buttons.forEach((button) => {
    button.onclick = () => {
        const appName = button.id.replace("-button", "");
        fetch(`/launch/${appName}`);
    };
});