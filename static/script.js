document.addEventListener("DOMContentLoaded", () => {
  const groups = document.querySelectorAll(".star-input");
  if (!groups.length) return;

  groups.forEach(group => {
    const labels = group.querySelectorAll("label");

    labels.forEach(label => {
      label.addEventListener("mouseenter", () => {
        highlight(label);
      });

      label.addEventListener("mouseleave", () => {
        restore(group);
      });

      label.addEventListener("click", () => {
        set(group, label);
      });
    });
  });

  function highlight(label) {
    let el = label;
    while (el) {
      el.classList.add("active");
      el = el.nextElementSibling;
    }
  }

  function restore(group) {
    group.querySelectorAll("label").forEach(l => l.classList.remove("active"));
    const checked = group.querySelector("input:checked + label");
    if (checked) highlight(checked);
  }

  function set(group, label) {
    group.querySelectorAll("label").forEach(l => l.classList.remove("active"));
    highlight(label);
  }
});
