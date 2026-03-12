import React, { useState } from "react";
import { logUserAction } from "../actions/log-user";

export const LoginForm = () => {
  const [formUser, setFormUser] = useState("");
  const [formPassword, setFormPassword] = useState("");
  const [isLoged, setIsLoged] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const result = await logUserAction(formUser, formPassword);

    if (result.success) {
      setIsLoged(true);
      // Opcional: podrías redirigir al usuario al Home/Dashboard aquí
    } else {
      setError(result.error);
    }
  };

  if (isLoged) return <h3>Sesión iniciada correctamente.</h3>;

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit}>
        {error && <p style={{ color: "red" }}>{error}</p>}
        
        <input
          type="text"
          placeholder="Nombre de usuario"
          value={formUser}
          onChange={(e) => setFormUser(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={formPassword}
          onChange={(e) => setFormPassword(e.target.value)}
          required
        />
        <button type="submit">Ingresar</button>
      </form>
    </div>
  );
};