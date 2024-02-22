/*!
 * PDF.js v2.11.338 (build: 9f518b1d2)
 * Built on 2022-01-14
 * Copyright 2018 Mozilla Contributors
 * Licensed under GPLv3 (https://github.com/mozilla/pdf.js/blob/master/LICENSE)
 */
! function (t, e) {
    "object" == typeof exports && "undefined" != typeof module ? e(exports) : "function" == typeof define && define.amd ? define(["exports"], e) : (t = "undefined" != typeof globalThis ? globalThis : t || self, e(t.pdfjsWorker = {}))
}(this, (function (t) {
    "use strict";

    function e(t, e) {
        return t(e = {
            exports: {}
        }, e.exports), e.exports
    }

    function r(t, r) {
        return e((function (e, n) {
            var o;
            t((function (t) {
                t.exports = o = r()
            }), o = o || {})
        }))
    }

    function n(t) {
        return (n = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (t) {
            return typeof t
        } : function (t) {
            return t && "function" == typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
        })(t)
    }

    function o(t, e) {
        if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
    }

    function i(t, e) {
        for (var r = 0; r < e.length; r++) {
            var n = e[r];
            n.enumerable = n.enumerable || !1, n.configurable = !0, "value" in n && (n.writable = !0), Object.defineProperty(t, n.key, n)
        }
    }

    function a(t, e, r) {
        return e && i(t.prototype, e), r && i(t, r), t
    }

    function s(t, e) {
        return !e || "object" !== n(e) && "function" != typeof e ? function (t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }(t) : e
    }

    function c(t) {
        return (c = Object.setPrototypeOf ? Object.getPrototypeOf : function (t) {
            return t.__proto__ || Object.getPrototypeOf(t)
        })(t)
    }

    function u(t, e) {
        return (u = Object.setPrototypeOf || function (t, e) {
            return t.__proto__ = e, t
        })(t, e)
    }

    function l(t) {
        return (l = Object.getPrototypeOf ? Object.getPrototypeOf : function (t) {
            return t.__proto__ || Object.getPrototypeOf(t)
        })(t)
    }

    function f(t, e) {
        return (f = Object.setPrototypeOf || function (t, e) {
            return t.__proto__ = e, t
        })(t, e)
    }

    function h(t, e) {
        if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
        t.prototype = Object.create(e && e.prototype, {
            constructor: {
                value: t,
                writable: !0,
                configurable: !0
            }
        }), e && f(t, e)
    }

    function p(t) {
        return (p = Object.setPrototypeOf ? Object.getPrototypeOf : function (t) {
            return t.__proto__ || Object.getPrototypeOf(t)
        })(t)
    }

    function d(t, e) {
        return (d = Object.setPrototypeOf || function (t, e) {
            return t.__proto__ = e, t
        })(t, e)
    }
}));


