/* Учебный вход и отметки. Всё хранится только в этом браузере (localStorage). */
(function () {
  var ROOT = window.SITE_ROOT || "";
  var ROLES = { uchenik: "Ученик", kurator: "Куратор", rukovoditel: "Руководитель Академии" };
  function get(k, d) { try { var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } }
  function set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  var user = get("dp-user", null);

  // шапка
  var link = document.getElementById("login-link");
  if (link && user && ROLES[user.role]) {
    link.textContent = "Мой кабинет";
    link.href = ROOT + "kabinet/" + user.role + ".html";
  }
  document.querySelectorAll("[data-who]").forEach(function (el) {
    el.innerHTML = user ? "Вы вошли как: <b>" + (user.name ? esc(user.name) + ", " : "") + ROLES[user.role] + "</b> · <a href='" + ROOT + "vhod.html'>сменить</a>"
                        : "Вы не вошли. <a href='" + ROOT + "vhod.html'>Войти</a>";
  });
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  // вход
  var form = document.getElementById("login-form");
  if (form) {
    if (user) {
      form.name.value = user.name || "";
      var r = form.querySelector("input[value='" + user.role + "']"); if (r) r.checked = true;
    }
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var role = form.querySelector("input[name=role]:checked").value;
      set("dp-user", { name: form.name.value.trim(), role: role });
      location.href = ROOT + "kabinet/" + role + ".html";
    });
    document.getElementById("logout").addEventListener("click", function () {
      try { localStorage.removeItem("dp-user"); } catch (e) {}
      location.href = ROOT + "index.html";
    });
  }

  // отметка «Изучено» на странице материала
  var studied = get("dp-studied", {});
  document.querySelectorAll(".studied[data-mat]").forEach(function (el) {
    var id = el.getAttribute("data-mat");
    var b = document.createElement("button");
    b.type = "button"; b.className = "btn small";
    function paint() { b.textContent = studied[id] ? "✓ Изучено" : "Отметить как изученное"; b.classList.toggle("done", !!studied[id]); }
    b.onclick = function () { studied[id] = !studied[id]; set("dp-studied", studied); paint(); };
    paint(); el.appendChild(b);
  });

  // прогресс в кабинете ученика
  var prog = document.getElementById("progress");
  if (prog && window.CATALOG) {
    function render() {
      var html = "";
      window.CATALOG.forEach(function (bl) {
        var done = bl.items.filter(function (i) { return studied[i.id]; }).length;
        var pct = Math.round(100 * done / bl.items.length);
        html += "<details class='pb'><summary><span class='pbt'>Блок " + bl.n + ". " + esc(bl.title) + "</span>" +
          "<span class='bar'><i style='width:" + pct + "%'></i></span><span class='pbn'>" + done + " из " + bl.items.length + "</span></summary><ul>";
        bl.items.forEach(function (i) {
          html += "<li><label><input type='checkbox' data-id='" + i.id + "'" + (studied[i.id] ? " checked" : "") + "> " +
            "<a href='" + ROOT + i.href + "'>" + esc(i.title) + "</a></label></li>";
        });
        html += "</ul></details>";
      });
      prog.innerHTML = html;
      prog.querySelectorAll("input[data-id]").forEach(function (cb) {
        cb.onchange = function () { studied[cb.getAttribute("data-id")] = cb.checked; set("dp-studied", studied); var open = [].map.call(prog.querySelectorAll("details"), function (d) { return d.open; }); render(); prog.querySelectorAll("details").forEach(function (d, k) { d.open = open[k]; }); };
      });
    }
    render();
  }

  // поля, которые сохраняются в браузере
  var saved = document.querySelector("[data-saved]");
  document.querySelectorAll("[data-save]").forEach(function (f) {
    var k = "dp-f-" + f.getAttribute("data-save");
    f.value = get(k, "");
    f.addEventListener("input", function () { set(k, f.value); if (saved) saved.textContent = "Сохранено в этом браузере"; });
  });

  // разбор куратора
  var copy = document.getElementById("copy-review");
  if (copy) {
    copy.onclick = function () {
      var parts = [];
      document.querySelectorAll("#razbor [data-save]").forEach(function (f) {
        var label = f.closest("label").querySelector("span").textContent;
        if (f.value.trim()) parts.push(label + ":\n" + f.value.trim());
      });
      var text = parts.join("\n\n");
      (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(
        function () { copy.textContent = "Скопировано"; setTimeout(function () { copy.textContent = "Скопировать разбор"; }, 1500); },
        function () { window.prompt("Скопируйте текст:", text); });
    };
    document.getElementById("clear-review").onclick = function () {
      document.querySelectorAll("#razbor [data-save]").forEach(function (f) { f.value = ""; set("dp-f-" + f.getAttribute("data-save"), ""); });
    };
  }
})();
