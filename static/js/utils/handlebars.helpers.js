﻿// requiere de i18n_ns
Handlebars.registerHelper('lang', function (key) {
    var result = i18n_ns.get(key);
    return new Handlebars.SafeString(result);
});

Handlebars.registerHelper('getLang', function () {
    var result = i18n_ns.getLang();
    return new Handlebars.SafeString(result);
});

Handlebars.registerHelper('first', function (context, block) {
    return block(context[0]);
});

Handlebars.registerHelper('getVirtualPath', function () {
    var result = main_globals.virtualPath;
    return new Handlebars.SafeString(result);
});

Handlebars.registerHelper('getUserName', function () {
    var result = main_globals.userFullname;
    return new Handlebars.SafeString(result);
});

Handlebars.registerHelper('verifyTour', function (flag, cod, val1, val2) {
    if(flag){
        return new Handlebars.SafeString(val1 + cod);
    }        
    else {
        return new Handlebars.SafeString(val2 + cod);
    }
});

Handlebars.registerHelper('equal', function (lvalue, rvalue, options) {
    if (arguments.length < 3)
        throw new Error("Handlebars Helper equal needs 2 parameters");
    if (lvalue != rvalue) {
        return options.inverse(this);
    } else {
        return options.fn(this);
    }
});

Handlebars.registerHelper("inc", function (value, options) {
    return parseInt(value) + 1;
});

Handlebars.registerHelper('ifCond', function (v1, operator, v2, options) {

    switch (operator) {
        case '==':
            return (v1 == v2) ? options.fn(this) : options.inverse(this);
        case '===':
            return (v1 === v2) ? options.fn(this) : options.inverse(this);
        case '<':
            return (v1 < v2) ? options.fn(this) : options.inverse(this);
        case '<=':
            return (v1 <= v2) ? options.fn(this) : options.inverse(this);
        case '>':
            return (v1 > v2) ? options.fn(this) : options.inverse(this);
        case '>=':
            return (v1 >= v2) ? options.fn(this) : options.inverse(this);
        case '&&':
            return (v1 && v2) ? options.fn(this) : options.inverse(this);
        case '||':
            return (v1 || v2) ? options.fn(this) : options.inverse(this);
        default:
            return options.inverse(this);
    }
});

Handlebars.registerHelper("prettifyDate", function (timestamp) {
    var d = new Date(timestamp.replace('T', ' '));
    var curr_date = d.getDate();
    var curr_month = d.getMonth();
    var curr_year = d.getFullYear();
    return curr_date + '/' + curr_month + '/' + curr_year;
});

Handlebars.registerHelper("prettifyDateHour", function (timestamp) {
    var d = new Date(timestamp.replace('T', ' '));
    var curr_date = d.getDate();
    var curr_month = d.getMonth();
    var curr_year = d.getFullYear();
    var curr_hour = d.getHours();
    var curr_minute = d.getMinutes();        
    return d.format("dd/mm/yy h:MM TT");;
    
});


/*
 * Date Format 1.2.3
 * (c) 2007-2009 Steven Levithan <stevenlevithan.com>
 * MIT license
 *
 * Includes enhancements by Scott Trenda <scott.trenda.net>
 * and Kris Kowal <cixar.com/~kris.kowal/>
 *
 * Accepts a date, a mask, or a date and a mask.
 * Returns a formatted version of the given date.
 * The date defaults to the current date/time.
 * The mask defaults to dateFormat.masks.default.
 */
var dateFormat = function () { var t = /d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZ]|"[^"]*"|'[^']*'/g, e = /\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g, a = /[^-+\dA-Z]/g, m = function (t, e) { for (t = String(t), e = e || 2; t.length < e;) t = "0" + t; return t }; return function (d, n, r) { var y = dateFormat; if (1 != arguments.length || "[object String]" != Object.prototype.toString.call(d) || /\d/.test(d) || (n = d, d = void 0), d = d ? new Date(d) : new Date, isNaN(d)) throw SyntaxError("invalid date"); n = String(y.masks[n] || n || y.masks["default"]), "UTC:" == n.slice(0, 4) && (n = n.slice(4), r = !0); var s = r ? "getUTC" : "get", i = d[s + "Date"](), o = d[s + "Day"](), u = d[s + "Month"](), M = d[s + "FullYear"](), l = d[s + "Hours"](), T = d[s + "Minutes"](), h = d[s + "Seconds"](), c = d[s + "Milliseconds"](), g = r ? 0 : d.getTimezoneOffset(), S = { d: i, dd: m(i), ddd: y.i18n.dayNames[o], dddd: y.i18n.dayNames[o + 7], m: u + 1, mm: m(u + 1), mmm: y.i18n.monthNames[u], mmmm: y.i18n.monthNames[u + 12], yy: String(M).slice(2), yyyy: M, h: l % 12 || 12, hh: m(l % 12 || 12), H: l, HH: m(l), M: T, MM: m(T), s: h, ss: m(h), l: m(c, 3), L: m(c > 99 ? Math.round(c / 10) : c), t: 12 > l ? "a" : "p", tt: 12 > l ? "am" : "pm", T: 12 > l ? "A" : "P", TT: 12 > l ? "AM" : "PM", Z: r ? "UTC" : (String(d).match(e) || [""]).pop().replace(a, ""), o: (g > 0 ? "-" : "+") + m(100 * Math.floor(Math.abs(g) / 60) + Math.abs(g) % 60, 4), S: ["th", "st", "nd", "rd"][i % 10 > 3 ? 0 : (i % 100 - i % 10 != 10) * i % 10] }; return n.replace(t, function (t) { return t in S ? S[t] : t.slice(1, t.length - 1) }) } }(); dateFormat.masks = { "default": "ddd mmm dd yyyy HH:MM:ss", shortDate: "m/d/yy", mediumDate: "mmm d, yyyy", longDate: "mmmm d, yyyy", fullDate: "dddd, mmmm d, yyyy", shortTime: "h:MM TT", mediumTime: "h:MM:ss TT", longTime: "h:MM:ss TT Z", isoDate: "yyyy-mm-dd", isoTime: "HH:MM:ss", isoDateTime: "yyyy-mm-dd'T'HH:MM:ss", isoUtcDateTime: "UTC:yyyy-mm-dd'T'HH:MM:ss'Z'" }, dateFormat.i18n = { dayNames: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"] }, Date.prototype.format = function (t, e) { return dateFormat(this, t, e) };