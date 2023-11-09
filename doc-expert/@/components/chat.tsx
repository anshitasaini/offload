import { useState } from "react"

import type { ChatMessageSchema } from "~api/openapi/schemas"

import ChatMessage from "./chat-message"
import PromptForm from "./prompt-form"

const Chat = () => {
  const [messages, setMessages] = useState<ChatMessageSchema[]>([
    {
      message: "Hello, I'm Bot!",
      sender: "bot"
    }
  ])
  return (
    <div className="max-h-screen overflow-y-auto">
      {messages.map((chatMessage, index) => (
        <div key={index}>
          <ChatMessage {...chatMessage} />
        </div>
      ))}
      <PromptForm messages={messages} setMessages={setMessages} />
    </div>
  )
}

export default Chat
