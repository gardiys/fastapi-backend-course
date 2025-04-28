export default {
    async fetch(request) {
      if (request.method !== "POST") {
        return new Response("Only POST allowed", { status: 405 });
      }
  
      try {
        const { prompt } = await request.json();
        return new Response(JSON.stringify({ response: `Вот как я решаю задачу: "${prompt}"` }), {
          headers: { "Content-Type": "application/json" },
        });
      } catch (err) {
        return new Response("Invalid JSON", { status: 400 });
      }
    },
  };