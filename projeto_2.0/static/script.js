document.addEventListener("DOMContentLoaded", function () {
    // Aplica o fade-in no body
    document.body.classList.add("fade-in");
  
    // Aguarda o fade-in do body antes de aplicar slide nos elementos
    setTimeout(() => {
      const elementos = document.querySelectorAll(".slide-in");
      elementos.forEach((el, i) => {
        setTimeout(() => {
          el.classList.add("active");
        }, i * 200); // Efeito cascata nos elementos
      });
    }, 500); // Delay pra não sobrepor o fade-in do body
  });
  