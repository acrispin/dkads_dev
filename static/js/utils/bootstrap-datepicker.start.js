$(document).ready(function () {
    $.fn.datepicker.dates['es'] = {
        days: ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
        daysShort: ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
        daysMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"],
        months: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
        monthsShort: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
        today: "Hoy"
    };

    $('.datepicker').datepicker({
        format: "dd/mm/yyyy",
        weekStart: 1,
        todayBtn: "linked",
        language: "es",
        autoclose: true
    });

    $('.datepickerperiod').datepicker({
        format: "yyyymm",
        endDate: "null",
        minViewMode: 1,
        todayBtn: true,
        language: "es",
        autoclose: false
    });

    $('.datepickeryear').datepicker({
        format: "yyyy",
        endDate: "null",
        minViewMode: 2,
        todayBtn: true,
        language: "es",
        autoclose: true
    });
});