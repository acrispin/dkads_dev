var request_ns = {};

request_ns.CountAjax = 0;

request_ns.showLoading = function () {
    request_ns.CountAjax = request_ns.CountAjax < 0 ? 1 : request_ns.CountAjax + 1;
    if (request_ns.CountAjax == 1) {
        $('#loadingpage').show();
    }
};

request_ns.hideLoading = function () {
    request_ns.CountAjax = request_ns.CountAjax - 1;
    if (request_ns.CountAjax == 0) {
        $('#loadingpage').hide();
    }
};

request_ns.clearLoading = function () {
    request_ns.CountAjax = 0;
    $('#loadingpage').hide();
};

request_ns.VerifyCustomErrorCode = function (request) {
    var rs = true;
    try {
        if (request.status === 403) {
            var obj = JSON.parse(request.responseText);
            if (obj.hasOwnProperty("CustomErrorCode")) {
                switch (obj.CustomErrorCode) {
                    case 5001:
                        document.location.href = "";
                        rs = false;
                        break;
                    default:
                        break;
                }
            }
        }
    } catch (e) {
        console.log(e)
    }
    return rs;
};

// constantes
request_ns.VERB_GET = "GET";
request_ns.VERB_POST = "POST";
request_ns.VERB_PUT = "PUT";
request_ns.VERB_DEL = "DELETE";
request_ns.CONTENT_TYPE_JSON = "application/json; charset=utf-8";
request_ns.CONTENT_TYPE_TEXT = "text/plain; charset=utf-8";


// _type = "GET" || "POST"
// _dataType = "xml" || "json" || "script" || "html" // tipo de contenido que se recibe del server
// _contentType = "application/x-www-form-urlencoded; charset=UTF-8" || "application/json; charset=utf-8" || "text/plain; charset=utf-8" // tipo de contenido que se envia al server
// _cache = true || false
// _async = true || false

request_ns.common = function (_url, _data, _type, _success, _error, _before, _complete, _dataType, _contentType, _cache, _async) {

    if (typeof _url === "undefined" || _url === null || _url === "" || typeof _url !== "string") _url = undefined; // location.href;
    if (typeof _data === "undefined" || _data === null || _data === "" || (typeof _data !== "string" && typeof _data !== "object")) _data = undefined;
    if (typeof _type === "undefined" || _type === null || _type === "" || typeof _type !== "string") _type = "GET";
    if (typeof _async === "undefined" || _async === null || _async === "" || typeof _async !== "boolean") _async = true;
    if (typeof _cache === "undefined" || _cache === null || _cache === "" || typeof _cache !== "boolean") _cache = false;
    if (typeof _contentType === "undefined" || _contentType === null || _contentType === "" || typeof _contentType !== "string") _contentType = "application/x-www-form-urlencoded; charset=UTF-8";
    if (typeof _dataType === "undefined" || _dataType === null || _dataType === "" || typeof _dataType !== "string") _dataType = undefined; // "*";

    $.ajax({
        url: main_globals.virtualPath + _url,
        data: _data,
        type: _type,
        async: _async,
        cache: _cache,
        contentType: _contentType,
        dataType: _dataType,
        success: function (data) {
            if ((typeof _success !== "undefined" || _success !== null) && typeof _success === "function") {
                _success(data);
            }
            else {
                console.log(data);
            }
        },
        error: function (request, status, error) {
            if (request_ns.VerifyCustomErrorCode(request)) {
                if ((typeof _error !== "undefined" || _error !== null) && typeof _error === "function") {
                    _error(request, status, error);
                }
                else {
                    alert(request.status + " - " + request.statusText);
                }
            }
        },
        beforeSend: function (obj) {
            if ((typeof _before !== "undefined" || _before !== null) && typeof _before === "function") {
                _before(obj);
            }
            else {
                request_ns.showLoading();
                //$("#loadingpage").show();
            }
        },
        complete: function (obj, status) {
            if ((typeof _complete !== "undefined" || _complete !== null) && typeof _complete === "function") {
                _complete(obj, status);
            }
            else {
                request_ns.hideLoading();
                //$("#loadingpage").hide();
            }
        }
    });
};

request_ns.get = function (_url, _data, _success, _error, _before, _complete, _dataType, _contentType, _cache, _async) {
    request_ns.common(_url, _data, request_ns.VERB_GET, _success, _error, _before, _complete, _dataType, _contentType, _cache, _async);
};

request_ns.get_json = function (_url, _data, _success, _error, _before, _complete, _contentType, _cache, _async) {
    request_ns.common(_url, _data, request_ns.VERB_GET, _success, _error, _before, _complete, "json", _contentType, _cache, _async);
};

request_ns.get_html = function (_url, _data, _success, _error, _before, _complete, _contentType, _cache, _async) {
    request_ns.common(_url, _data, request_ns.VERB_GET, _success, _error, _before, _complete, "html", _contentType, _cache, _async);
};

request_ns.post = function (_url, _data, _success, _error, _before, _complete, _dataType, _contentType, _cache, _async) {
    request_ns.common(_url, _data, request_ns.VERB_POST, _success, _error, _before, _complete, _dataType, _contentType, _cache, _async);
};

request_ns.post_net = function (_url, _data, _success, _error, _before, _complete, _dataType, _cache, _async) {
    var _dataparsed = JSON.stringify(_data);
    request_ns.common(_url, _dataparsed, request_ns.VERB_POST, _success, _error, _before, _complete, _dataType, request_ns.CONTENT_TYPE_JSON, _cache, _async);
};

request_ns.post_json = function (_url, _data, _success, _error, _before, _complete, _contentType, _cache, _async) {
    request_ns.common(_url, _data, request_ns.VERB_POST, _success, _error, _before, _complete, "json", _contentType, _cache, _async);
};

request_ns.post_json_net = function (_url, _data, _success, _error, _before, _complete, _cache, _async) {
    var _dataparsed = JSON.stringify(_data);
    request_ns.common(_url, _dataparsed, request_ns.VERB_POST, _success, _error, _before, _complete, "json", request_ns.CONTENT_TYPE_JSON, _cache, _async);
};

request_ns.post_html = function (_url, _data, _success, _error, _before, _complete, _contentType, _cache, _async) {
    request_ns.common(_url, _data, request_ns.VERB_POST, _success, _error, _before, _complete, "html", _contentType, _cache, _async);
};

request_ns.script = function (_url, _data, _type, _success, _error, _before, _complete, _contentType, _cache, _async) {
    request_ns.common(_url, _data, _type, _success, _error, _before, _complete, "script", _contentType, _cache, _async);
};

request_ns.html = function (_url, _data, _type, _success, _error, _before, _complete, _contentType, _cache, _async) {
    request_ns.common(_url, _data, _type, _success, _error, _before, _complete, "html", _contentType, _cache, _async);
};


// request galo

request_ns.get_galo = function (_url, _data, _success, _error, _before, _complete, _cache, _async) {
    var _dataparsed = JSON.stringify(_data);
    request_ns.common(main_globals.galoPath + _url, _dataparsed, request_ns.VERB_GET, _success, _error, _before, _complete, "json", request_ns.CONTENT_TYPE_JSON, _cache, _async);
};

request_ns.post_galo = function (_url, _data, _success, _error, _before, _complete, _cache, _async) {
    var _dataparsed = JSON.stringify(_data);
    request_ns.common(main_globals.galoPath + _url, _dataparsed, request_ns.VERB_POST, _success, _error, _before, _complete, "json", request_ns.CONTENT_TYPE_JSON, _cache, _async);
};

request_ns.put_galo = function (_url, _data, _success, _error, _before, _complete, _cache, _async) {
    var _dataparsed = JSON.stringify(_data);
    request_ns.common(main_globals.galoPath + _url, _dataparsed, request_ns.VERB_PUT, _success, _error, _before, _complete, "json", request_ns.CONTENT_TYPE_JSON, _cache, _async);
};

request_ns.del_galo = function (_url, _data, _success, _error, _before, _complete, _cache, _async) {
    var _dataparsed = JSON.stringify(_data);
    request_ns.common(main_globals.galoPath + _url, _dataparsed, request_ns.VERB_DEL, _success, _error, _before, _complete, "json", request_ns.CONTENT_TYPE_JSON, _cache, _async);
};

// request galo


///////// Global Ajax Events
function offAjaxGlobalEvents() {
    $(document).off("ajaxSend").off("ajaxComplete");
}

function onAjaxGlobalEvents() {
    if ($(".sectionLoadingAjax").length === 1) {
        $(document).on("ajaxSend", function () { $(".sectionLoadingAjax").show(); }).on("ajaxComplete", function () { $(".sectionLoadingAjax").hide(); });
    }
}

$(document).ready(function () {
    //onAjaxGlobalEvents();
});


