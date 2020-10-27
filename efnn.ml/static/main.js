function run(button, event) {
    event.preventDefault();
    event.stopPropagation();

    let sample_name = [...document.querySelectorAll('input[type="radio"]')].find(c => c.checked).value;

    document.querySelector('.loading_overlay').style.display = 'grid';

    document.location = '/run/' + sample_name + '#results';

}

function selectSample(sample, event) {
    event.stopPropagation();
    sample.querySelector('input').click();
}

function upload(elem, event) {
    event.preventDefault();
    files = document.querySelectorAll('input[type="file"]');

    for(let i = 0; i < files.length; i++) {
        if (files[i].files.length == 0) {
            alert("You must select all 3 exposures before upload");
            return;
        }
    }

    var fd = new FormData();
    fd.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
    fd.append('under', files[0].files[0]);
    fd.append('normal', files[1].files[0]);
    fd.append('over', files[2].files[0]);

    // var fd = new FormData(elem.parentElement);

    document.querySelector('.loading_overlay').style.display = 'grid';

    $.ajax({
        url: '/upload/',
        type: 'post',
        data: fd,
        cache: false,
        contentType: false,
        processData: false,
        success: function(res){
            console.log(res);

            document.location = '/run/' + res.sample_name + '#results';
        },
        error: function () {
            document.querySelector('.loading_overlay').style.display = 'none';
        }
    });
}