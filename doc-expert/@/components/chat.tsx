import { cn } from "@/lib/utils"
import { useEffect, useState } from "react"

import { chatSendMessage } from "~api/openapi/chat/chat"
import type { ChatMessageSchema } from "~api/openapi/schemas"

import ChatMessage from "./chat-message"
import PromptForm from "./prompt-form"
import { Separator } from "./ui/separator"

const Chat = () => {
  const [messages, setMessages] = useState<ChatMessageSchema[]>([
    {
      message:
        "Hi!\n\n I'm an assistant trained on this documentation!\n\n Ask me anything about `Airbyte`.",
      sender: "bot"
    }
  ])

  const showPopularQuestions = messages.length === 1

  const sendMessage = async (message: string) => {
    setMessages((messages) => [...messages, { message, sender: "user" }])

    const response = await chatSendMessage({
      current_url: window.location.href,
      history: messages,
      query: message
    })

    setMessages((messages) => [
      ...messages,
      { message: response.answer, sender: "bot" }
    ])
  }

  return (
    <div className="max-h-screen overflow-y-auto">
      <div className="flex-1 overflow-y-auto max-h-[80vh]">
        {messages.map((chatMessage, index) => (
          <div key={index}>
            <div className="p-3">
              <ChatMessage
                {...chatMessage}
                showPopularQuestions={showPopularQuestions}
                sendMessage={sendMessage}
              />
            </div>
            {index < messages.length - 1 && <Separator />}
          </div>
        ))}
      </div>
      <div className="p-4 px-10">
        <PromptForm sendMessage={sendMessage} />
      </div>
    </div>
  )
}

export default Chat
