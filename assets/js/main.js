(function () {
  "use strict";

  var doc = document.documentElement;
  doc.classList.add("js");

  /* Header-Schatten beim Scrollen */
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 8);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* Mobile Navigation */
  var toggle = document.querySelector(".nav-toggle");
  function closeNav() {
    document.body.classList.remove("nav-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.querySelectorAll(".nav__link").forEach(function (a) {
      a.addEventListener("click", closeNav);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeNav();
    });
  }

  /* Aktiver Menüpunkt */
  var links = Array.prototype.slice.call(document.querySelectorAll(".nav__link[href^='#']"));
  if ("IntersectionObserver" in window && links.length) {
    var map = {};
    links.forEach(function (l) { map[l.getAttribute("href").slice(1)] = l; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && map[entry.target.id]) {
          links.forEach(function (l) { l.classList.remove("is-active"); });
          map[entry.target.id].classList.add("is-active");
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    Object.keys(map).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) spy.observe(el);
    });
  }

  /* Einblend-Animation */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* Jahr im Footer */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* Kontaktformular
     Sendet per fetch an das action-Ziel (contact.php). Ist dort kein
     PHP verfügbar, öffnet sich als Fallback das E-Mail-Programm. */
  var form = document.querySelector("[data-contact-form]");
  if (!form) return;
  var status = form.querySelector(".form__status");
  var button = form.querySelector("button[type='submit']");

  function show(type, text) {
    status.className = "form__status is-" + type;
    status.textContent = text;
  }

  function mailtoFallback(data) {
    var to = form.getAttribute("data-mailto");
    var subject = (data.get("subject") || form.getAttribute("data-subject")) + "";
    var body =
      data.get("message") + "\n\n— \n" +
      data.get("name") + "\n" +
      (data.get("company") ? data.get("company") + "\n" : "") +
      data.get("email") +
      (data.get("phone") ? "\n" + data.get("phone") : "");
    window.location.href = "mailto:" + to +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(body);
    show("ok", form.getAttribute("data-msg-mailto"));
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    var data = new FormData(form);
    if (data.get("website")) return; /* Spam-Honeypot */

    button.disabled = true;
    fetch(form.getAttribute("action"), {
      method: "POST",
      body: data,
      headers: { "Accept": "application/json" }
    })
      .then(function (res) {
        var type = res.headers.get("content-type") || "";
        if (!res.ok || type.indexOf("application/json") === -1) throw new Error("no-backend");
        return res.json();
      })
      .then(function (json) {
        if (json && json.ok) {
          form.reset();
          show("ok", form.getAttribute("data-msg-ok"));
        } else {
          show("error", form.getAttribute("data-msg-error"));
        }
      })
      .catch(function () {
        mailtoFallback(data);
      })
      .then(function () {
        button.disabled = false;
      });
  });
})();
