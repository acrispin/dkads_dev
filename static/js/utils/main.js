
var timerTemClassId = 0;
var main_ns = {};
main_ns.SELECTOR = null;

///////////////// utils methods

main_ns.msgError = function (message, selector) {    
    var alertify = main_ns.getModule("alertify");
    $("#alertify-logs").html("");
    alertify.error(message);
};


main_ns.msgInfo = function (message, selector) {
    var alertify = main_ns.getModule("alertify");
    $("#alertify-logs").html("");
    alertify.log(message);
};

main_ns.msgSuccess = function (message, selector) {
    var alertify = main_ns.getModule("alertify");
    $("#alertify-logs").html("");
    alertify.success(message);
};

main_ns.getParameterByName = function (name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(document.location.href);
    if (results == null)
        return "";
    else
        return decodeURIComponent(results[1].replace(/\+/g, " "));
};

main_ns.removeURLParameter = function (parameter) {
    var url = document.location.href;
    var urlparts = url.split('?');
    if (urlparts.length >= 2) {

        var prefix = encodeURIComponent(parameter) + '=';
        var pars = urlparts[1].split(/[&;]/g);

        for (var i = pars.length; i-- > 0;) {
            if (pars[i].lastIndexOf(prefix, 0) !== -1) {
                pars.splice(i, 1);
            }
        }

        url = urlparts[0] + '?' + pars.join('&');
        return url;
    } else {
        return url;
    }
};

main_ns.VerifyBrowserSupportInputByType = function (value) {
    var i = document.createElement("input");
    i.setAttribute("type", value);
    return i.type !== "text";
};

main_ns.getInternetExplorerVersion = function () {
    var rv = -1; // Return value assumes failure.
    if (navigator.appName == 'Microsoft Internet Explorer') {
        var ua = navigator.userAgent;
        var re = new RegExp("MSIE ([0-9]{1,}[\.0-9]{0,})");
        if (re.exec(ua) != null)
            rv = parseFloat(RegExp.$1);
    }
    return rv;
};

main_ns.checkVersion = function () {
    var msg = "You're not using Internet Explorer.";
    var ver = main_ns.getInternetExplorerVersion();

    if (ver > -1) {
        if (ver >= 6.0)
            msg = "You're using a recent copy of Internet Explorer."
        else
            msg = "You should upgrade your copy of Internet Explorer.";
    }
    alert(msg);
};

main_ns.endsWith = function (str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
};

main_ns.countProperties = function (obj) {
    if (main_ns.getInternetExplorerVersion() == -1) {
        return Object.keys(obj).length;
    }
    else {
        var count = 0;
        for (var k in obj) {
            if (obj.hasOwnProperty(k)) {
                ++count;
            }
        }
        return count;
    }
};

main_ns.getFileName = function (path_file) {
    var reg = new RegExp(/([^\/\\]+)$/);
    var result = reg.exec(path_file);
    return result != null ? result[0] : result;
};

main_ns.getFileSizeMB = function (id) {
    try {
        var fileSize = 0;
        var scale = 1048576; // 1024*1024
        if (main_ns.getInternetExplorerVersion() > -1 && main_ns.getInternetExplorerVersion() <= 9) {
            fileSize = 2;
        }
        else
            if (main_ns.getInternetExplorerVersion() > 9) {
                var objFSO = new ActiveXObject("Scripting.FileSystemObject");
                var filePath = $("#" + id)[0].value;
                var objFile = objFSO.getFile(filePath);
                if (typeof (objFile) !== "undefined") fileSize = objFile.size / scale;
                //fileSize = 1000;
            }
            else {
            if (typeof ($("#" + id)[0].files[0]) !== "undefined") fileSize = $("#" + id)[0].files[0].size / scale;
        }

        return fileSize;
    }
    catch (e) {
        console.log("Error en obtener el tamaño del archivo :" + e);
        return 0;
    }
};

main_ns.getCookie = function (name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    //return r ? r[1] : undefined;
    return r ? r[1] : "";
};

main_ns.createCookie = function (name, value, days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        var expires = "; expires=" + date.toGMTString();
    }
    else var expires = "";
    document.cookie = name + "=" + value + expires + "; path=/";
};

main_ns.readCookie = function (name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
};

main_ns.deleteCookie = function (name) {
    main_ns.createCookie(name, "", -1);
};

main_ns.getPeriod = function (date) {
    try {
        return date.getFullYear() + "" + (("" + (date.getMonth() + 1)).length == 1 ? "0" + (date.getMonth() + 1) : "" + (date.getMonth() + 1));
    } catch (e) {
        console.log(e);
        return "";
    }
};

main_ns.getCurrentPeriod = function () {
    var date = new Date();
    return main_ns.getPeriod(date);
};

main_ns.renderTemplate = function (_selector, _template, data) {
    $(_selector).html("");
    var templatehtml = $(_template).html();
    var sourcehtml = Handlebars.compile(templatehtml);
    $(_selector).html(sourcehtml({ ListData: data }));
};

main_ns.renderTemplateGen = function (_selector, _template, _context) {
    $(_selector).html("");
    var templatehtml = $(_template).html();
    var sourcehtml = Handlebars.compile(templatehtml);
    $(_selector).html(sourcehtml(_context));
};

main_ns.getTemplate = function (_template, _context) {
    var templatehtml = $(_template).html();
    var sourcehtml = Handlebars.compile(templatehtml);
    return sourcehtml(_context);
};

main_ns.validateEmail = function (_email, _re) {
    return _re.test(_email);
};

// dates utils
main_ns.addMonthToDate = function(date, months){
    date.setMonth(date.getMonth() + months);
    return date
};

Date.prototype.formatDDMMYYYY = function () {
    return (("" + this.getDate()).length == 1 ? "0" + (this.getDate()) : (this.getDate())) +
            "/" + (("" + (this.getMonth() + 1)).length == 1 ? "0" + (this.getMonth() + 1) : (this.getMonth() + 1)) +
            "/" + this.getFullYear();
}

Date.prototype.formatDDMMYYYY2 = function () {
    return (("" + this.getDate()).length == 1 ? "0" + (this.getDate()) : (this.getDate())) +
            "-" + (("" + (this.getMonth() + 1)).length == 1 ? "0" + (this.getMonth() + 1) : (this.getMonth() + 1)) +
            "-" + this.getFullYear();
}

Date.prototype.formatDDMMYYYY3 = function () {
    return (("" + this.getDate()).length == 1 ? "0" + (this.getDate()) : (this.getDate())) +
            "-" + (("" + (this.getMonth() + 1)).length == 1 ? "0" + (this.getMonth() + 1) : (this.getMonth() + 1)) +
            "-" + (this.getFullYear() + "").substr(2, 2);
}

Date.prototype.formatYYYYMMDD = function () {
    return this.getFullYear() +
        "-" + (("" + (this.getMonth() + 1)).length == 1 ? "0" + (this.getMonth() + 1) : (this.getMonth() + 1)) +
        "-" + (("" + this.getDate()).length == 1 ? "0" + (this.getDate()) : (this.getDate()));
}

if (!String.prototype.format) {
    String.prototype.format = function () {
        var args = arguments;
        return this.replace(/\{(\d+)\}/g, function (match, number) {
            return typeof args[number] != 'undefined' ? args[number] : match;
        });
    };
}

if (typeof String.prototype.trim !== 'function') {
    String.prototype.trim = function () {
        return this.replace(/^\s+|\s+$/g, '');
    }
}

(function ($) {

    $.fn.extend({

        addTempClass: function (className, duration) {
            var elements = this;
            timerTemClassId = setTimeout(function () {
                elements.removeClass(className);
            }, duration);

            return this.each(function () {
                $(this).addClass(className);
            });
        }
    });

})(jQuery);

////////////////

$("#imgLogo").on("click", function () {
    if ($('.navbar-collapse').hasClass('in')) {
        $('.navbar-collapse').collapse('hide');
    }
});

$(document).on("click", "#btnLanguage", function () {
    var lang = $(this).attr("data-lang") == "es" ? "en" : "es";
    i18n_ns.setLang(lang, true);
    location.reload();
});

$(document).on("focusout", ".has-error", function () {
    $(this).removeClass('has-error');
    $(this).children('input').attr('placeholder', '');
});

main_ns.validateInput = function (selector, type) {
    if (type === "email") {
        if ($("#" + selector).val()) {
            var validator = main_ns.getModule("validator"); // https://github.com/chriso/validator.js
            if (validator.isEmail($("#" + selector).val())) {
                return 1;
            }
            else {
                return 2;
            }
        }
    }
    else if (type === "select") {
        if ($("#" + selector).val()) {
            return 1;
        }
    }
    else {
        if ($("#" + selector).val()) {
            return 1;
        }
    }
    return 0;
};

main_ns.errorInput = function (selector, label, error) {
    var required = $("#hdnRequired").val();
    var invalid = $("#hdnInvalid").val();
    var label = $("#" + label).text();
    label = label.substring(0, label.length - 1);
    if (error == 2) {
        $("#" + selector).val('');
        $("#" + selector).parent().addClass('has-error');
        $("#" + selector).attr('placeholder', label + ' ' + invalid);
    }
    else if (error == 3) {        
        $("#" + selector).parent().addClass('has-error');
        main_ns.msgError(label + ' ' + invalid, "#" + selector);
    }
    else if (error == 4) {
        $("#" + selector).parent().addClass('has-error');
        main_ns.msgError(label + ' ' + required, "#" + selector);
    }
    else {
        $("#" + selector).val('');
        $("#" + selector).parent().addClass('has-error');
        $("#" + selector).attr('placeholder', label + ' ' + required);
    }
};

// para acceder a los modulos amd definidos directamente y obtener sus metodos
main_ns.getModule = function (module) {
    return (require || requirejs).s.contexts._.defined[module];
};

/**
 * @param  {[string]} selector [id table]
 * @param  {[string]} list [comment the table]
 * @return {[dataTable]}   [table with options dataTable]
 */
var dataTable = function(selector, list){
    var options = {
        "order": [
            [0, "asc"]
        ],
        "bLengthChange": true,
        //'iDisplayLength': 7,
        "oLanguage": {
            "sLengthMenu": "_MENU_ registros por página",
            "sInfoFiltered": " - filtrada de _MAX_ registros",
            "sSearch": "Buscar: ",
            "sZeroRecords": "No existen, " + list,
            "sInfoEmpty": " ",
            "sInfo": 'Mostrando _END_ de _TOTAL_',
            "oPaginate": {
                "sPrevious": "Anterior",
                "sNext": "Siguiente"
            }
        }
    };
    $(selector).DataTable(options);
};

$(document).ready(function () {

    //Switch Navigation Menu
    $('#switch-nav').on('click', function () {
        $('.App-sidebar').animate({ width: 'toggle' })
        /*var self = $(this);
        $( "#switch-nav:checked" ).length == 1{
            self.animate({width:'toggle'})
        }*/
    });

    $('#listMenu').on('click', 'li', function () {
        $("#listMenu li").removeClass("active");
        $(this).addClass("active"); 
        // var _hash = $(this).find("a").attr("href");
        // console.log(_hash);
        // $("#listMenu li").removeClass("active").each(function(ind, data){
        //     var _lihash = $(data).find("a").attr("href");
        //     console.log(_lihash);
        //     if (_hash === _lihash) {
        //         $(data).addClass("active");                
        //         return false;
        //     };
        // });
    });
});