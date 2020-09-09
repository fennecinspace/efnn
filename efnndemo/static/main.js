function run(button, event) {
    event.preventDefault();
    event.stopPropagation();
    console.log(
        [...document.querySelectorAll('input[type="radio"]')].find(c => c.checked).value
    );
}

function selectSample(sample, event) {
    event.stopPropagation();
    sample.querySelector('input').click();
}