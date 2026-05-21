(async () => {
   const p = "pepe1234"; // Cambia esto por tu contraseña
   const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(p));
   const b64 = btoa(String.fromCharCode(...new Uint8Array(buf)));
   console.log("Tu hash en Base64 es:", b64);
})();