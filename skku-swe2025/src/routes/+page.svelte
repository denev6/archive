<script>
  import arrowIcon from "$lib/assets/arrow-up.svg";
  import SentenceBox from "./SentenceBox.svelte";

  let userMessage = "";
  let responseMessage = "";
  let textRequest = "";
  let is_loading = false;
  let conversations = [];
  const API_BASE_URL = "http://127.0.0.1:8001";

  async function askLLM() {
    is_loading = true; // prevent duplicate inputs

    if (!userMessage.trim()) {
      return;
    }
    conversations = [...conversations, ["user", userMessage]];
    document.getElementById("input-area").value = "";

    // JSON Request
    textRequest = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage }),
    };

    conversations = [...conversations, ["loading", "검색 중..."]];
    requestAnimationFrame(() => {
      scrollToBottom();
    });

    // Fetch response from API
    const response = await fetch(`${API_BASE_URL}/answer`, textRequest);

    responseMessage = ""; // init
    conversations = [...conversations.slice(0, -1), ["llm", responseMessage]];

    if (response.ok && response.body) {
      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let lastRender = Date.now(); // prevent overhead
      let sleepTime = 50;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        responseMessage += chunk;
        conversations[conversations.length - 1][1] = responseMessage;

        if (Date.now() - lastRender > sleepTime) {
          // force svelte to render on the user screen
          conversations = [...conversations];
          lastRender = Date.now();
        }
      }
    } else {
      responseMessage = "오류: 요청을 받을 수 없는 상태입니다.";
      conversations = [...conversations.slice(0, -1), ["llm", responseMessage]];
    }

    is_loading = false;
  }

  function handleKeydown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      if (!is_loading) {
        event.preventDefault();
        askLLM();
      }
    }
  }

  function scrollToBottom() {
    window.scrollTo({
      top: document.documentElement.scrollHeight,
      behavior: "smooth",
    });
  }
</script>

<svelte:document onkeydown={handleKeydown} />

<div id="floating-box">
  <div id="input-container">
    <textarea
      id="input-area"
      bind:value={userMessage}
      placeholder="무엇이 궁금한가요?"
    ></textarea>
    <button onclick={askLLM} onkeydown={handleKeydown} disabled={is_loading}
      ><img src={arrowIcon} alt="submit" /></button
    >
  </div>
</div>
<div id="conversation-container">
  {#each conversations as conversation, i}
    <SentenceBox speaker={conversation[0]} sentence={conversation[1]} />
  {/each}
</div>

<style>
  #floating-box {
    position: fixed;
    left: 50%;
    bottom: 16px;
    transform: translate(-50%, 0);
    width: 95%;
    text-align: center;
  }
  #input-container {
    background-color: var(--gray-800);
    border-radius: 8px;
    display: flex;
    align-items: flex-end;
    padding: 12px 8px 8px 16px;
  }
  textarea {
    flex-grow: 1;
    padding: 4px;
    font-size: 18px;
    line-height: 1.3;
    color: var(--text-dimmed);
    background-color: transparent;
    border: none;
    height: 60px;
    resize: none;
    overflow-y: auto;
    outline: none;
    font-family: inherit;
  }
  button {
    display: flex;
    justify-content: center;
    align-items: center;
    color: var(--gray-300);
    background-color: var(--primary-700);
    font-size: 24px;
    padding: 4px;
    border: none;
    border-radius: 50%;
    margin-left: 10px;
    cursor: pointer;
    align-self: flex-end;
    white-space: nowrap;
  }
  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  #conversation-container {
    margin-bottom: 160px;
  }
</style>
