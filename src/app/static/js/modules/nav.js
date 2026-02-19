// Exportamos la función para poder importarla desde app.js u otros módulos.
export function initNavToggle() {
  const buttons = document.querySelectorAll(".mobile-nav-toggle"); //A
  const navMenu = document.querySelector("#navmenu"); //B
  if (!navMenu || buttons.length === 0) return; //C

  // Función que actualiza los íconos según el estado del menú
  // Recibe: isOpen (true si el menú quedó abierto)
  const syncIcons = (isOpen) => {
    buttons.forEach((btn) => { //D
      btn.classList.toggle("bi-list", !isOpen); //E
      btn.classList.toggle("bi-x", isOpen);//F
    });
  };

  // Función principal de toggle (abrir/cerrar menú)
  const toggle = () => {
    const isOpen = document.body.classList.toggle("mobile-nav-active");//G
    navMenu.classList.toggle("navmenu-open", isOpen); //H
    syncIcons(isOpen); //I
  };

  // Cuando el usuario hace click en cualquier botón, ejecutamos toggle().
  buttons.forEach((btn) => btn.addEventListener("click", toggle));
  navMenu.querySelectorAll("a").forEach((link) => { //J
    link.addEventListener("click", () => { //K
      if (document.body.classList.contains("mobile-nav-active"))
        toggle();//M
    });
  });
}

// A - Seleccionamos todos los botones que abren/cierran el menú móvil.
// B - Seleccionamos el contenedor del menú por id.
// C - Si no existe el menú o no hay botones, salimos.

// D - Recorremos todos los botones encontrados
// E - Si el menú NO está abierto (!isOpen), mostramos el ícono "bi-list"
// F - Si el menú está abierto (isOpen === true), mostramos el ícono "bi-x"

// G - Alternamos la clase mobile-nav-active en el <body>. Y guardamos en isOpen si quedó activado (true) o desactivado (false).
// H - Agregamos o quitamos la clase que abre/cierra el menú visualmente.
// I - Actualizamos íconos acorde al nuevo estado del menú.

// J - Si el usuario hace click en un link del menú, lo cerramos automáticamente.
// K - Si el menú está actualmente abierto...
// M - ...lo cerramos.