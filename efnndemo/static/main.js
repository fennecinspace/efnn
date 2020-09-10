function run(button, event) {
    event.preventDefault();
    event.stopPropagation();

    let sample_name = [...document.querySelectorAll('input[type="radio"]')].find(c => c.checked).value;

    document.location = '/run/' + sample_name + '#results';

}

function selectSample(sample, event) {
    event.stopPropagation();
    sample.querySelector('input').click();
}