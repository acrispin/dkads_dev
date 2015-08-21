function numericValidator() {
    $(".numeric").numeric();
    $(".integer").numeric(false, function () {
        this.value = "";
        this.focus();
    });
    $(".positive").numeric({ negative: false }, function () {
        this.value = "";
        this.focus();
    });
    $(".positive-integer").numeric({ decimal: false, negative: false }, function () {
        this.value = "";
        this.focus();
    });
}

$(document).ready(function () {
    numericValidator();
});

