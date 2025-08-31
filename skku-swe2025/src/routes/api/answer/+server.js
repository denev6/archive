/** @type {import('@sveltejs/kit').RequestHandler} */
export async function POST({ request }) {
  const { text } = await request.json();

  await new Promise((resolve) => setTimeout(resolve, 2000));

  const responseText = `테스트 응답입니다:\n입력: ${text}`;
  return new Response(JSON.stringify({ text: responseText }), {
    status: 200,
    headers: {
      "Content-Type": "application/json",
    },
  });
}
