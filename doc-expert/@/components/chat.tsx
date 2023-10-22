import ChatMessage from "./chat-message"
import PromptForm from "./prompt-form"
import { Separator } from "./ui/separator"

const Chat = () => {
  const messages = [
    "How can I help you?",
    "How do I install this library?",
    "I don't understand this part of the doc"
  ]
  return (
    <div>
      {messages.map((message, index) => (
        <div key={index}>
          <ChatMessage message={message} />
        </div>
      ))}
      <PromptForm />
    </div>
  )
}

export default Chat
