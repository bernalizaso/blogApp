import { blogApp } from "../api/blog-api";

export const logUserAction = async (username: string, password: string) => {
  try {
    const response = await blogApp.post("/login", {
      username: username,
      password: password,
    });

    const data = response.data;

    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      return { success: true, data };
    }

    return { success: false, error: "Token no encontrado en la respuesta" };
  } catch (error: any) {
    const message =
      error.response?.data?.detail || "Error de conexión con el servidor";
    return { success: false, error: message };
  }
};
