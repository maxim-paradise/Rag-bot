import { ref } from "vue";
import { chatAPI } from "@/api/chat";

export const useChatAPI = () => {
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const sendMessage = async (message: string): Promise<string> => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await chatAPI.sendMessage({
        message,
        model: "gpt-3.5-turbo",
        temperature: 0.7,
        max_tokens: 1000,
      });

      return response.response;
    } catch (err) {
      console.error("API Error:", err);
      error.value = "Произошла ошибка при отправке сообщения";
      return "Извините, произошла ошибка. Попробуйте еще раз.";
    } finally {
      isLoading.value = false;
    }
  };

  return {
    sendMessage,
    isLoading,
    error,
  };
};
