import { json } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";

// Замените на URL вашего бэкенда
const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export const POST: RequestHandler = async ({ request }) => {
  try {
    const { message } = await request.json();

    if (!message || typeof message !== "string") {
      return json({ error: "Invalid message" }, { status: 400 });
    }

    // Отправляем запрос к бэкенду
    const response = await fetch(`${BACKEND_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`);
    }

    const data = await response.json();

    return json({
      message: data.message || data.response || "No response from backend",
      sources: data.sources || [],
    });
  } catch (error) {
    console.error("Error communicating with backend:", error);

    return json(
      {
        error: "Failed to communicate with backend",
        message:
          "Извините, не удалось подключиться к серверу. Пожалуйста, убедитесь, что бэкенд запущен.",
      },
      { status: 500 }
    );
  }
};
